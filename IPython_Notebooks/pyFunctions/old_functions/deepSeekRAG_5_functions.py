
## STEP 0: DEFINE SCHEMAS FOR MULTIPLE CHOICE LABELS

## ORO type -- Intervention -------------------------------
class Institutional(BaseModel):
    intervention_type: Literal['Institutional'] = Field(..., description="Institutional interventions (e.g. Ocean governance, Marine spatial planning, Integrated coastal zone management, Climate-related policies and agreements)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class FisheriesManagement(BaseModel):
    intervention_type: Literal['Fisheries management'] = Field(..., description="Management of fisheries or changing fishing practices (e.g. co-management, adaptive or ecosystem-based management, community-based management)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class SocioBehavioural(BaseModel):
    intervention_type: Literal['Socio-Behavioural'] = Field(..., description="Socio-behavioural interventions (e.g. changing fishing gear/location/species, mobility and relocation, livelihood diversification, human migration or exiting the fishery)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class Economic(BaseModel):
    intervention_type: Literal['Economic'] = Field(..., description="Economic interventions (e.g. insurance, finance/market mechanisms, new value chains/markets)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class NewTechnologies(BaseModel):
    intervention_type: Literal['New technologies'] = Field(..., description="New technologies to adapt to changing fish (e.g. new fishing technologies, biotechnology)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class ClimateServices(BaseModel):
    intervention_type: Literal['Climate services technologies'] = Field(..., description="New technologies to guard against coastal climate hazards (e.g. disaster response programs, early warning systems, seasonal/dynamic forecasting)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class HardInfrastructure(BaseModel):
    intervention_type: Literal['Hard infrastructure'] = Field(..., description="Hard or physical built infrastructure (e.g. seawalls, artificial reefs, ports or processing infrastructure, gear or vessel modification)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class SoftInfrastructure(BaseModel):
    intervention_type: Literal['Soft infrastructure'] = Field(..., description="Soft infrastructure (e.g. beach, dune or shore nourishment)")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At which spatial scale is the intervention implemented?")
    fishery_type: Literal["Commercial","Subsistence","Other","Not specified"] = Field(
        default = "None",
        description="What type of fishery or fishing activity does the intervention pertain to?")
    fishery_size: Literal["Industrial/large-scale","Artisinal/small-scale","Other","Not specified"] = Field(
        default = "None",
        description="The size of the fishery or fishing activity that the intervention pertain to?")
    climatic_impact_driver: Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storm surges","Sea level rise","Climate change in general","Other","Not specified"] = Field(
        default = "None",
        description="What climate impact driver(s) are motivating the adaptation response?")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

class NoIntervention(BaseModel):
    intervention_type: Literal['No intervention'] = Field(..., description="No valid intervention is studied that is relevant for improving climate change adaptation or resilience in fisheries, fishing communities, or the fishing industry")
    reason: str = Field(
        default = "None",
        description="A short (max 50 words) summary: a) describing the intervention, b) justifying your reasoning for identifying this intervention as eligible, and c) justifying your reasoning for classifying it in this category"
    )

# Combine into a Union
InterventionTypeUnion = Annotated[
    Union[Institutional, FisheriesManagement, SocioBehavioural, Economic, NewTechnologies, ClimateServices, HardInfrastructure, SoftInfrastructure, NoIntervention],
    Field(discriminator = "intervention_type")
]

# Final model with discriminator
class InterventionTypeList(BaseModel):
    intervention_type: List[InterventionTypeUnion] = Field(
        default_factory=list,
        description="A list of all the types of interventions (actions, technologies or infrastructure) studied in the article relevant for improving climate change adaptation or resilience in fisheries, fishing communities, or the fishing industry, categorized by type."
    )

# make a parser
InterventionParser = PydanticOutputParser(pydantic_object=InterventionTypeList)




## METHODS INFO
"""
# Study area ---------------------
class CountryName(BaseModel):
    country_name: CountryShortName


class StudyAreas(BaseModel):
    study_areas: List = Field(
        default_factory=list,
        description="A list of the names of the geographical locations as written in the source text (e.g. municipality, country, supra-national region, global)."
    )
    country_names: List[CountryName] = Field(
        default_factory=list,
        description="A list of all the countries corresponding to the geographical locations in short name format (as expected by pydantic CountryShortName). If this information is unavailable, return an empty list."
    )

# make a parser
StudyAreaParser = PydanticOutputParser(pydantic_object=InterventionTypeList)
"""

# Study method -------------------------
class CountryName(BaseModel):
    country_name: CountryShortName


class Experiment(BaseModel):
    method_type: Literal['Experiment'] = Field(..., description="A scientific experiment, including controlled experiments, natural experiments, or field experiments where the researcher manipulates variables.")

class Statistical(BaseModel):
    method_type: Literal['Statistics/Modelling'] = Field(..., description="Quantitative modeling, simulation, or statistical analysis of secondary or pre-existing datasets without new data collection.")
    
class Observation(BaseModel):
    method_type: Literal['Observation'] = Field(..., description="Direct observational methods where researchers record behaviors, patterns, or phenomena without manipulation or direct interaction.")

class Workshop(BaseModel):
    method_type: Literal['Workshop'] = Field(..., description="Group-based participatory or stakeholder engagement activities such as scenario planning, mapping, or visioning workshops.")

class Interview(BaseModel):
    method_type: Literal['Interview'] = Field(..., description="Data collected through structured, semi-structured, or unstructured interviews, often qualitative in nature.")

class Survey(BaseModel):
    method_type: Literal['Survey'] = Field(...,description="Standardized data collection through questionnaires, polls, or forms administered to individuals or groups.")

class Anecdotal(BaseModel):
    method_type: Literal['Anecdotal/Ethnographic'] = Field(..., description="Narratives, field notes, informal conversations, or immersive ethnographic accounts used to describe experiences or contexts.")

class Anecdotal(BaseModel):
    method_type: Literal['Anecdotal/Ethnographic'] = Field(..., description="Narratives, field notes, informal conversations, or immersive ethnographic accounts used to describe experiences or contexts.")

class UnclearMethod(BaseModel):
    method_type: Literal['Unclear'] = Field(..., description="The method is unclear, or insufficient information is availabel to categorize it into another category.")


# Discriminated Union
MethodUnion = Annotated[
    Union[Experiment, Statistical, Observation, Workshop, Interview, Survey, Anecdotal, UnclearMethod],
    Field(discriminator='method_type')
]


class studyMethod(BaseModel):
    method_type: List[MethodUnion] = Field(
        default_factory=list,
        description="A list of all the types of research methodologies used in the article, categorized by type from a predefined list."
    )
    study_areas: List[str] = Field(
        default_factory=list,
        description="A list of the names of the geographical locations where the study was conducted."
    )
    country_names: List[CountryName] = Field(
        default_factory=list,
        description="A list of countries in short name format (as expected by pydantic CountryShortName) where the study was conducted. If this information is unavailable, return an empty list."
    )
    time_scale: Literal["< 1 month","1 month <= 1 year","1 year <= 5 years","5 years <= 10 years", "> 10 years", "Unclear","Not applicable"] = Field(
        default = "None",
        description="What is the length of time between the implementation of the intervention and the end of the study period? In other words, how long was the intervention active before these results were measured? Select the best-fitting category, and if none apply, select 'Not applicable'.")
    spatial_scale: Literal["Local","National","Regional","Global","Not applicable"] = Field(
        default = "None",
        description="At what spatial scale was the study conducted, or at what spatial scale was the data collected? Select the best-fitting category, and if none apply, select 'Not applicable'.")
    method_summary: str = Field(
        default = "None",
        description="Provide a short (< 50 word) summary of the research method used in the study."
    )


# make a parser
StudyMethodParser = PydanticOutputParser(pydantic_object=studyMethod)




## Outcomes --------------------
class StudyResult(BaseModel):
    result_description: str = Field(
        default="None",
        description="A short description of the result."
    )
    result_type: Literal["Ecological","Social","Management","Economic","Not applicable"] = Field(
        default = "None",
        description="Is the result 'Ecological' (i.e. relevant to marine/coastal organisms, habitats, environment), 'Social' (i.e. relevant to humans, human welfare), 'Management' (i.e. pertains to how institutions, policies/practices are managed), or 'Economic' (i.e. relevant to a commerical business, industry, or the economy). Select the best-fitting category, and if none apply, select 'Not applicable'.")
    data_type: Literal["Quantitative","Qualitative","Mixed", "Not applicable"] = Field(
        default = "None",
        description="Is the result 'Quantitative' (i.e. numeric) or 'Qualitative' (i.e. descriptive/observational), or 'Mixed' (i.e. a combination of various quantitative and qualitative metrics all needed to represent the same result). Select the best-fitting category, and if none apply, select 'Not applicable'.")
    result_direction: Literal["Positive","Negative","Neutral","Mixed","Uncertain","Not applicable"] = Field(
        default = "None", #default_factory=str,
        description="The resulting change reported in the result, from a predefined set of allowed categories: 'Positive' (success, improvement, adaptation, increase), 'Negative' (failure, mal-adaptation, decrease), 'Neutral' (no significant change reported, no directionality), 'Mixed' (positive on some aspects, negative on others), 'Uncertain' (results were not clear), 'Not applicable'."
    )


class StudyResultList(BaseModel):
    # Note this field must always be named 'labels'
    study_result: List[StudyResult] = Field(
        default_factory=list,  # Default to an empty list
        description="A list of all study findings/results/outcomes identified as relevant to the intervention."
    )    

# make a parser
ResultParser = PydanticOutputParser(pydantic_object=StudyResultList)





## Enabling conditions -----------------------  


class EnablingConditions(BaseModel):
    procedural_equity_bool: bool = Field(default_factory=False,description= "Was procedural equity considered in the design or implementation of the intervention? Examples of procedural equity include: communities having a voice in the decisionmaking process; inclusive engagement; considerations make for gender equity, social justice, inclusiveness; factoring in of local or indigenous knowledge; participatory approaches.")
    procedural_equity: Literal["Gender equity","Local & indigenous knowledge inclusiveness","Participatory process", "Social justice", "Other","Unclear","Not applicable"] = Field(default = "None", description="If procedural equity was considered in the design or implementation of the intervention, select all relevant categories."
    )
    governance_body: Literal["Community-based","National government","Regional (e.g. RFMOs)","International","Private organizations/companies","Unclear"] = Field(default = "None", description="What institution/institutions are responsible for governing the activities of the intervention? Examples include: communities; municiple governments; national governments; regional institutions (e.g. regional fisheries management organizations (RFMOs)); international/global governance (e.g. international agreements), private organizations/companies."
    )
    rules_of_law: Literal["Law (binding)","Policy/code of conduct (non-binding)", "Informal rule","Unclear"] = Field(default = "None", description="How is the intervention governed?"
    )
    barriers: List[str] = Field(default_factory = list, description = "List of any BARRIERS pertaining to the intervention explicitly mentioned in the article. Barriers CAN be overcome, and can pertain to any stage of the intervention process, including development, planning, design, implementation or operation.")
    limits: List[str] = Field(default_factory = list, description = "List of any LIMITS pertaining to the intervention explicitly mentioned in the article. Limits CANNOT be overcome, and can pertain to any stage of the intervention process, including development, planning, design, implementation or operation.")
    
EnablingConditionsParser = PydanticOutputParser(pydantic_object=EnablingConditions)




############ Write variable definitions ##########################
allVariables = [
    {
        "variable name": "Intervention type",
        "variable faissK": 8,
        "variable question": """
        What types of interventions are studied in the article that are relevant for improving fisheries adaptation (i.e. fisheries, fishing communities, or the fishing industry) to climate change/climatic impact drivers (i.e. marine/coastal environmental pressures/hazards linked to climate change, such as ocean acidification, ocean warming, marine heatwaves, sea level rise, storm surges)? If the information is available, what climatic impact drivers are motivating the adaptation intervention, what type and size of fishery does it pertain to, and what is the spatial scale implementation?
        
        **Examples of relevant types of interventions**: 
        - Institutional (e.g. ocean governance, institutional agreements, marine spatial planning and integrated coastal zone managmeent)
        - Fisheries management (e.g. co-management, adaptive or ecosystem-based management, community-based management)
        - Socio-behavioural (e.g. changing fishing gear/location/species, mobility and relocation, livelihood diversification, human migration or exiting the fishery)
        - Economic (e.g. insurance, finance/market mechanisms, new value chains/markets)")
        - New technologies (e.g. new fishing technologies, biotechnology)
        - Climate services technologies (e.g. disaster response programs, early warning systems, seasonal/dynamic forecasting)
        - Hard infrastructure (e.g. seawalls, artificial reefs, ports or processing infrastructure, gear or vessel modification)
        - Soft infrastructure (e.g. beach, dune or shore nourishment)
        """,
        "variable exclude":"""
        **Filtering Criteria**: 
        - DO NOT include aquaculture or agriculture-related interventions, 
        - DO NOT include purely descriptive studies with no intervention studied, 
        - DO NOT include theoretical/future suggestions without implemented intervention, 
        - DO NOT include interventions addressing overfishing/pollution without mention of climate change or climatic impact drivers""",
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## Task:
                    You are a scientific research assistant, and your task is to answer a question based on information from the following text extracts from a research article. DO NOT MAKE ANYTHING UP. 

                    ## Article text extracts:
                    {context}
                    
                    ## Instructions:
                    In your response, classify the interventions according to the category definitions in the formatting instructions and provide any metadata requested in the output format if available. Wrap the output in `json` tags:
                    {format_instructions}"""
                ),
                ("human", """
                ## Question: 
                {variable question}
                {variable exclude}
                """)
            ]
        ).partial(format_instructions=InterventionParser.get_format_instructions()),
        "variable parser": InterventionParser
    },

    {
        "variable name": "Enabling conditions",
        "variable faissK": 3,
        "variable question": """
        What types of enabling conditions, barriers or limits for the adaptation intervention are explicitly mentioned in the article? Include the following information where available:
        
        - Procedural equity (bool): Was procedural equity considered in the design or implementation of the intervention? 
        - Procedural equity: What type of procedural equity was considered? (e.g. "Gender equity","Local & indigenous knowledge inclusiveness","Participatory process", "Social justice")
        - Governance bodies: What types of institution/institutions are responsible for governing the activities of the intervention? (e.g. "Community-based","National government","Regional (e.g. RFMOs)","International","Private organizations/companies")
        - Rules of law: How is the intervention governed? (i.e. "Law (binding)","Policy/code of conduct (non-binding)", "Informal rule")
        - Are any barriers or limits to the intervention explicitly mentioned? Barriers or limits can pertain to any stage of the intervention process, including development, planning, design, implementation or operation. Examples of barriers or limits include: lack of capital; lack of leadership; lack of legal framework; lack of knowledge. Barriers CAN be overcome, whereas a limit CANNOT be overcome.
        """,
        "variable exclude":"""
        **Filtering Criteria**: 
        - DO NOT infer enabling conditions -- enabling conditions must be clearly stated in the text 
       """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## Task:
                    You are a scientific research assistant, and your task is to answer a question based on information from the following text extracts from a research article. DO NOT MAKE ANYTHING UP. 

                    ## Article text extracts:
                    {context}
                    
                    ## Instructions:
                    In your response, classify the enabling conditions according to the category definitions in the formatting instructions and provide any metadata requested in the output format if available. Wrap the output in `json` tags:
                    {format_instructions}"""
                ),
                ("human", """
                ## Question: 
                {variable question}
                {variable exclude}
                """)
            ]
        ).partial(format_instructions=EnablingConditionsParser.get_format_instructions()),
        "variable parser": EnablingConditionsParser
    },
    
    {
        "variable name": "Outcome",
        "variable faissK": 4,
        "variable question": """
        What are the study's main results/findings pertaining to fisheries climate change adaptation? For each main result, include the following information where available: 
        - A short summary of the result
        - What category the result is most relevant to: "Ecological","Social","Management","Economic","Not applicable"
        - The type of data used to support the result: "Quantitative","Qualitative","Mixed", "Not applicable"
        - Whether the result was "Positive","Negative","Neutral","Mixed","Uncertain","Not applicable" for fisheries adaptation.
        """,
        "variable exclude": None,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## Task:
                    You are a scientific research assistant, and your task is to answer a question based on information from the following text extracts from a research article. DO NOT MAKE ANYTHING UP. 

                    ## Article text extracts:
                    {context}
                    
                    ## Instructions:
                    Format your response according to the format instructions and provide any metadata requested in the output format if available. Wrap the output in `json` tags:
                    {format_instructions}"""
                ),
                ("human", """
                ## Question: 
                {variable question}
                """)
            ]
        ).partial(format_instructions=ResultParser.get_format_instructions()),
        "variable parser": ResultParser
    },
    {
        "variable name": "Study method",
        "variable faissK": 2,
        "variable question": """
        Describe the research methodology used in the study, including the following information where available: 
        - The type of research method (e.g. experimental, statistical analysis, modelling, observation, workshops, interviews, surveys, anecdotes) 
        - Where the study was conducted (the geographical location and country)
        - The time scale/temporal coverage of the study/how long the study was conducted
        - The spatial scale/coverage of the study
        """,
        "variable exclude": None,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## Task:
                    You are a scientific research assistant, and your task is to answer a question based on information from the following text extracts from a research article. DO NOT MAKE ANYTHING UP. 

                    ## Article text extracts:
                    {context}
                    
                    ## Instructions:
                    Format your response according to the format instructions and provide any metadata requested in the output format if available. Wrap the output in `json` tags:
                    {format_instructions}
                    """
                ),
                ("human", """
                ## Question: 
                {variable question}
                """)
            ]
        ).partial(format_instructions=StudyMethodParser.get_format_instructions()),
        "variable parser": StudyMethodParser
    },
] 


