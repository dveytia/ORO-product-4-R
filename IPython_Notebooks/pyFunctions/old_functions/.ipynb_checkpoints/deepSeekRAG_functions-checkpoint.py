

# Prompt to generative Q&A model classify as included or excluded based on a given labels
prompt_unstructured = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert assistant helping to classify a scientific article"
     "according to user-defined descriptive typologies."),
    ("human", 
     """Given the text of a scientific article, use the variable description and possible categories to classify the scientific article into one of the categories. If you don't know the answer, or the classification is not applicable to the article, reply 'not applicable'. DON'T MAKE UP ANYTHING.

--------------------------
{categories}
--------------------------

Using the descriptions of the possible categories, please classify the following article:

--------------------------
{context}
--------------------------

Return a response including:
- A list of the category or categories that are relevant to the article
- The reasoning for each category assignment
""")
])


## Prompts for structuring answers from Q&A model
# Prompt to structure screening response
prompt_structured = ChatPromptTemplate.from_template("""
You are an assistant for structured question-answering tasks. The following input is a response generated from a large language model for question-answering tasks:
{response}

--- 

As well as the associated reasoning from the model:
{reasoning}

---

The model was asked to classify a scientific document into categories based on a predefined typology, and to provide it's reasoning. List all selected categories identified by the model and structure your response according to the provided schema. If you don't know the answer to a field, write 'False'. DON'T MAKE UP ANYTHING.
"""
)


## Define schemas 
# class listLabels(BaseModel):
#     label_list: List[str] = Field(description="List of the names of each category assigned to the article", required=False);
#     label_reasoning: List[str] = Field(description="Reasoning for classifying the intervention into the chosen category", required=False);

## To allow for multiple choice, adapt code below from pydantic v2 to v1
# https://docs.pydantic.dev/latest/concepts/fields/#discriminator

# Allowed labels
ALLOWED_LABELS = {"management", "institutional", "socio-behavioral","economic", "climate services", "new technologies","hard infrastructure", "soft infrastructure"}

class listLabels(BaseModel):
    label_list: List[str] = Field(
        description="List of the names of each category assigned to the article",
        required=False
    )
    label_reasoning: List[str] = Field(
        description="Reasoning for classifying the intervention into the chosen category",
        required=False
    )

    # Custom validator to restrict values
    @validator("label_list", each_item=True)
    def validate_label(cls, v):
        if v not in ALLOWED_LABELS:
            raise ValueError(f"'{v}' is not a valid label. Allowed labels: {sorted(ALLOWED_LABELS)}")
        return v




## FUNCTIONS FOR QUESTION ANSWERING -------------------------------------
# Get an answer from the generative Q&A model
def answer_question(documents, prompt_unstructured, labels):
    chain=(
        prompt_unstructured
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
def structure_answer(response, reasoning, prompt_structured, schema):
    chain=(
        prompt_structured
        | model2.with_structured_output(schema)
    )
    return chain.invoke({"response": response, "reasoning":reasoning})


## Package together to provide structured answer to a given eligibility labels
def answerVariables(variable, labels, vector_store, max_retries = 3):
    related_documents = vector_store.similarity_search(labels)

    # Try several times because of randomness introduced by temperature, sometimes the 
    # model results don't conform
    for attempt in range(max_retries):
        try:
            answer = answer_question(related_documents, prompt_unstructured, labels)
            reasoning = getThinkTag(answer)
            response = getAnswer(answer)
            answer_structured = structure_answer(response, reasoning, prompt_structured, listLabels)
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
        pdf_path = os.path.join(pdfs_directory, f"{file}.pdf")
        faiss_path = os.path.join(faiss_directory, f"{file}.faiss")

        vector_store = load_vectorstore(faiss_path, embeddings)
        if vector_store is None:
            text = load_pdf(pdf_path)
            chunked_text = split_text(text)
            vector_store = get_vectorstore([x.page_content for x in chunked_text], embeddings)
            vector_store.save_local(faiss_path)

        # Question answering functions
        labelResults = {}
        for variable, labels in variables.items():
            labelResults.update(answerVariables(variable, labels, vector_store))

        labelResults['id'] = int(file)
        labelResults['response_status'] = 'responded'

        # Explicitly delete large objects and force GC
        del vector_store
        
    except Exception as e:
        labelResults = {
            'response_status': 'error',
            'id': int(file),
            'error': str(e)
        }

    # Save to disk
    json.dump(labelResults, open(os.path.join(answer_directory, f"{file}.txt"), 'w'))


    gc.collect()
    time.sleep(10)

    return file  # Just for progress reporting



