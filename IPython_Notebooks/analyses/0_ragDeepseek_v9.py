from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Title
from langchain_community.document_loaders import PDFPlumberLoader
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.vectorstores import FAISS

from FlagEmbedding import BGEM3FlagModel ## new -- pip install -U FlagEmbedding
from langchain_core.embeddings import Embeddings ## new
from langchain_ollama.llms import OllamaLLM

from langchain_core.prompts import ChatPromptTemplate

from typing import Union, List, Literal, Annotated
from typing import Any, Optional
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from pydantic_extra_types.country import CountryShortName

from unidecode import unidecode
import pandas as pd
import json
import os
import gc
import re
import time
import numpy as np
import unicodedata
import math
import datetime
import pickle

import asyncio
from tqdm.asyncio import tqdm_asyncio

"""
This file runs the screening and coding pipeline against the test list files

This version modifications from previous iterations
- add more examples to clarify boundaries of category definitions. Corrected some typos that may have led to parsing errors
- run again for all variables
- change structured answer approach -- use smaller model like phi3 for restructuring and use langchain OutputFixingParser to extract parsed output. return think tags if present
- change codeVariable so that it outputs default values if all values none limit reached, otherwise outputs nan values
"""

## Import RAG functions ----------------
with open(f'/home/dveytia/IPython_Notebooks/Product_4/pyFunctions/genericRAG_functions.py') as f:
    exec(f.read())
    
with open(f'/home/dveytia/IPython_Notebooks/Product_4/pyFunctions/deepSeekRAG_9_functions.py') as f:
    exec(f.read())




## Constant variables --------------------------------------
v = 9 # Version of the script

# Paths
dataFolder = '/homedata/dveytia/Product_4_data'
pdfs_directory = f'{dataFolder}/data/raw-data/testListPDFs/'
faiss_directory = f'{dataFolder}/data/derived-data/testList_vectorstores_partitioned_bgem3_300/'
answer_directory = f'{dataFolder}/outputs/testListDeepseekAnswers_v{v}/'
checkpoint_path = os.path.join(answer_directory, "batch_checkpoint.json")
log_path = os.path.join(answer_directory, "cluster_log.txt")
# check directories exists and create if not
os.makedirs(faiss_directory, exist_ok=True) 
os.makedirs(answer_directory, exist_ok=True) 

# Batching parameters
max_concurrent_tasks = 1  # concurrency limit
batch_size = 25
max_failed_id_retries = 5 # number of times to retry a failed id in a batch
codeMaxRetries = 8 # number of times to retry each variable if parsing fails

# RAG parameters
# Chunk size and overlap for text splitting (in characters)
chunk_size = 300
chunk_overlap=50
faissK = 2 # the number of similar chunks to return

embeddings = LangchainBGEM3Embeddings()
model1 = OllamaLLM(model="deepseek-r1:7b", temperature=0.2)
model2 = OllamaLLM(model="phi3:3.8b", temperature=0.2)




# Get a list of the id pdfs in the directory
pdfs = os.listdir(pdfs_directory)
pdfs = [x for x in pdfs if ".pdf" in x]
pdfs = [x.replace(".pdf","") for x in pdfs]
split_data = [s.split('_', 1) for s in pdfs]
ids = [x[0] for x in split_data]
ids = [x for x in ids if x.isdigit()]


answered = os.listdir(answer_directory)
answered = [x.replace("_code.txt","") for x in answered]
answered = [x for x in answered if x.isdigit()] 

# Only process the unanswered pdfs
unansweredPdfs = [x for x in ids if x not in answered]
print(f'Processing {len(unansweredPdfs)} PDFs')

# ----- Main async runner with batching -----
async def main_batched():
    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    total_batches = math.ceil(len(unansweredPdfs) / batch_size)
    log_failed_ids = load_failed_ids_from_log(log_path)

    completed_batches = load_checkpoint()

    for i in range(total_batches):
        batch_pdfs = unansweredPdfs[i * batch_size: (i + 1) * batch_size]

        # First go through completed bactches and retry failed IDs
        if i in completed_batches:
            failed_ids = [int(file) for file in batch_pdfs if int(file) in log_failed_ids]
    
            if not failed_ids:
                print(f"✅ Skipping batch {i + 1}/{total_batches} (already completed)")
                continue
            else:
                print(f"⚠️ Reprocessing failed IDs in completed batch {i + 1}/{total_batches}: {failed_ids}")
                log_event(f"Retrying failed IDs in completed batch {i + 1}")
    
                retries = 0
                while failed_ids and retries < max_failed_id_retries:
                    retries += 1
                    log_event(f"Retry {retries} for failed IDs in completed batch {i + 1}: {failed_ids}")
                    print(f"🔁 Retrying {len(failed_ids)} failed docs (attempt {retries}/{max_failed_id_retries})")
    
                    retry_pdfs = [file for file in batch_pdfs if int(file) in failed_ids]
                    failed_ids.clear()
    
                    tasks = [code_with_throttle(file, semaphore, failed_ids) for file in retry_pdfs]
                    await tqdm_asyncio.gather(*tasks, desc=f"Retrying batch {i+1} - Attempt {retries}")
    
                    if failed_ids:
                        await asyncio.sleep(3)
    
                if failed_ids:
                    log_event(f"⚠️ Failed IDs remain after retrying completed batch {i + 1}: {failed_ids}")
                else:
                    log_event(f"✅ Completed batch {i + 1} now fully successful")
    
            continue  # skip re-processing the whole batch again

        # (original batch processing block continues here...)
        print(f"\n▶️ Starting batch {i + 1}/{total_batches} ({len(batch_pdfs)} docs)")
        log_event(f"Started batch {i + 1}/{total_batches} with {len(batch_pdfs)} docs")

        failed_ids = []
        tasks = [code_with_throttle(file, semaphore, failed_ids) for file in batch_pdfs]
        await tqdm_asyncio.gather(*tasks, desc=f"Batch {i+1}/{total_batches}")

        # === Retry Loop for Failed IDs ===
        retries = 0
        while failed_ids and retries < max_failed_id_retries:
            retries += 1
            log_event(f"Retry attempt {retries} for failed IDs: {failed_ids}")
            print(f"🔁 Retrying {len(failed_ids)} failed docs (attempt {retries}/{max_failed_id_retries})")

            # Build task list for retries
            retry_failed_ids = failed_ids.copy()
            failed_ids.clear()

            retry_pdfs = [file for file in batch_pdfs if int(file) in failed_ids]
            tasks = [code_with_throttle(file, semaphore, failed_ids) for file in retry_pdfs]
            await tqdm_asyncio.gather(*tasks, desc=f"Retry {retries}/{max_failed_id_retries}")

            if failed_ids:
                await asyncio.sleep(3)

        # === Post-batch reporting ===
        if failed_ids:
            log_event(f"Batch {i + 1} completed with unrecoverable errors: {failed_ids}")
        else:
            log_event(f"Finished batch {i + 1} with all documents processed successfully")

        completed_batches.add(i)
        save_checkpoint(completed_batches)

        await asyncio.sleep(2)  # optional cooldown

    log_event("✅ All batches completed.")