# methodsVariables = [
    # {
    #     "variable name": "Study area",
    #     "variable question": "Where was the research study conducted, and in what country?",
    #     "variable exclude": None,
    #     "variable prompt": ChatPromptTemplate.from_messages(
    #         [
    #             (
    #                 "system",
    #                 """
    #                 ## Task:
    #                 You are a scientific research assistant, and your task is to answer a question based on information from the following text extracts from a research article. DO NOT MAKE ANYTHING UP. 

    #                 ## Article text extracts:
    #                 {context}
                    
    #                 ## Instructions:
    #                 Format your response according to the format instructions and provide any metadata requested in the output format if available. Wrap the output in `json` tags:
    #                 {format_instructions}"""
    #             ),
    #             ("human", """
    #             ## Question: 
    #             {variable question}
    #             """)
    #         ]
    #     ).partial(format_instructions=InterventionParser.get_format_instructions())
    # },
    
# ]



##############################################
########### Wrapper  functions ###########
##############################################


async def structure_variable_deepseek(related_documents, variable_question, variable_prompt,variable_parser, variable_exclude=None):
    chain = variable_prompt | model1 | variable_parser
    if variable_exclude:
        result = await chain.ainvoke({
            "context": format_docs(related_documents),
            "variable question": variable_question,
            "variable exclude": variable_exclude,
        })
    else:
        result = await chain.ainvoke({
            "context": format_docs(related_documents),
            "variable question": variable_question,
        })
    return result


