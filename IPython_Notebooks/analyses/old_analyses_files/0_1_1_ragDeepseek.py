from langchain_community.document_loaders import PDFPlumberLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List

# from typing import List, Literal, Union
# from langchain_core.pydantic_v1 import ValidationError

from langchain_experimental.llms.ollama_functions import OllamaFunctions
from PyPDF2 import PdfReader
import pandas as pd
from tqdm import tqdm
import json
import os
import gc
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor, as_completed
import re
import time

"""

This version updates was set up to label oro type from a specified set of categories (not tested)

"""



## PROMPTS AND SCHEMAS ------------------------------------------------


## List of variables and label definitions to loop through


variables = {
    "oro_subType": """
    ### Intervention type

    The technology, infrastructure, practice, behaviour, institutional policy, or action that the study is measuring a response to, impact from, or outcome from is referred to at the 'intervention'. A study can measure effects of an intervention while the intervention is being implemented (e.g. ***), or by inference by comparing before the intervention was implimented and after, comparing between groups where an intervention has taken place and where an intervention is absent or less intense (e.g. comparing outcomes between groups with different management practices). Thus the intervention does not need to be implemented in the study, so long as the study is designed to measure or infer its impacts/outcomes. Studies of the outcomes from environmental changes caused directly by an intervention are included (e.g. ***). 

Studies of interventions that aim to improve the adaptation or resilience of fisheries (across all scales from individuals/small scale communities to national and international policies) in response to climate change should be classified based on the type of interventions presented in the study (multiple choice is possible). Interventions are first classified according to three types: Socio-institutional (***), Technology (***), and Infrastructure (***). Each type is classified further into a sub-type:
- "institutional": Socio-institutional sub-type, includes options on ocean governance, institutional agreements, marine spatial planning and integrated coastal zone managmeent
- "management": Socio-institutional sub-type, includes options on co-management, adaptive management, ecosystem based management, community based management, sustainable management
- "socio-behavioral": Socio-institutional sub-type, includes options on fishing mobility, changing fish gear, fishing location, targeted species, lievelihood diversification, migration, relocation, exiting the fishery
- "economic": Socio-institutional sub-type, includes options on finance & market mechanisms, insurances, new markets
- "climate services": Technology sub-type, includes disaster response programs, early warning systems, seasonal and dynamic forecasts, societal monitoring systems
- "new technologies": Technology sub-type, includes biotechnology and new fishing technologies
- "hard infrastructure": Infrastructure sub-type, includes accomodation, retreat, seawalls, artificial reefs, gear/vessel modification
- "soft infrastructure": Infrastructure sub-type, includes beach, dunes, shore nourishment


Excluded interventions:
- Interventions unrelated to the ocean
- Purely descriptive articles with no intervention
- marine or coastal ecosystem conservation or restoration with no mention of aiming to faciliate societal adaptation to climate change hazards
- human assisted evolution to facilitate natural adaptation (e.g. genetic engineering of heat-tolerant corals)
- marine protected areas (MPAs)

***Rule: Classify all eligible interventions according to their appropriate sub type, and respond with a list of all applicable sub-type names (values available from the following list: ["management", "institutional", "socio-behavioral","economic", "climate services", "new technologies","hard infrastructure", "soft infrastructure"]) ***
    """
}



## Import RAG functions ----------------
with open(f'/home/dveytia/IPython_Notebooks/Product_4/pyFunctions/deepSeekRAG_functions.py') as f:
    exec(f.read())


# Test functions on test list ---------------------
embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
model1 = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.2)
model2 = OllamaFunctions(model="phi3:3.8b", format="json", temperature=0)


v = 5 # Version of the script
dataFolder = '/homedata/dveytia/Product_4_data'
pdfs_directory = f'{dataFolder}/data/raw-data/testListPDFs/'
faiss_directory = f'{dataFolder}/data/derived-data/testList_vectorstores_15b/'
answer_directory = f'{dataFolder}/outputs/testListDeepseekAnswers_v{v}/'

# Get a list of the id pdfs in the directory
pdfs = os.listdir(pdfs_directory)
pdfs = [x.replace(".pdf","") for x in pdfs]
pdfs = [x for x in pdfs if x.isdigit()] 