# ----- Entry point -----
if __name__ == "__main__":
    asyncio.run(main_batched())



## Format test list answers --------------------------
# The data are highly nested as json, so to unnest (partially), make each row a unique publication id x oro combination, and then each coded variable is a column. There may be multiple labels for each coded variables within the same cell.
"""
compiled_answer_directory = '/homedata/dveytia/Product_4_data/outputs/testListDeepseekAnswers_compiled/'

# Get a list of which ids have already been answered
answered = os.listdir(answer_directory)
answered = [x.replace("_code.txt","") for x in answered]
answered = [x for x in answered if x.isdigit()] 
print(f"Combining {len(answered)} answers into a data frame")


answers = []
answers_study_results = []
for file in answered:

    file_path = f"{answer_directory}{file}_code.txt"
    with(open(file_path)) as f:
        answer_dict = json.load(f)

    doc_id = answer_dict.get('id')
    responses = answer_dict.get('coding response',[])
    read_error = answer_dict.get('pdf reading error')

    if read_error:
        flat_row = answer_dict
        answers.append(flat_row)
        continue   
    
    if not responses:
        continue
        
    flat_row = {'id': doc_id}

    # Each response is a dict with a single variable
    for response in responses[0]:
        if not isinstance(response, dict):
            continue

        for var_name, value in response.items():

            # If value is a dict (e.g., with 'error_message' and 'source text'), flatten those too
            if isinstance(value, dict):
                for subkey, subval in value.items():
                    if isinstance(subval, list):
                        subval = list(set(subval)) # de-deuplicate
                    flat_row[f"{var_name} {subkey}"] = subval
            elif var_name == 'study_results' and isinstance(value, list) and len(value)>0:
                for study_result in value:
                        study_result['id'] = doc_id
                        answers_study_results.append(study_result)
                
            elif isinstance(value, list):
                value = list(set(value)) # de-deuplicate
                flat_row[var_name] = value
            else:
                flat_row[var_name] = value

    answers.append(flat_row)
    



# Bind all dataframes together
answers_df = pd.DataFrame(answers)
answers_df['id'] = answers_df['id'].astype(int)
print(f"Answers shape: {answers_df.shape}")
answers_df.head()

study_results_metadata = answers_df[['id', 'study results source text','study results error_message'], 'study results raw output']
answers_df = answers_df.drop(['study results source text','study results error_message','study_results'], axis=1)

colOrder = [
    'id', 
    'include', 'safe fish source text', 'safe fish error_message', 'safe fish raw output',
    'intervention_institutional','ORO_institutional source text', 'ORO_institutional error_message','ORO_institutional raw output',
    'intervention_technology', 'ORO_technology source text', 'ORO_technology error_message','ORO_technology raw output',
    'intervention_infrastructure', 'ORO_infrastructure source text', 'ORO_infrastructure error_message', 'ORO_infrastructure raw output',
    'climatic_impact_driver', 'climatic impact driver source text','climatic impact driver raw output',
    'study_method', 'study method source text', 'study method raw output',
    'spatial_scale','continent','study location source text', 'study location error_message','study location raw output',
    'time_scale', 'duration_description','time scale source text', 'time scale error_message','time scale raw output',
    'procedural_equity','procedural equity source text','procedural equity raw output',
    'governance_body', 'rules_of_law', 'governance source text','governance error_message','governance raw output',
    'pdf reading error'
    ]

colOrder = [col for col in colOrder if col in list(answers_df)]

answers_df = answers_df[colOrder]


## Save 
answers_df.to_excel(f'{compiled_answer_directory}testList_answers_df_v{v}.xlsx', index=False)

if len(answers_study_results)>0:
    answers_study_results_df = pd.DataFrame(answers_study_results)
    answers_study_results_df['id'] = answers_study_results_df['id'].astype(int)
    answers_study_results_df = answers_study_results_df.merge(
        study_results_metadata, on = 'id', how = 'outer'
    )
    # organize columns
    cols = list(answers_study_results_df)
    cols.insert(0, cols.pop(cols.index('id')))
    answers_study_results_df = answers_study_results_df.loc[:, cols]
    print(f"Answers results shape: {answers_study_results_df.shape}")
    answers_study_results_df.head()

    ## Save
    answers_study_results_df.to_excel(
    f'{compiled_answer_directory}testList_answers_df_studyResults_v{v}.xlsx', index=False)




"""