## Helper function to identify if all values returned in a dict are None
def all_values_none(obj):
    """
    Recursively checks whether all values in a nested dict or list are the string "None".
    """
    if isinstance(obj, dict):
        return all(all_values_none(v) for v in obj.values())
    elif isinstance(obj, list):
        return all(all_values_none(item) for item in obj)
    else:
        return obj == "None"



async def codeVariable(
    vector_store,
    variable_name,
    variable_question,
    variable_prompt,
    variable_parser,
    variable_exclude=None,
    faissK=4,
    max_retries_error=2,
    max_retries_none=2
):
    related_documents = retrieve_docs(query=variable_question, vector_store=vector_store, faissK=faissK)

    none_attempts = 0
    error_attempts = 0

    while True:
        try:
            answer_structured = await structure_variable_deepseek(
                related_documents,
                variable_question,
                variable_prompt,
                variable_parser,
                variable_exclude=variable_exclude
            )
            answer_dict = answer_structured.model_dump()
            answer_dict['source text'] = [doc.page_content for doc in related_documents]
            # need to correct to: **************************
            # answer_dict[f'{variable_name} source text'] = [doc.page_content for doc in related_documents]

            # Retry if all values are None
            if all_values_none(answer_dict):
                none_attempts += 1
                if none_attempts >= max_retries_none:
                    raise ValueError("Max retries exceeded: All values are 'None'")
                continue  # Retry
            return answer_dict

        except Exception as e:
            error_attempts += 1
            if error_attempts >= max_retries_error:
                return {
                    f"{variable_name} error_message": str(e),
                    f"{variable_name} source text": [doc.page_content for doc in related_documents]
                }


