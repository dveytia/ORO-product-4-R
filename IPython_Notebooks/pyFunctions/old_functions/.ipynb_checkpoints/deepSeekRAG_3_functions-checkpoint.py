

## STEP 1: SCREEN BY INTERVENTION --------------------------------------

# Prompt to generative Q&A model classify as included or excluded based on a given labels
promptIntervention_unstructured = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert assistant helping to identify and list all eligible interventions studied in the provided scientific article, according to the provided definitions"),
    ("human", 
     """Identify and list all eligible interventions studied in the provided scientific article, according to the definitions of eligible interventions provided: 

     ---

     #### Scientific article: {context}

     #### Definition of Intervention: 
    An intervention refers to any technology, infrastructure, practice, behavior, institutional policy, or action that the study measures a response, impact, or outcome from. This can include: direct measurement during implementation, retrospective comparison before/after the intervention, comparative analysis between exposed and non-exposed groups.
    
    {interventionCriteria}
    ---
    
    #### Instruction: ####
    - Identify all eligible interventions explicitly studied in the article as a part of the research methodology. These interventions must be distinct/separate from each other and not synonyms used to describe the same intervention. Do not include interventions only mentioned speculatively or theoretically 
    - DO NOT mention any irrelevant interventions in your response.
    - Return a summary including: (1) A list of the interventions you identified; (2) The reasoning for selecting each intervention. 
    - If you don't know the answer, or the classification is not applicable to the article, reply 'None'. DON'T MAKE UP ANYTHING.
    ---
""")
])


# Prompt to structure intervention response
promptIntervention_structured = ChatPromptTemplate.from_template("""
You are a helpful assistant that extracts eligible interventions from a response and explains the reasoning for why they were selected.
---
Response:
{response}

Reasoning:
{reasoning}
---

#### Instruction: ####
Given a response and reasoning, return a structured list of interventions and the reason for why each was selected. If you don't know the answer to a field, write 'None'. DON'T MAKE UP ANYTHING.

"""
)

## Intervention schemas
class interventionSafeFish(BaseModel):
    intervention: str = Field(
        default="None",
        description="A description of the intervention that was identified as eligible"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this intervention as eligible"
    )

class interventionSafeFishList(BaseModel):
    interventions: List[interventionSafeFish] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all eligible interventions and their associated reasoning"
    )


## Langchain functions for input > prompt > model

# Get an answer from the generative Q&A model
def screenIntervention(related_documents, interventionCriteria, promptIntervention_unstructured):
    chain=(
        promptIntervention_unstructured
        | model1
    )
    return chain.invoke({"context": format_docs(related_documents), "interventionCriteria": interventionCriteria})

# Structure the answer given a prompt and schema
def structure_screenIntervention(response, reasoning, promptIntervention_structured, schema):
    chain=(
        promptIntervention_structured
        | model2.with_structured_output(schema, include_raw=True) 
    )
    return chain.invoke({"response": response, "reasoning":reasoning})



## Package together to get a structured answer of all OROs
def answerScreenIntervention(interventionCriteria, vector_store, max_retries = 3):
    related_documents = vector_store.similarity_search(interventionCriteria)

    # Try several times because of randomness introduced by temperature, sometimes the 
    # model results don't conform
    for attempt in range(max_retries):
        try:
            answer = screenIntervention(related_documents, interventionCriteria, promptIntervention_unstructured) 
            reasoning = getThinkTag(answer)
            response = getAnswer(answer)
            answer_structured = structure_screenIntervention(response, reasoning, promptIntervention_structured, interventionSafeFishList)
            answer_list = answer_structured['parsed'].dict()['interventions']
            # Add the labels variable to dict name
            answer_dict = {
                "interventions": answer_list
            }
            answer_dict
            break
        except Exception as e:
            answer_dict = {
                'interventions': None,
                'error_message': str(e)
            }
    return answer_dict




## STEP 2: CODE VARIABLES IF INTERVENTIONS FOUND --------------------------------------

promptCode_unstructured = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert assistant helping to extract information pertaining to a specific intervention studied in the provided scientific article"),
    ("human", 
     """
     ## Task: For the scientific article provided, extract the metadata related to the intervention named: {intervention_name}.

     ## Scientific article: {context}
     
     ## Use the metadata field below to guide your response.
     Metadata Variable: {variable}
     Definition:
     {variable_description}

    ### Instructions ###
    - Focus only on information pertaining to the intervention named "{intervention_name}".
    - Extract the value(s) for the metadata variable "{variable}" as described above. 
    - If multiple values are relevant (e.g. multiple outcomes or study areas), list them all.
    - Only extract values that are explicitly stated in the study text (not inferred).
    - Return a response with a list of any relevant values identified. DO NOT include irrelevant values in your response. If the information is not provided, return: None. DON'T MAKE UP ANYTHING.
""")
])