# Get a list of which ids have already been answered
if not os.path.exists(answer_directory):
    os.mkdir(answer_directory)
    print(f"created answer directory: {answer_directory}")

answered = os.listdir(answer_directory)
answered = [x.replace(".txt","") for x in answered]
answered = [x for x in answered if x.isdigit()] 

# Only process the unanswered pdfs
unansweredPdfs = [x for x in pdfs if x not in answered]
print(f'Processing {len(unansweredPdfs)} PDFs')

# Answer texts
for file in tqdm(unansweredPdfs):
	process_pdf(file, variables)

# print(json.load(open(f"{answer_directory}{unansweredPdfs[0]}.txt"))) # then open the pdf you just processed



## Format test list answers --------------------------
compiled_answer_directory = '/homedata/dveytia/Product_4_data/outputs/testListDeepseekAnswers_compiled/'

# Get a list of which ids have already been answered
answered = os.listdir(answer_directory)
answered = [x.replace(".txt","") for x in answered]
answered = [x for x in answered if x.isdigit()] 
print("Combining all answers into a data frame")

answers = []
missing_answers = []
for file in answered:
	answer_dict = json.load(open(f"{answer_directory}{file}.txt"))
	
	if answer_dict['response_status'] != 'error':
		answers.append(answer_dict)
	else:
		missing_answers.append(answer_dict)

answers_df = pd.DataFrame(answers)
answers_df['id'] = answers_df['id'].astype(int)
missing_answers_df = pd.DataFrame(missing_answers)
print(f"Answers shape: {answers_df.shape}")
print(f"Missing answers shape: {missing_answers_df.shape}")

# ## Get test list metadata
# df_testList = pd.read_csv(f'{dataFolder}/raw-data/product2_testList.txt', delimiter = '\t')
# df_testList = df_testList.rename(columns={"TI": "title", "AB": "abstract", "DE":"keywords","DI":"doi"})
# df_testList["id"] = list(df_testList.index)
# df_testList = df_testList[["id","title","abstract","keywords","doi"]]
# df_testList['relevant'] = 1
# df_testList['random_sample'] = "test list"

# ## Merge with metadata
# answers_df = answers_df.merge(df_testList, on='id', how = 'right')

## Save 
answers_df.to_excel(f'{compiled_answer_directory}testList_answers_df_v{v}.xlsx', index=False)








# # With screened abstracts ---------------------------
# pdfs_directory = '/homedata/dveytia/Product_2_data/derived-data/screenedTitleAbstractsPdfs/'
# faiss_directory = '/homedata/dveytia/Product_2_data/derived-data/screenedTitleAbstractsPdfs_vectorstores/'
# answer_directory = '/homedata/dveytia/Product_2_data/outputs/screenDeepseekAnswers_v4/'
# # Get a list of the id pdfs in the directory
# pdfs = os.listdir(pdfs_directory)
# pdfs = [x.replace(".pdf","") for x in pdfs]
# pdfs = [x for x in pdfs if x.isdigit()] 

# # Get a list of which ids have already been answered
# if not os.path.exists(answer_directory):
#     os.mkdir(answer_directory)
#     print(f"created answer directory: {answer_directory}")
    
# answered = os.listdir(answer_directory)
# answered = [x.replace(".txt","") for x in answered]
# answered = [x for x in answered if x.isdigit()] 

# # Only process the unanswered pdfs
# unansweredPdfs = [x for x in pdfs if x not in answered]
# print(f'Processing {len(unansweredPdfs)} PDFs')




# ## TESTING--------------------
# # ## To test just one pdf
# for file in tqdm([unansweredPdfs[0]]):
# 	process_pdf(file, variables)
# print(json.load(open(f"{answer_directory}{unansweredPdfs[0]}.txt"))) # then open the pdf you just processed

# # Also test for articles which model got wrong in last version:
# fileIdsToTest = ['69821', '310890', '325476', '181', '346886', '32087', '25130']
# for file in tqdm(fileIdsToTest):
# 	process_pdf(file, variables)

# # then open the answers you just processed
# for file in fileIdsToTest:
#     print(json.load(open(f"{answer_directory}{file}.txt"))) 