"""
async def codeVariable(vector_store, variable_name, variable_question, variable_prompt,variable_parser, variable_exclude=None, faissK=4, max_retries = 2):
    
    related_documents = retrieve_docs(query = variable_question, vector_store=vector_store, faissK=faissK)

    # Try several times because of randomness introduced by temperature, sometimes the model results don't conform
    for attempt in range(max_retries):
        try:
            answer_structured = await structure_variable_deepseek(related_documents, variable_question, variable_prompt,variable_parser, variable_exclude=variable_exclude)
            answer_dict = answer_structured.model_dump() #.dict()

            answer_dict['source text'] = [doc.page_content for doc in related_documents]

            # Raise error if output is "None" at all levels
            if all_values_none(answer_dict):
                raise ValueError("All values in the model output are 'None'. Retrying...")
                
            return answer_dict
        except Exception as e:
            if attempt == max_retries - 1:
                answer_dict = {
                    f"{variable_name} error_message": str(e),
                    f"{variable_name} source text": [doc.page_content for doc in related_documents]
                }
                return answer_dict


"""


### STEP 3: WRAP ALL FUNCTIONS TOGETHER ---------------------


### Wrap all the functions together #####
async def code_pdf_async(file, faiss_directory, answer_directory):
    # RAG AI functions
    files = os.listdir(pdfs_directory)
    pdf_path = [f for f in files if file+'_' in f]
    pdf_path = pdf_path[0]
    pdf_path = os.path.join(pdfs_directory, pdf_path)
    faiss_path_methods = os.path.join(faiss_directory, f"{file}_methods.faiss")
    faiss_path = os.path.join(faiss_directory, f"{file}.faiss")

    vector_store_methods = load_vectorstore(faiss_path_methods, embeddings)
    vector_store = load_vectorstore(faiss_path, embeddings)

    if vector_store_methods:
        print("loading methods vectorstore")

    if vector_store:
        print("loading vectorstore")
    
    if vector_store is None:
        methods_text = identifyMethods(pdf_path)
        if methods_text:
            chunked_methods = split_text_unstructured([methods_text], chunk_size, chunk_overlap)
            vector_store_methods = get_vectorstore([x.page_content for x in chunked_methods], embeddings)
            vector_store_methods.save_local(faiss_path_methods)
            print(f"saved : {faiss_path_methods}")

        allText = extract_text_excluding_sections_terminal(pdf_path, exclude_sections=[])
        if allText:
            chunked = split_text_unstructured([allText], chunk_size, chunk_overlap)
        else:
            text = load_pdf(pdf_path)
            chunked = split_text(text, chunk_size, chunk_overlap)
            
        vector_store = get_vectorstore([x.page_content for x in chunked], embeddings)
        vector_store.save_local(faiss_path)
        print(f"saved : {faiss_path}")
  
    ## Code all variables
    codeResults = []
    for variable in allVariables:
        variable_name = variable.get("variable name")
        variable_question = variable.get("variable question")
        variable_prompt = variable.get("variable prompt")
        variable_parser = variable.get("variable parser")
        variable_exclude = variable.get("variable exclude")
        variable_faissK = variable.get("variable faissK")

        if vector_store_methods and variable_name == "Study method":
            answer_dict = await codeVariable(vector_store_methods, variable_name, variable_question, variable_prompt,variable_parser, variable_exclude, variable_faissK, max_retries_error = codeMaxRetries)
            
        else:
            answer_dict = await codeVariable(vector_store, variable_name, variable_question, variable_prompt,variable_parser, variable_exclude, variable_faissK, max_retries_error = codeMaxRetries)

        
        codeResults.append(answer_dict)
        await asyncio.sleep(2)

    result = {'id': int(file), 'coding response': [codeResults]} # removed [codeResults]

    # Explicitly delete large objects and force GC
    del vector_store
    del vector_store_methods
        
    # Save to disk
    with open(os.path.join(answer_directory, f"{file}_code.txt"), 'w') as f:
        json.dump(result, f)

    gc.collect()
    await asyncio.sleep(2)

    return file  # Just for progress reporting