# Prompt to structure response
promptCode_structured = ChatPromptTemplate.from_template("""
## Task: Extract eligible values for the metadata variable: "{variable}" from a response. For each eligible value, summarize the reasoning for why it was selected.
---

## Metadata variable definition.
Metadata Variable: {variable}
Definition:
{variable_description}

## Response: {response}

## Reasoning: {reasoning}
---

#### Instructions ####
- Return a structured response according to the schema provided. 
- DO NOT include values that were deemed irrelevant in your response. ONLY include relevant values.
- If the information is not provided, return: None. DON'T MAKE UP ANYTHING.

"""
)

# Variable schemas --- STILL NEED TO WRITE

# Study area ---------------------
class studyArea(BaseModel):
    label: str = Field(
        default="None",
        description="The geographical area where the research on the intervention was conducted."
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this as the study area of the intervention."
    )

class studyAreaList(BaseModel):
    labels: List[studyArea] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all study areas identified as relevant to the intervention."
    )

# Unit adapting ----------------------
class unitAdapting(BaseModel):
    label: str = Field(
        default="None",
        description="A unit the intervention is aiming to help adapt"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for selecting this as a relevant adapting unit for the intervention"
    )

class unitAdaptingList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[unitAdapting] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all adapting units identified as relevant to the intervention."
    )

# Underrepresented group --------------------------
class underrepresentedGroup(BaseModel):
    label: str = Field(
        default="None",
        description="An underrepresented group"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this as a relevant underrepresented group for the intervention"
    )

class underrepresentedGroupList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[underrepresentedGroup] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all underrepresented groups identified as relevant to the intervention."
    )

# Study method -------------------------
class studyMethod(BaseModel):
    label: str = Field(
        default="None",
        description="A method used to study the intervention"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this as a relevant study method for the intervention"
    )

class studyMethodList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[studyMethod] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all study methods identified as relevant to the intervention."
    )


## Fishing sector ---------------
class fishingSector(BaseModel):
    fisherySize: str = Field(
        default="None",
        description="The size of the fishery (e.g. artisinal, small, large, industrial) that the intervention acts on"
    )
    fisheryType: str = Field(
        default="None",
        description="The type of fishery (e.g. commercial or subsistence) that the intervention acts on"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this as a relevant fishery for the intervention"
    )

class fishingSectorList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[fishingSector] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all fisheries identified as relevant to the intervention."
    )

## Procedural equity ---------------
class proceduralEquity(BaseModel):
    label: str = Field(
        default="None",
        description="A description of how procedural equity was considered in the planning, design or implementation of the intervention."
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this as a relevant form of procedural equity for the intervention"
    )

class proceduralEquityList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[proceduralEquity] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all procedural equity considerations identified as relevant to the intervention."
    )

## Governance body ---------------
class governanceBody(BaseModel):
    label: str = Field(
        default="None",
        description="A description of the governance body responsible for the intervention's activities."
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this governance body as relevant for the intervention."
    )

class governanceBodyList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[governanceBody] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all governance bodies identified as relevant to the intervention."
    )

## Rules of law -------------------------------
class rulesOfLaw(BaseModel):
    label: str = Field(
        default="None",
        description="A description of the rule of law that governs the intervention's activities."
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this rule of law as relevant for the intervention."
    )

class rulesOfLawList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[rulesOfLaw] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all rules of law identified as relevant to the intervention."
    )

## Additional pressures -----------------
class additionalPressure(BaseModel):
    label: str = Field(
        default="None",
        description="A description of the additional pressure affecting the intervention"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this additional pressure as relevant for the intervention."
    )

class additionalPressureList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[additionalPressure] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all additional pressures identified as relevant to the intervention."
    )

## Climatic impact driver --------------
class climaticImpactDriver(BaseModel):
    label: str = Field(
        default="None",
        description="A description of the climatic impact driver that the intervention targets."
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this climatic impact driver as relevant for the intervention."
    )

class climaticImpactDriverList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[climaticImpactDriver] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all climatic impact drivers identified as relevant to the intervention."
    )

