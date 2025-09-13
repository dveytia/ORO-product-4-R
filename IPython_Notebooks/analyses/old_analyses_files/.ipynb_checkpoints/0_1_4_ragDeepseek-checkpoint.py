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

This version specifies a pdf section for some coded variables

"""



## PROMPTS AND SCHEMAS ------------------------------------------------


## List of variables and label definitions to loop through


interventionCriteria = """
    
    Interventions must be relevant to climate change adaptation or resilience in fisheries, fishing communities, or the fishing industry. This includes the direct environmental and ecological consequences of climate change, such as ocean acidification, increased storm frequency or intensity, marine heatwaves, changes in fish distribution due to temperature changes, etc.
    
    ### Eligible Interventions Include:
    
    ## Institutional Interventions
    - Ocean governance
    - Marine spatial planning
    - Integrated coastal zone management
    - Climate-related policies and agreements
    
    ## Management of Fisheries or Practices
    - Co-management
    - Adaptive or ecosystem-based management
    - Community-based management
    
    ## Socio-Behavioral Interventions
    - Changing fishing gear/location/species
    - Mobility and relocation
    - Livelihood diversification
    - Human migration or exiting the fishery
    
    ## Economic Interventions
    - Insurance
    - Finance/market mechanisms
    - New value chains/markets
    
    ## Interventions Guarding Against Climate Hazards
    - Disaster response programs
    - Early warning systems
    - Seasonal or dynamic forecasting
    
    ## New Technologies
    - New fishing technologies
    - Biotechnology
    
    ## Hard Infrastructure
    - Seawalls, artificial reefs
    - Port or processing infrastructure
    - Gear or vessel modification
    
    ## Soft Infrastructure
    - Beach, dune, or shore nourishment

    
    ### Excluded Interventions:
    - Aquaculture or agriculture-related interventions
    - Purely descriptive studies with no intervention studied
    - Theoretical/future suggestions without implemented intervention
    - Interventions addressing overfishing/pollution without mention of climate change or hazards
    
    
    """




## Import RAG functions ----------------
with open(f'/home/dveytia/IPython_Notebooks/Product_4/pyFunctions/genericRAG_functions.py') as f:
    exec(f.read())
    
with open(f'/home/dveytia/IPython_Notebooks/Product_4/pyFunctions/deepSeekRAG_3_functions.py') as f:
    exec(f.read())


# Test functions on test list ---------------------
embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
model1 = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.2)
model2 = OllamaFunctions(model="phi3:3.8b", format="json", temperature=0)


v = 4 # Version of the script
dataFolder = '/homedata/dveytia/Product_4_data'
pdfs_directory = f'{dataFolder}/data/raw-data/testListPDFs/'
faiss_directory = f'{dataFolder}/data/derived-data/testList_vectorstores_partitioned_15b/'
answer_directory = f'{dataFolder}/outputs/testListDeepseekAnswers_v{v}/'

## For testing
file = '252'
process_pdf(file)
response_dict = json.load(open(f"{answer_directory}{file}.txt"))
print(response_dict)


# Get a list of the id pdfs in the directory
pdfs = os.listdir(pdfs_directory)
pdfs = [x for x in pdfs if ".pdf" in x]
pdfs = [x.replace(".pdf","") for x in pdfs]
split_data = [s.split('_', 1) for s in pdfs]
ids = [x[0] for x in split_data]
ids = [x for x in ids if x.isdigit()]

# Get a list of which ids have already been answered
if not os.path.exists(answer_directory):
    os.mkdir(answer_directory)
    print(f"created answer directory: {answer_directory}")

answered = os.listdir(answer_directory)
answered = [x.replace(".txt","") for x in answered]
answered = [x for x in answered if x.isdigit()] 

# Only process the unanswered pdfs
unansweredPdfs = [x for x in ids if x not in answered]
print(f'Processing {len(unansweredPdfs)} PDFs')

# Answer texts
for file in tqdm(unansweredPdfs):
	process_pdf(file)

# print(json.load(open(f"{answer_directory}{unansweredPdfs[0]}.txt"))) # then open the pdf you just processed



## Format test list answers --------------------------

"""
The data are highly nested as json, so to unnest (partially), make each row a unique publication id x oro combination, and then each coded variable is a column. There may be multiple labels for each coded variables within the same cell.
"""
compiled_answer_directory = '/homedata/dveytia/Product_4_data/outputs/testListDeepseekAnswers_compiled/'

# Get a list of which ids have already been answered
answered = os.listdir(answer_directory)
answered = [x.replace(".txt","") for x in answered]
answered = [x for x in answered if x.isdigit()] 
print(f"Combining {len(answered)} answers into a data frame")


answers = []
for file in answered:
    answer_dict = json.load(open(f"{answer_directory}{file}.txt"))
    if answer_dict.get('interventions',[]):
        tempDat= pd.json_normalize(
            answer_dict,
            record_path = 'interventions',
            meta = ['id']
        )
        tempDat=tempDat.explode('coded variables')
        
        codedVariablesMelt = tempDat.copy()
        codedVariablesMelt = (codedVariablesMelt
                              .pop("coded variables")
                              .apply(pd.Series)
                              .explode('labels')
                             )
        tempDatMelt = tempDat.merge(codedVariablesMelt, how='left', left_index=True, right_index=True)
        tempDatMelt = tempDatMelt.drop(columns=['error_message','coded variables'])

        # Pivot variables wider? so each row is a paper x unique oro combination
        tempDatMelt = tempDatMelt.pivot_table(
            index=['intervention', 'reason', 'id'],  
            columns='variable',                      
            values='labels',                         
            aggfunc='first'                          
        ).reset_index()

        # Append dataframe to list
        answers.append(
            tempDatMelt
        )


# Bind all dataframes together
answers_df = pd.concat(answers)
answers_df['id'] = answers_df['id'].astype(int)

print(f"Answers shape: {answers_df.shape}")
print(answers_df.head())


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


