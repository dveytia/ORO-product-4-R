

# Prompt to generative Q&A model classify as included or excluded based on a given labels
promptIntervention_unstructured = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert assistant helping to classify whether a scientific article contains information relevant to certain criteria"),
    ("human", 
     """Determine whether this scientific article studies interventions that meet the criteria provided: 

     ### scientific article: {context}

     ### criteria: {categories}

     Return a summary including: (1) A list of any eligible interventions; (2) the reasoning for your conclusion. If you don't know the answer, or the classification is not applicable to the article, reply 'not applicable'. DON'T MAKE UP ANYTHING.
""")
])


## Prompts for structuring answers from Q&A model
# Prompt to structure screening response

promptIntervention_structured = ChatPromptTemplate.from_template("""
You are a helpful assistant that extracts eligible interventions from a response and explains the reasoning for why they were selected.
---

Response:
{response}

Reasoning:
{reasoning}

---

Given a response and reasoning, return a structured list of interventions and reasons. If you don't know the answer to a field, write 'None'. DON'T MAKE UP ANYTHING.

"""
)


## Define schemas 
# class interventionList(BaseModel):
#     label_list: List[str] = Field(description="List of the names of each category assigned to the article", required=False);
#     label_reasoning: List[str] = Field(description="Reasoning for classifying the intervention into the chosen category", required=False);

## To allow for multiple choice, adapt code below from pydantic v2 to v1
# https://docs.pydantic.dev/latest/concepts/fields/#discriminator

## The structuring of each intervention
class intervention(BaseModel):
    label: str = Field(
        default="None",
        description="A description of the intervention that was identified as eligible"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this intervention as eligible"
    )

class interventionList(BaseModel):
    interventions: List[intervention] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all eligible interventions and their associated reasoning"
    )




## FUNCTIONS FOR QUESTION ANSWERING -------------------------------------
# Get an answer from the generative Q&A model
def answer_question(documents, promptIntervention_unstructured, labels):
    chain=(
        promptIntervention_unstructured
        | model1
    )
    return chain.invoke({"categories": labels,"context": format_docs(documents)})

# extract think tags from the generative Q&A model
def getThinkTag(answer):
    match = re.search(r"<think>(.*?)</think>", answer, re.DOTALL)
    if match:
        extracted_text = match.group(1).strip()
        return extracted_text
    else:
        return None

# extract the answer from the generative Q&A model
def getAnswer(answer):
    split_text = answer.rsplit("</think>", 1)
    if len(split_text) > 1:
        after_think = split_text[1].strip()
        return after_think
    else:
        return None

## Structure the answer given a prompt and schema
def structure_answer(response, reasoning, promptIntervention_structured, schema):
    chain=(
        promptIntervention_structured
        | model2.with_structured_output(schema, include_raw=True) 
    )
    return chain.invoke({"response": response, "reasoning":reasoning})



## Package together to get a structured answer of all OROs
def answerOROs(variable, labels, vector_store, max_retries = 3):
    related_documents = vector_store.similarity_search(labels)

    # Try several times because of randomness introduced by temperature, sometimes the 
    # model results don't conform
    for attempt in range(max_retries):
        try:
            answer = answer_question(related_documents, promptIntervention_unstructured, labels)
            reasoning = getThinkTag(answer)
            response = getAnswer(answer)
            answer_structured = structure_answer(response, reasoning, promptIntervention_structured, interventionList)
            answer_list = answer_structured['parsed'].dict()['interventions']
            # Add the labels variable to dict name
            answer_dict = {
                "variable": variable,
                "labels": answer_list
            }
            answer_dict
            break
        except Exception as e:
            answer_dict = {
                'variable': variable,
                'error_message': str(e)
            }
    return answer_dict

## Package together to provide structured answer to a given eligibility labels
def answerVariables(variable, labels, vector_store, max_retries = 3):
    related_documents = vector_store.similarity_search(labels)

    # Try several times because of randomness introduced by temperature, sometimes the 
    # model results don't conform
    for attempt in range(max_retries):
        try:
            answer = answer_question(related_documents, promptIntervention_unstructured, labels)
            reasoning = getThinkTag(answer)
            response = getAnswer(answer)
            answer_structured = structure_answer(response, reasoning, promptIntervention_structured, interventionList)
            answer_dict = answer_structured.dict()
            # Add the labels variable to dict name
            answer_dict["error_message"] = 'None'
            answer_dict = {f"{variable}_{key}": value for key, value in answer_dict.items()}
            break
        except Exception as e:
            answer_dict = {
                'error_message': str(e)
            }
            answer_dict = {f"{variable}_{key}": value for key, value in answer_dict.items()}

    return answer_dict

# # Example use: Screen all eligibility variables
# labelResults = {}
# for variable, labels in variables.items():
#     labelResults.update(answerVariables(variable, labels, vector_store))



## Functions for RAG -------------------------------

# load pdfs
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages

def split_text(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " "]
    )
    chunks = text_splitter.split_documents(pages)
    return chunks


# If vectors don't exist, get them from embeddings function
def get_vectorstore(text_chunks, embeddings):
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# If vectors exist, load them
def load_vectorstore(faiss_path, embeddings):
    """Load FAISS vectorstore from disk if available."""
    if os.path.exists(faiss_path):
        return FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
    return None


# Retrieve relevant chunks based on similarity to variables
def retrieve_docs(query, vector_store):
    return vector_store.similarity_search(query)



# Chain together  the prompts and models
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)






### Wrap all the functions together #####
def process_pdf(file, variables):
    try:
        # RAG AI functions
        files = os.listdir(pdfs_directory)
        pdf_path = [f for f in files if file+'_' in f]
        pdf_path = pdf_path[0]
        pdf_path = os.path.join(pdfs_directory, pdf_path)
        faiss_path = os.path.join(faiss_directory, f"{file}.faiss")

        vector_store = load_vectorstore(faiss_path, embeddings)
        if vector_store is None:
            text = load_pdf(pdf_path)
            chunked_text = split_text(text)
            vector_store = get_vectorstore([x.page_content for x in chunked_text], embeddings)
            vector_store.save_local(faiss_path)

        # Question answering functions
        # First get a list of all the OROs in the article
        answer_dict = answerOROs(variable, labels, vector_store)
        answer_dict['id'] = int(file)

        # answer_dataframe = pd.json_normalize(
        #     answer_dict,
        #     record_path='labels',
        #     meta=['id', 'variable']
        # )

        # # Then for each ORO (item in the list 'labels', add further labels...
        # labelResults = answer_dict['labels']
        # for oro, labels in variables.items():
        #     labelResults.update(answerVariables(variable, labels, vector_store))

        # Explicitly delete large objects and force GC
        del vector_store
        
    except Exception as e:
        answer_dict = {
            'response_status': 'error',
            'id': int(file),
            'error': str(e)
        }

    # Save to disk
    json.dump(answer_dict, open(os.path.join(answer_directory, f"{file}.txt"), 'w'))


    gc.collect()
    time.sleep(10)

    return file  # Just for progress reporting