## Result --------------------
class studyResult(BaseModel):
    description: str = Field(
        default="None",
        description="A short description of the result."
    )
    metric: str = Field(
        default="None",
        description="Any quantitiative metrics or statistics used to measure the result"
    )
    dataType: str = Field(
        default="None",
        description="Whether the result is quantitative (i.e. numeric) or qualitative (i.e. descriptive/observational)"
    )
    resultDirection: str = Field(
        default="None",
        description="A description of whether the result is positive (e.g. success, improvement, adaptation, increase), negative (e.g. failure, mal-adaptation, decrease), neutral (no directionality), or mixed (positive on some aspects, negative on others)"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this result as relevant to the intervention."
    )

class studyResultList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[studyResult] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all results identified as relevant to the intervention."
    )


## Barriers and limits
class barrierLimit(BaseModel):
    description: str = Field(
        default="None",
        description="A short description of the barrier or limit."
    )
    isBarrier: bool = Field(
        default_factory=False,
        description="Is it a barrier that CAN be overcome?"
    )
    isLimit: bool = Field(
        default_factory=False,
        description="Is it a limit that CANNOT be overcome?"
    )
    reason: str = Field(
        default = "None",
        description="The model's reasoning for identifying this barrier or limit as relevant to the intervention."
    )

class barrierLimitList(BaseModel):
    # Note this field must always be named 'labels'
    labels: List[barrierLimit] = Field(
        default_factory=list,  # Default to an empty list
        description="List of all barriers or limits identified as relevant to the intervention."
    )


## Then store all schemas and descriptions in a list
variableDescriptions = [
    {
        'variable': 'study area',
        'variable_description': 'Geographic location of the study',
        'variable_schema': studyAreaList  # Only one study area per oro
    },
    {
        'variable': 'adapting unit',
        'variable_description': """
        Who is the intervention aimed at helping adapt? Select any that apply: Individuals (e.g. single persons, households); Organizations (e.g. NGOs, firms, public institutions, professional associations); Sectors (e.g. large or small scale fishing sector or aquaculture); Institutions (broad definition encompassing all administrative units).
        """,
        'variable_schema': unitAdaptingList
    },
    {
        'variable': 'underrepresented group',
        'variable_description': """
        Any underrepresented, marginalized or minority demographic groups that the intervention aims to help adapt. These must be explicitly mentioned and not inferred. For example women, indigeneous people, a particular ethnicity group. 
        """,
        'variable_schema': underrepresentedGroupList
    },
    {
        'variable': 'study method',
        'variable_description': """
        What methods did the study use to collect data? These include: experiments, analyzing existing data, observation, workshops, interviews, surveys, anecdotal evidence, conversations, ethnographies. 
        """,
        'variable_schema': studyMethodList
    },
    {
        'variable': 'fishing sector',
        'variable_description': """
        Describe each fishery studied in the article. Include in your description: a) The size of the fishery (e.g. artisinal, small, large, industrial); and b) the type of fishery (e.g. commercial or subsistence). 
        """,
        'variable_schema': fishingSectorList
    },
    {
        'variable': 'procedural equity',
        'variable_description': """
        Was procedural equity considered in the planning, design or implementation of the intervention? Examples of procedural equity include: communities having a voice in the decisionmaking process; inclusive engagement; considerations make for gender equity, social justice, inclusiveness; factoring in of local or indigenous knowledge; participatory approaches. Determine if procedural equity was considered and summarize how. 
        """,
        'variable_schema': proceduralEquityList
    },
    {
        'variable': 'governance body',
        'variable_description': """
        What institution/institutions are responsible for governing the activities of the intervention? Examples include: communities; municiple governments; national governments; regional institutions (e.g. regional fisheries management organizations (RFMOs)); international/global governance (e.g. international agreements), private organizations/companies.
        """,
        'variable_schema': governanceBodyList
    },
    {
        'variable': 'rules of law',
        'variable_description': """
        How is the intervention governed? Examples include: binding laws; policies; strategies; codes of conduct; informal rules.
        """,
        'variable_schema': rulesOfLawList
    },
    {
        'variable': 'additional pressures',
        'variable_description': """
        Are any additional pressures identified that may affect the outcome (e.g. success, failure, effectiveness) of the intervention? These pressures can be related to the political, socioeconomic or ecological context of the fishery. Additional pressures can include: overfishing; overcapacity; bycatch; pollution; invasive species; socio-economic crisis; conflicts/instability; health crisis.
        """,
        'variable_schema': additionalPressureList
    },
    {
        'variable': 'climatic impact driver',
        'variable_description': """
        What climatic impact drivers does the intervention aim to address? A climatic impact-driver is a physical climate condition that is being altered by climate change. These can be changes in long-term conditions (e.g. ocean warming, sea level rise, changes in ocean pH/ocean acidification, changes in ocean circulation/currents) or the changes in the frequency/intensity of events (e.g. storms, coastal flooding, marine heatwaves).
        """,
        'variable_schema': climaticImpactDriverList
    },
    {
        'variable': 'result',
        'variable_description': """
        What are the main results/findings from the research on the intervention? This should be reported in the study's 'Results' section. For EACH result relevant to the intervention, return a response that summarizes (if provided): a) a short description of the result; b) any quantitiative metrics or statistics used to measure the result; c) whether the result is quantitative (i.e. numeric) or qualitative (i.e. descriptive/observational); d) whether the result is positive (e.g. success, improvement, adaptation, increase), negative (e.g. failure, mal-adaptation, decrease), neutral (no directionality), or mixed (positive on some aspects, negative on others). 
        """,
        'variable_schema': studyResultList
    },
    {
        'variable': 'barrier or limit',
        'variable_description': """
        Are any barriers or limits to the intervention explicitly mentioned? Barriers or limits can pertain to any stage of the intervention process, including development, planning, design, implementation or operation. Examples of barriers or limits include: lack of capital; lack of leadership; lack of legal framework; lack of knowledge. For each barrier or limit identified as relevant for the intervention, provide: 1) a description of the barrier or limit; 2) whether it is a barrier that can be overcome (True/False); 3) whether it is a limit that CANNOT be overcome (True/False).
        """,
        'variable_schema': barrierLimitList
    },
]