# ----- Throttled async processor -----
async def code_with_throttle(file, semaphore, failed_ids):
    async with semaphore:
        try:
            await asyncio.sleep(2)
            await code_pdf_async(file, faiss_directory, answer_directory)
        except Exception as e:
            msg = f"[ERROR] ID {file} failed with error: {e}"
            print(msg)
            log_event(msg)
            failed_ids.append(file)


# ----- Utils -----
# Function to retry failed IDs from previous batches before progressing
def load_failed_ids_from_log(log_path):
    failed_ids = set()
    if not os.path.exists(log_path):
        print(f"[INFO] No log file found at {log_path}")
        return failed_ids

    try:
        with open(log_path, "r") as f:
            for line in f:
                if "Failed IDs:" in line:
                    match = re.search(r"Failed IDs: \[([^\]]+)\]", line)
                    if match:
                        ids_str = match.group(1)
                        ids = [int(id_str.strip()) for id_str in ids_str.split(",") if id_str.strip().isdigit()]
                        failed_ids.update(ids)
    except Exception as e:
        print(f"[ERROR] Could not parse log file: {e}")
    
    print(f"[INFO] Loaded {len(failed_ids)} previously failed IDs from log.")
    return failed_ids



def load_checkpoint():
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, "r") as f:
            return set(json.load(f))
    return set()