## Langchain functions for input > prompt > model

# Get an answer from the generative Q&A model
def codeVariable(related_documents, intervention, variable, variable_description, promptCode_unstructured):
    chain=(
        promptCode_unstructured
        | model1
    )
    return chain.invoke({"context": format_docs(related_documents), "intervention_name":intervention, "variable":variable, "variable_description":variable_description})


# Structure the answer given a prompt and schema
def structure_codeVariable(response, reasoning, variable, variable_description, promptCode_structured, schema):
    chain=(
        promptCode_structured
        | model2.with_structured_output(schema, include_raw=True) 
    )
    return chain.invoke({"response": response, "reasoning":reasoning, "variable":variable, "variable_description": variable_description})



## Package together to get a structured answer
def answerCodeVariable(intervention, variable, variable_description, variable_schema, vector_store, max_retries = 3):
    related_documents = vector_store.similarity_search(intervention + variable + variable_description)

    # Try several times because of randomness introduced by temperature, sometimes the 
    # model results don't conform
    for attempt in range(max_retries):
        try:
            variableAnswer = codeVariable(related_documents, intervention, variable, variable_description, promptCode_unstructured) 
            reasoning = getThinkTag(variableAnswer)
            response = getAnswer(variableAnswer)
            variableAnswer_structured = structure_codeVariable(response, reasoning, variable, variable_description, promptCode_structured, variable_schema)
            variableAnswer_list = variableAnswer_structured['parsed'].dict()['labels']
            # Add the labels variable to dict name
            variableAnswer_dict = {
                "variable": variable,
                "labels": variableAnswer_list
            }
            variableAnswer_dict
            break
        except Exception as e:
            variableAnswer_dict = {
                'variable': variable,
                'error_message': str(e)
            }
    return variableAnswer_dict












### STEP 3: WRAP ALL FUNCTIONS TOGETHER ----------------------


### Wrap all the functions together #####
def process_pdf(file):
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
        answer_dict = answerScreenIntervention(interventionCriteria, vector_store) 
        answer_dict['id'] = int(file)

        # answer_dataframe = pd.json_normalize(
        #     answer_dict,
        #     record_path='labels',
        #     meta=['id', 'variable']
        # )
 

        # Then for each ORO (item in the list 'labels', add further labels...
        interventions = answer_dict['interventions'] # a list of the oros
        if len(interventions)> 0:
            for i, interventionResponse in enumerate(interventions):
                ## for testing:
                # i=0
                # interventionResponse = interventions[0]
                intervention = interventionResponse.get("intervention","")
                
                codedVariables = []
                # for item in [variableDescriptions[1]]: ## for testing
                for item in variableDescriptions:
                    variable = item.get('variable')
                    variable_description = item.get('variable_description')
                    variable_schema = item.get('variable_schema')  # This is the class itself
                    variableAnswer_dict = answerCodeVariable(
                        intervention,
                        variable,
                        variable_description,
                        variable_schema,
                        vector_store
                    )
                    # print(variableAnswer_dict) ## for testing
                    codedVariables.append(variableAnswer_dict)

                answer_dict['interventions'][i]['coded variables'] = codedVariables

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
    time.sleep(2)

    return file  # Just for progress reporting