def save_checkpoint(completed_batches):
    with open(checkpoint_path, "w") as f:
        json.dump(list(completed_batches), f)


def log_event(message):
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {message}\n")





def process_pdf(file):
    try:
        # RAG AI functions
        files = os.listdir(pdfs_directory)
        pdf_path = [f for f in files if file+'_' in f]
        pdf_path = pdf_path[0]
        pdf_path = os.path.join(pdfs_directory, pdf_path)
        faiss_path_methods = os.path.join(faiss_directory, f"{file}_methods.faiss")
        faiss_path = os.path.join(faiss_directory, f"{file}.faiss")

        vector_store_methods = load_vectorstore(faiss_path_methods, embeddings)
        vector_store = load_vectorstore(faiss_path, embeddings)

        if vector_store_methods:
            print("loading methods vectorstore")

        if vector_store:
            print("loading vectorstore")
        
        if vector_store is None:
            methods_text = identifyMethods(pdf_path)
            if methods_text:
                chunked_methods = split_text_unstructured([methods_text])
                vector_store_methods = get_vectorstore([x.page_content for x in chunked_methods], embeddings)
                vector_store_methods.save_local(faiss_path_methods)
                print(f"saved : {faiss_path_methods}")

            allText = extract_text_excluding_sections_terminal(pdf_path, exclude_sections=[])
            if allText:
                chunked = split_text_unstructured([allText])
            else:
                text = load_pdf(pdf_path)
                chunked = split_text(text)
                
            vector_store = get_vectorstore([x.page_content for x in chunked], embeddings)
            vector_store.save_local(faiss_path)
            print(f"saved : {faiss_path}")
      
        ## Code all variables
        codeResults = []
        for variable in allVariables:
            variable_name = variable.get("variable name")
            variable_question = variable.get("variable question")
            variable_prompt = variable.get("variable prompt")
            variable_exclude = variable.get("variable exclude")

            if vector_store_methods and variable_name == "Study method":
                answer_dict = codeVariable(vector_store_methods, variable_name, variable_question, 
                                                 variable_prompt, variable_exclude, faissK, max_retries = codeMaxRetries)
            else:
    
                answer_dict = codeVariable(vector_store, variable_name, variable_question, 
                                                 variable_prompt, variable_exclude, faissK, max_retries_error = codeMaxRetries)
    
            
            codeResults.append(answer_dict)
            time.sleep(2)

        result = {'id': int(file), 'coding response': [codeResults]}

        # Explicitly delete large objects and force GC
        del vector_store
        del vector_store_methods
        
    except Exception as e:
        result = {
            'response_status': 'error',
            'id': int(file),
            'error': str(e)
        }

    # Save to disk
    with open(os.path.join(answer_directory, f"{file}_code.txt"), 'w') as f:
        json.dump(result, f)

    gc.collect()
    time.sleep(2)

    return file  # Just for progress reporting


    
    

