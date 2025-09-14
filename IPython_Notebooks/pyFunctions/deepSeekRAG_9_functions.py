


## STEP 0: DEFINE SCHEMAS FOR MULTIPLE CHOICE LABELS

## Screening question
class SafeFish(BaseModel):
    include: bool = Field(default=True,description= "Does this research study a fisheries climate change adaptation action? If yes, reply True and if no, reply False. If the information is unavailable or unclear, reply with True.")


SafeFishParser = PydanticOutputParser(pydantic_object=SafeFish)

SafeFish_dict = {
        "variable name": "safe fish",
        "variable faissK": 10,
        "variable question": """
        **Decide whether the article meets the following inclusion criteria (True/False)**: 
        
        **INCLUSION CRITERIA**
        To be included, a study must meet ALL of the following criteria:
        1) The study researches a *climate change adaptation action*. 
        2) The climate change adaptation action MUST aim to help *marine fisheries* adapt to climate change, and/or its associated impacts.
        3) The study's *outcomes* result from the adaptation action. This includes outcomes on effectiveness (e.g. adaptation, success, mal-adaptation, failure), co-benefits, dis-benefits, side-effects or trade-offs, costs, or impacts. 

        Use the following term definitions to guide your interpretation: 
        - climate change: climate change, including 'climatic impact drivers': environmental pressures/hazards caused/exacerbated by climate change. These include, for example: ocean acidification, ocean warming, marine heatwaves, sea level rise, storm surges, extreme weather, extreme climate variability (e.g. increased frequency/intensity of ENSO), Harmful Algal Blooms (HABs).
        - adaptation: the process of adjustment to actual or expected climate and its effects, in order to moderate harm or exploit beneficial opportunities. Adaptation outcomes can be ecological, economic or social. 
        - action: any action. The definition of 'action' is broad, and includes institutional actions (e.g. governance, laws, policy, practice, fisheries management, ecosystem-based management, strategy), economic mechanisms (e.g. finance, credit, financial markets, ownership schemes, value chains), socio-behavioural actions (i.e. actions, responses or current practices taken voluntarily by individual fishers, households, or communities to adapt their behavior or livelihoods, for example: changing fishing practices, migration, relocation, livelihood diversification), built infrastructure (e.g. sea walls, dykes), nature-based coastal protection (e.g. coastal ecosystem restoration for storm protection, shore nourishment), technology (e.g. early warning systems, new fishing technologies) 
        - fisheries: any marine fishery or fishing practice (commercial, subsistence, artisanal), including: fishers, fishing community, commercially fished species (e.g. population health, stock size, landings, catch), or fishing business. 
        - outcome: a result or finding derived from the study conducted by the authors. Outcomes can be qualitative (descriptive, anecdotal, observation) or quantitative.  
        

        INCLUDED EXAMPLES (i.e. response: {{'include': True}}):
        - A case study of how fishing communities are adapting to climate change through their current practices 
        - A qualitative analysis of the effectiveness of institutional actions directly relevant to fisheries (e.g. fisheries management, ocean governance with fisheries implications, improving resilience of marine natural resources to climate change)
        - analyses (including descriptive/qualitative analyses) of the impacts of existing management policies/laws/documents
        - A study modelling outcomes (e.g. income loss) of adaptive actions 


        EXCLUDED EXAMPLES (i.e. response: {{'include': False}}): 
        - *the adaptation action is NOT implemented*. For example:
            - vulnerability assessments
            - planning or design of an action
            - action recommendation with no implementation
        - Coastal/marine climate change adaptation with NO fishery relevance (e.g. aquaculture, mariculture, coastal community adaptation with no fishery).
        - actions adapting to other pressures (e.g. overfishing/pollution) without mention of climate change or a climatic impact driver.
        - freshwater fisheries
        - Policy/legal summaries with no analysis of outcomes
        """,

        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    
                    ## INSTRUCTIONS:
                    - DO NOT MAKE ANYTHING UP.
                    - DO NOT include <think> tags or any explanations in your response.
                    - DO NOT explain your reasoning.
                    - Output ONLY a single valid JSON object that conforms to the schema.
                    - Do NOT add commentary or wrap your output with XML or markdown tags.
                    - Start your response with '{{` and end with  `}}' — nothing else.

                    - **Wrap the output in the following `json` tags, and adhere STRICTLY to this schema:**
                    
                    {format_instructions}

                    ## Here are some examples of responses:
                    
                    example_text: "In this article, we compare four fishing-based areas in Thailand and the Philippines to examine if and how small-scale fishing communities are able to escape marginalization. Three questions guide our inquiry: (i) How have fishing communities been affected by overfishing, climate change and other pressures? (ii) What adaptive strategies have these communities employed to mitigate socio-economic and environmental challenges? "
                    example_assistant: {{'include': True}} 
                    
                    --

                    example_text: "priorities for adaptation actions. The community-identiﬁed and selected actions that were intended to be implemented by the community and/or with the support of local organizations and government"
                    example_assistant: {{'include': True}} 
                    
                    --

                    example_text: " This article examines recent legal developments to summarize the United States’ current policy approach to climate change adaptation, especially as such developments affect marine sector."
                    example_assistant: {{'include': False}} 
                    
                    ---
                    
                    example_text: "Many municipalities undertake actions individually and/or collectively, in cooperation with central administrations, regional authorities, the private sector, and other municipalities (both nationally and internationally). This paper aims to examine how they use transnational municipal networks (TMNs) as a tool for cooperation that supports marine governance in the context of climate change adaptation and mitigation. "
                    example_assistant: {{'include': False}}
                    
                    --

                    example_text:"Faced with rising seas, eroding coastlines, and depleting fish stocks and biodiversity, Guet Ndarians abroad and at home respond to the ensuing degradation of livelihoods and the destruction of homes by altering their mobility patterns"
                    example_assistant: {{'include': True}}
                    
                    --

                    example_text: "This article examines recent legal developments to summarize the United States’ current policy approach to climate change adaptation, especially as such developments affect marine sector. This includes regulations necessary to make the Nation’s watersheds, natural resources, and ecosystems, and the communities and economies that depend on them, more resilient in the face of a changing climate"
                    example_assistant: {{'include': True}}

                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=SafeFishParser.get_format_instructions()),
        "variable parser": SafeFishParser
    }



## ORO type -- Intervention institutional -------------------------------
class InterventionInstitutional(BaseModel):
    intervention_institutional: List[Literal['Institutional','Fisheries management','Socio-behavioural','Economic']] = Field(
        default_factory = list, description="All types of socio-institutional adaptation actions studied in the article, selected from a list of pre-defined allowed values: ['Institutional','Fisheries management','Socio-behavioural','Economic']")


InterventionInstitutionalParser = PydanticOutputParser(pydantic_object=InterventionInstitutional)

InterventionInstiutional_dict = {
        "variable name": "ORO_institutional",
        "variable faissK": 10,
        "variable question": """
        Respond in structured JSON output schema (defined in 'Instructions') with a List of all relevant SOCIO-INSTITUTIONAL actions/strategies studied in the article. List elements must be selected from the **allowed values** ['Institutional','Fisheries management','Socio-behavioural','Economic'] defined below.  
        
        All socio-institutional actions/strategies MUST aim help marine fisheries adapt to climate change. In general, actions relevant to changes in POLICY, PRACTICE, MANAGEMENT, LAW, ECONOMICS/FINANCE or SOCIAL BEHAVIOUR will fall into one of these categories. If no eligible socio-institutional actions are identified, respond with an empty list.
        
        **Allowed values definitions**:
        
        - "Institutional": Changes to institutional structures, policies, laws, or governance frameworks that support climate adaptation in marine fisheries. These are typically top-down actions by governments or institutions. Examples include: new or reformed ocean governance frameworks, international or inter-institutional agreements, marine spatial planning (MSP), integrated coastal zone management (ICZM), legal reforms or environmental legislation relevant to fisheries.

        - "Fisheries management": Changes to how fisheries are managed or fishing is conducted, often led by management authorities but sometimes involving community participation. These actions directly regulate or influence fishing activity. Examples include: fisheries closures, co-management; community-based management; adaptive management; ecosystem-based fisheries management; quotas, seasonal closures, or gear restrictions; population assessments or fish stocking; restoration of fish habitats

        - "Socio-behavioural": Actions (including current practices) taken voluntarily by individual fishers, households, or communities to adapt their behavior or livelihoods in response to climate change impacts. These are bottom-up, behavioral or social responses rather than imposed regulations. Examples include: switching fishing gear, target species, or fishing grounds; adjusting the timing or frequency of fishing; seasonal mobility or relocation to follow fish; livelihood diversification (e.g. fish processing, aquaculture, tourism); human migration or planned retreat from coastal areas; voluntarily exiting the fishery; participating in community knowledge-sharing or adaptive learning

        - "Economic": Actions that involve the use of financial, market-based, or economic instruments to support adaptation in marine fisheries. These strategies focus on monetary, market, or financial aspects. Examples include: insurance programs for fishers; access to finance or credit; market-based mechanisms (e.g. carbon credits, fishing rights); alternative or value-added seafood markets; financial incentives or compensation schemes; economic diversification related to fisheries (e.g. eco-tourism, new product development)
             

        Note: Use the examples provided in the definitions to guide your inclusion decisions. If no eligible socio-institutional action is identified, respond with an empty list.


        ** Filtering Criteria **
        ALL ACTIONS MUST aim to help **marine fisheries** (including fishing communities, fishers, fishing industries, commercially fished populations) **adapt** to **climate change** (including marine/coastal environmental pressures/hazards linked to climate change, such as ocean acidification, ocean warming, marine heatwaves, sea level rise, storm surges, extreme weather) 
    
        """,
        "variable exclude":"""
        EXCLUDE: 
        - Adaptation actions that are NOT socio-institutional**. For example,  EXCLUDE: built infrastructure (e.g. sea walls, dykes), nature-based coastal protection (e.g. coastal ecosystem restoration for storm protection, shore nourishment, nature-based approaches), technology (e.g. early warning systems, new fishing technologies) 
        - aquaculture, freshwater fishery, or agriculture-related actions, 
        - purely descriptive studies
        - theoretical/future suggestions without implemented action, 
        - actions addressing overfishing/pollution without mention of climate change or climatic impact drivers
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible.
                    - If no eligible socio-institutional adaptation actions are identified, respond with an empty list.
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    ## EXAMPLE RESPONSES:
                    - A fisher changes target species or fishing grounds due to warming waters ➤ {{"intervention_institutional": ["Socio-behavioural"]}}
                    - A policy bans fishing in certain areas ➤ {{"intervention_institutional": ["Fisheries management"]}}
                    - low cost intensive monitoring and rapid flexible management to cope with climate impacts ➤ {{"intervention_institutional": ["Fisheries management"]}}
                    - Stock rebuilding as a buffer against climate change ➤ {{"intervention_institutional": ["Fisheries management"]}}
                    - A community starts migrating away from the coast ➤ {{"intervention_institutional": ["Socio-behavioural"]}}
                    - The article describes how fishing communities are adapting to climate change through their current practices ➤ {{"intervention_institutional": ["Socio-behavioural"]}}
                    - A government creates a new integrated coastal management plan ➤ {{"intervention_institutional": ["Institutional"]}}
                    - Fishers receive subsidies to offset losses ➤ {{"intervention_institutional": ["Economic"]}}
                    - simultaneous ownership of fishing fleet and processing factories ➤ {{"intervention_institutional": ["Economic"]}}
                    - Document analysis of recent Research Priorities from the major fisheries research funding body for reference to climate change related themes, and the number of subsequently funded projects which considered climate change or related topics ➤ {{"intervention_institutional": ["Economic"]}}
                    - A study of trends in grant/funding allocations to support the ﬁsheries sector ➤ {{"intervention_institutional": ["Institutional", "Economic"]}}

                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=InterventionInstitutionalParser.get_format_instructions()),
        "variable parser": InterventionInstitutionalParser
    }



## ORO type -- Intervention Technology -------------------------------
class InterventionTechnology(BaseModel):
    intervention_technology: List[Literal['Disaster response technologies','Fishing technologies']] = Field(
        default_factory = list, description="All types of technologies for fisheries climate change adaptation studied in the article, selected from a list of pre-defined allowed values: ['Disaster response technologies','Fishing technologies']")


InterventionTechnologyParser = PydanticOutputParser(pydantic_object=InterventionTechnology)

InterventionTechnology_dict = {
        "variable name": "ORO_technology",
        "variable faissK": 10,
        "variable question": """
        Respond with a List of all the unique types of TECHNOLOGIES studied in the article that aim to help marine fisheries adapt to climate change. List elements must be selected from the allowed values defined below. If no eligible technologies are identified, respond with an empty list.
        
        **Allowed value definitions**:
        - "Disaster response technologies": Technologies for responding to coastal climate hazards (e.g. early warning systems, seasonal/dynamic forecasting, technology to cope with extreme weather). This does NOT include 'ecosystem monitoring' which falls under fisheries management.
        - "Fishing technologies": New fishing technologies (e.g. new fishing technologies, biotechnology)

        Note: Use the examples provided in the definitions to guide your inclusion decisions. If no eligible technology is identified, respond with an empty list.

        ** Filtering Criteria **
        ALL TECHNOLOGIES MUST aim to help **marine fisheries** (including fishing communities, fishers, fishing industries, commercially fished populations) **adapt** to **climate change** (including marine/coastal environmental pressures/hazards linked to climate change, such as ocean acidification, ocean warming, marine heatwaves, sea level rise, storm surges, extreme weather) 
        """,
        "variable exclude":"""
        EXCLUDE: 
        - **Adaptation actions that are NOT TECHNOLOGIES**. For example, EXCLUDE: intitutional actions (e.g. governance, laws, policy, practice, fisheries management, ecosystem-based management, strategy), economic mechanisms (e.g. finance, credit, financial markets, ownership schemes, value chains), socio-behavioural actions (i.e. actions, responses or current practices taken voluntarily by individual fishers, households, or communities to adapt their behavior or livelihoods, for example: changing fishing practices, migration, relocation, livelihood diversification), built infrastructure (e.g. sea walls, dykes), nature-based coastal protection (e.g. coastal ecosystem restoration for storm protection, shore nourishment) 
        - General policies for climate resilience to both coastal inundation and climate impacts on ﬁsheries but NO TECHNOLOGY IS MENTIONED
        - aquaculture, freshwater fishery, or agriculture-related actions, 
        - purely descriptive studies with no action studied, 
        - theoretical/future suggestions without implemented action, 
        - actions addressing overfishing/pollution without mention of climate change or climatic impact drivers
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - If no eligible technologies are identified, respond with an empty list.
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "Fishers have had a variety of adaptation strategies to cope with the decreased catch and extreme weather (see Table 2). At the individual and household levels, they employ various types of technology to survive in extreme weather and compete with other fishers."

                    example_assistant: {{"intervention_technology": ['Disaster response technologies']}}
                    Reason: **Technology** was mentioned as being employed to help *fishers* adapt to extreme weather (a coastal hazard linked to climate change). 

                    --

                    example_text: "climate change adaptation activities, including projects using biodiversity for ecosystem services as part of Ecosystem-Based Adaptation (EbA)"
                    example_assistant: {{"intervention_technology": []}}
                    Reason: This is a socio-institutional action and does NOT classify as a technology.

                    example_text:" The main driver of anchovy stock variability is the El Niño Southern Oscillation (ENSO), and 
three extreme ENSO warm events were recorded in 1972–1973, 1983–1984 and 1997–1998. This study investigates the evolution of coping strategies developed by the anchovy fisheries to deal with climate variability and extreme ENSO events. Results showed eight coping strategies to reduce impacts on the fishery. These included: decentralized installation of anchovy processing factories; simultaneous ownership of fishing fleet and processing factories; low cost intensive monitoring; rapid flexible management; reduction of fishmeal price uncertainty through controlled production based on market demand; and decoupling of fishmeal prices from those of other protein-rich feed substitutes like soybean. "
                    example_assistant: {{"intervention_technology": []}}
                    Reason: Although these adaptation actions respond to extreme events/coastal hazards, they are NOT technologies -- they are better classified as 'socio-institutional' and 'infrastructure'.

                    --

                    example_text: "Over the longer term, fishermen and the fishing industry more broadly will face the challenges and costs of adapting processing and fishing infrastructure as well as fishing gear to take advantage of the opportunities provided by new species."
                    example_assistant: {{"intervention_technology": []}}
                    Reason: The statement is speculative and does not indicate that the techonology (new fishing gear) was implemented.
                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=InterventionTechnologyParser.get_format_instructions()),
        "variable parser": InterventionTechnologyParser
    }



## ORO type -- Intervention Infrastructure -------------------------------
class InterventionInfrastructure(BaseModel):
    intervention_infrastructure: List[Literal['Built infrastructure','Nature-based']] = Field(
        default_factory = list, description="All types of infrastructure for fisheries climate change adaptation studied in the article, selected from a list of pre-defined allowed values: ['Built infrastructure','Nature-based']")


InterventionInfrastructureParser = PydanticOutputParser(pydantic_object=InterventionInfrastructure)

InterventionInfrastructure_dict = {
        "variable name": "ORO_infrastructure",
        "variable faissK": 10,
        "variable question": """
        Respond with a List of all the unique types of INFRASTRUCTURE implemented to help marine/coastal fisheries/fishing communities adapt to climate change. List elements must be selected from the allowed values defined below. If no eligible infrastructure is identified, respond with an empty list. 
        
        **Allowed value definitions**:
        - "Built infrastructure": Hard or physical built infrastructure (e.g. seawalls, artificial reefs, ports, processing infrastructure, fleet and processing facilities)
        - "Nature-based": Nature-based solutions which work with natural processes to enhance natural coastal defenses against storms and erosion (e.g. beach, dune or shore nourishment, restoring coastal ecosystems)
        
        Note: Use the examples provided in the definitions to guide your inclusion decisions. If no eligible infrastructure is identified, respond with an empty list.

        ** Filtering Criteria **
        - ALL INFRASTRUCTURE MUST aim to help **marine fisheries** (including fishing communities, fishers, fishing industries, commercially fished populations) **adapt** to **climate change** (including marine/coastal environmental pressures/hazards linked to climate change, such as ocean acidification, ocean warming, marine heatwaves, sea level rise, storm surges, extreme weather) 

        """,
        "variable exclude":"""
        EXCLUDE: 
        - **adaptation actions that are NOT INFRASTRUCTURE**. For EXCLUDE: institutional actions (e.g. governance, laws, policy, practice, fisheries management, ecosystem-based management, strategy), economic mechanisms (e.g. finance, credit, financial markets, ownership schemes, value chains), socio-behavioural actions (i.e. actions, responses or current practices taken voluntarily by individual fishers, households, or communities to adapt their behavior or livelihoods, for example: changing fishing practices, migration, relocation, livelihood diversification), technology (e.g. early warning systems, new fishing technologies) 
        - coastal restoration/conservation if coastal hazard prevention/climate change (e.g. storm, erosion, sea level rise) is NOT mentioned.
        - Restoration activities under the purview of fisheries management to improve the health of fish stocks but are not aimed to protect coasts (e.g. fish habitat restoration)
        - aquaculture, freshwater fishery, or agriculture-related actions, 
        - purely descriptive studies -- the findings do not result from the implementation of an adaptation action 
        - theoretical/future suggestions without implemented action, 
        - actions addressing overfishing/pollution without mention of climate change or climatic impact drivers
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - If no eligible infrastructure is identified, respond with an empty list. 
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "This study investigates the evolution of coping strategies developed by the anchovy fisheries to deal with climate variability and extreme ENSO events. Results showed eight coping strategies to reduce impacts on the fishery. These included: use of low-cost unloading facilities."
                    example_assistant: {{"intervention_infrastructure": ['Built infrastructure']}}
                    Reason: Climate change causes increasingly extreme ENSO events, affecting fishers. Low-cost facilities consitutes the use of a new built infrastructure to improve adaptation.

                    example_text: "Successful initiatives have included disaster risk reduction measures, mangrove planting, and setting up fish sanctuaries and oyster cultures. "
                    example_assistant:  {{"intervention_infrastructure": ['Nature-based']}}
                    Reason: Mangroves attenuate storm surges and therefore planting or restoring mangroves to reduce coastal hazard risk in the context of fisheries adaptation is Nature-based.

                    --

                    example_text: "Stock rebuilding, ecosystem-based management and habitat restoration as a buffer against climate change"
                    example_assistant: {{"intervention_infrastructure": []}}
                    Reason: These actions fall under 'Fisheries management' NOT built infrastructure or nature-based for coastal protection. 

                    --

                    example_text: "Over the longer term, fishermen and the fishing industry more broadly will face the challenges and costs of adapting processing and fishing infrastructure as well as fishing gear to take advantage of the opportunities provided by new species."
                    example_assistant: {{"intervention_infrastructure": []}}
                    Reason: The statement is speculative and does not indicate that the infrastructure (processing and fishing infrastructure) was implemented.

                    --

                    example_text: "a broad-based outcome, including material goals such as economic yield, food supplies, and employ-ment, as well as nonmaterial aspects such as safe, decent, and nondiscriminatory work conditions. It also encompasses the preservation of marine and coastal ecosystems (International Labour Organi-', 'the heritage of the fishing community (i.e., the built environment) is protected and that 2) access to affordable housing is provided. These measures, if implemented, should caution against overdevelopment and property value inflation at the expense of local residents."
                    example_assistant: {{"intervention_infrastructure": []}}
                    Reason: Vague references to the built environment, ecosystem health and socio-ecological ecosystems is insufficient evidence for classification as infrastructure implemented to help marine/coastal fisheries/fishing communities adapt to climate change. 
                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=InterventionInfrastructureParser.get_format_instructions()),
        "variable parser": InterventionInfrastructureParser
    }


## Climate impact driver -------------------------------
class ClimaticImpactDriver(BaseModel):
    climatic_impact_driver: List[Literal["Ocean acidification","Ocean warming","Marine heatwaves","Storms/extreme weather","Sea level rise","Climate change in general"]] = Field(
        default_factory = list, description="A list of the types of climatic impact drivers motivating the need for fisheries adaptation studied in the article, selected from a list of pre-defined allowed values: ['Ocean acidification','Ocean warming','Marine heatwaves','Storms/extreme weather','Sea level rise','Climate change in general']")


ClimaticImpactDriverParser = PydanticOutputParser(pydantic_object=ClimaticImpactDriver)

ClimaticImpactDriver_dict = {
        "variable name": "climatic impact driver",
        "variable faissK": 5,
        "variable question": """
        Respond with a List of all the unique types of CLIMATIC IMPACT DRIVERS that are motivating the fisheries adaptation response. List elements must be selected from the allowed values defined below. 
        
        **Allowed value definitions**:
        - "Ocean acidification": A chemical change in seawater caused by the ocean absorbing atmospheric CO₂, which lowers the pH and reduces carbonate availability, affecting organisms like shellfish and corals that rely on calcium carbonate.
        - "Ocean warming": Long-term increases in average ocean temperatures over time due to global climate change. This affects species distributions, metabolism, and ecosystem dynamics.
        - "Marine heatwaves": Short-term, intense periods of abnormally high ocean temperatures lasting days to months. 
        - "Storms/extreme weather": High-intensity, short-duration weather events such as hurricanes, cyclones, or heavy rainfall, often intensified by climate change. These can also be related to changes in climate modes such as ENSO/El Nino/La Nina. 
        - "Sea level rise": The gradual increase in the average height of the ocean surface.
        - "Climate change in general": Broad references to global climate change without specifying particular drivers (e.g., warming, acidification, sea level rise). Used when the text refers to climate change impacts without identifying a specific mechanism.

        """,
        "variable exclude":"""
        ** Filtering Criteria **
        EXCLUDE: 
        - aquaculture or agriculture-related (not fisheries) 
        - purely descriptive studies or theoretical/future suggestions (no adaptation response studied)
        - adaptation is NOT responding to climate change (e.g. overfishing/pollution without mention of climate change or climatic impact drivers)
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - All category names should be unique
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "Through a survey of 393 fishing-based households and semi-structured interviews with 59 key informants we find an uneven mixture of drivers, strategies and impacts. Respondents varyingly attribute declining fish catch to illegal fishing, overfishing, population increase, climate change and pollution."
                    example_assistant: {{"climatic_impact_driver": ['Climate change in general']}}
                    Reason: Climate change was mentioned as motivating the fishers to adapt, but no specific mechanisms were identified

                    example_text: "Fishers have had a variety of adaptation strategies to cope with the decreased catch and extreme weather (see Table 2)."
                    example_assistant: {{"climatic_impact_driver": ["Storms/extreme weather"]}}
                    Reason: Extreme weather was mentioned as motivating the fishers to adapt.
                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=ClimaticImpactDriverParser.get_format_instructions()),
        "variable parser": ClimaticImpactDriverParser
    }



## Study Method -------------------------------
class StudyMethod(BaseModel):
    study_method: List[Literal['Experiment','Quantitative analysis','Qualitative analysis', 'Ecological observation', 'Workshop','Interview','Survey','Case study/anecdotal']] = Field(
        default_factory = list, description="A list of the types of study methods used in the study, selected from a list of pre-defined allowed values: ['Experiment','Quantitative analysis','Qualitative analysis', 'Ecological observation', 'Workshop','Interview','Survey','Case study/anecdotal']")


StudyMethodParser = PydanticOutputParser(pydantic_object=StudyMethod)

StudyMethod_dict = {
        "variable name": "study method",
        "variable faissK": 5,
        "variable question": """
        Respond with a List of the types of STUDY METHODS the authors used to conduct their research. List elements must be selected from the allowed values defined below. 
        
        **Allowed value definitions**:
        -'Experiment': A scientific experiment, including controlled experiments, natural experiments, or field experiments where the researcher manipulates variables.
        -'Quantitative analysis': Quantitative analysis, statistical modelling, modeling, simulation, or statistical analysis of secondary or pre-existing datasets without new data collection.
        - 'Qualitative analysis': Descriptive analysis/interpretation of external data (e.g. critical analyses of legislative documents, policy documents)
        -'Ecological observation': Ecological research methods that observe the environment (i.e. field observations/surveys). This includes observations of species, the environment or any other aspect of biodiversity (including: genetic composition, species populations, species traits, community composition, ecosystem structure, and ecosystem function).
        -'Workshop': Group-based participatory or stakeholder engagement activities such as scenario planning, mapping, or visioning workshops.
        -'Interview': Data collected through structured, semi-structured, or unstructured interviews, often qualitative in nature.
        -'Survey': Social science research method involving standardized data collection through questionnaires, polls, or forms administered to individuals or groups. This does NOT include ecological field surveys which are categorized as 'Ecological observation'
        -'Case study/anecdotal': Narratives, field notes, informal conversations, or immersive ethnographic accounts/observations used to describe experiences or contexts.

        ** Filtering Criteria **
        Inclusion:
        - **ONLY INCLUDE methods that were directly implemented by the authors as part of the current study**. This is often indicated by language such as: '<study method> was conducted/performed/carried out/etc.', 'we conducted/performed/carried out/etc. <study method>'

        """,
        "variable exclude":"""
        Exclusion:
        - DO NOT include methods mentioned from other studies, background literature, or prior work cited in the article.
        - DO NOT include methods mentioned as examples, comparisons, or findings from other studies
        - DO NOT include citations or descriptions of other research unless the method was re-used or replicated in this study
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - All category names should be unique
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "Through a survey of 393 fishing-based households and semi-structured interviews with 59 key informants we find an uneven mixture of drivers, strategies and impacts. Respondents varyingly attribute declining fish catch to illegal fishing, overfishing, population increase, climate change and pollution."
                    example_assistant: {{"study_method": ['Survey']}}
                    Reason: A survey is conducted as a part of the current study (there is no indication (e.g. citation) that this survey was conducted in another study)

                    --

                    example_text: "This study considers recent trends in ODA allocations to support the fisheries sector in the 146 ODA recipient countries and territories around the world– defined according to per capita income levels"
                    example_assistant: {{"study_method": ['Quantitative analysis']}}
                    Reason: A trends analysis is quantitative

                    --

                    

                    example_text: "While doing face-to-face interviews with 133 participants with a standardized open-ended questionnaire (Patton 2002, 344–346), I also used observation, sometimes called field research or ethnography (Neuman 2006), and took notes that were then used to analyze the data."
                    example_assistant: {{"study_method": ['Interview','Case study/anecdotal']}}
                    Reason: Both interviews and ethnographic observations methodologies were used to collect the study data.
                    
                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=StudyMethodParser.get_format_instructions()),
        "variable parser": StudyMethodParser
    }


## Spatial scale -------------------------------


class StudyLocation(BaseModel):
    spatial_scale: Literal['Local','National','Regional','Global','None'] = Field(
        default = "None",
        description="The spatial scale at which the study conducted/data collected. Select ONE value (best-fitting), from the list of allowed values: ['Local','National','Regional','Global','None']. If none apply, return the default 'None'.")
    # country_names: List[CountryShortName] = Field(
    #     default_factory=list,
    #     description="A list of countries in short name format (as expected by pydantic CountryShortName) where the study was conducted. If this information is unavailable, return an empty list."
    # )
    continent: List[Literal['South America','North America', 'Africa', 'Europe', 'Asia', 'Oceania']] = Field(
        default_factory = list, description="A list of the continents where the study was conducted/data collected, selected from the following allowed values: ['South America','North America', 'Africa', 'Europe', 'Asia', 'Oceania']. If none apply, return an empty list.")

StudyLocationParser = PydanticOutputParser(pydantic_object=StudyLocation)


# StudyLocation.parse_obj({'spatial_scale': 'Local', 'country_names':['United States','Uganda']})
    



StudyLocation_dict = {
        "variable name": "study location",
        "variable faissK": 5,
        "variable question": """
        Where was the study conducted? Respond with the following metadata fields:

        1) 'spatial_scale':
        The spatial scale of the study, or the spatial coverage of the data collected. Select the best fitting value from the allowed values defined below. 
        Allowed values:
        -'Local': small-scale studies, communities, municipalities.
        -'National': country-level. 
        -'Regional': Larger than country-level but not full global coverage.
        -'Global': Full global coverage.
        -'None': None of the previous categories suitably describe the spatial scale, or the information is unavailable. 

        If the spatial scale of the study is in between two values, select the smaller spatial scale.

        2) 'continent':
        A list of continents where the study was conducted, selected from the following allowed values: ['South America','North America', 'Africa', 'Europe', 'Asia', 'Oceania'].
        
        If a study location smaller than the continent is mentioned, but the continent can be matched, do so. If this information is unavailable, or the study is at a global scale, return an empty list. 

        """,
        "variable exclude":"""
        ** Filtering Criteria ** 
        - DO NOT include study locations mentioned from other studies, background literature, or prior work cited in the article.
        - DO NOT include study locations mentioned as examples, comparisons, or findings from other studies
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - All category names should be unique
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "In this article, we compare four fishing-based areas in Thailand and the Philippines to examine if and how small-scale fishing communities are able to escape marginalisation. Three questions guide our inquiry: (i) How have fishing communities been affected by overfishing, climate change and other pressures? (ii) What adaptive strategies have these communities employed to mitigate socio-economic and environmental challenges? (iii) What has been the impact of these strategies on (escaping) marginalisation?"
                    example_assistant:{{'spatial_scale': 'Local','continent':['Asia']}}
                    Reason: 'Local' spatial scale was most appropriate because references were made to 'small-scale' and 'communities'. The study was condiucted in Thailand and Phillipines which are both in the continent 'Asia'.

                    --

                    example_text: "This study considers recent trends in ODA allocations to support the fisheries sector in the 146 ODA recipient countries and territories around the world"
                    example_assistant:{{'spatial_scale': 'Global','continent':[]}}
                    Reason: The study was conducted at the global scale, and therefore no continents were identified

                    -- 

                    example_text: "This article explores marine resource governance in the Indian Ocean, the legal landscape relevant to the management of fisheries, as well as selected national law and policy approaches."
                    example_assistant:{{'spatial_scale': 'Regional','continent':['Africa', 'Asia', 'Oceania']}}
                    Reason: The study was conducted at the regional scale in the Indian Ocean, which is bounded by the continents Asia to the north, Africa to the west and Oceania to the east.

                    example_text: "By examining fisheries in the northeastern United States over the last four decades of warming temperatures, we show that northward shifts in species distributions were matched by corresponding northward shifts in fisheries. "
                    example_assistant:{{'spatial_scale': 'Regional','continent':['Africa', 'Asia', 'Oceania']}}
                    Reason: The study was conducted at the regional scale in the Indian Ocean, which is bounded by the continents Asia to the north, Africa to the west and Oceania to the east.

                    --

                    example_text: "To test the extent to which shifting species ranges drive changes in fisheries, this paper examines coincident shifts in selected fish and marine invertebrate distributions and landings over the last 40 years in the northeastern United States.
                    example_assistant:{{'spatial_scale': 'Local','continent':['North America']}}
                    Reason: The northeastern United States is in between 'Local' and 'National', therefore the smallest value 'Local' was selected. The united states is in the continent 'North America'. 

                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=StudyLocationParser.get_format_instructions()),
        "variable parser": StudyLocationParser
    }


## Time scale -------------------------------

class TimeScale(BaseModel):
    time_scale: Literal['<= 1 month','1 month <= 1 year','1 year <= 5 years','5 years <= 10 years', '> 10 years', 'None'] = Field(
        default = "None",
        description="What is the length of time between the implementation of the adaptation action and the end of the study period? Select the best-fitting category from the following allowed values: ['<= 1 month','1 month <= 1 year','1 year <= 5 years','5 years <= 10 years', '> 10 years','None']. If none apply, or the answer is unclear, select the default 'None'.")
    duration_description: str = Field(
        default = "None",
        description="Summarize (3-10 words) when the action was implemented, and when the study data were collected. If the information is unavailable, select the default 'None'.")
    


TimeScaleParser = PydanticOutputParser(pydantic_object=TimeScale)



TimeScale_dict = {
        "variable name": "time scale",
        "variable faissK": 5,
        "variable question": """
        What is the time period of the study? Respond with the following metadata fields:

        1) 'time_scale':
        The time scale of the study, corresponding to the approximate length of time between the implementation of the adaptation action (the action, change, strategy, technology or infrastructure being studied) and the end of the study period. Select the best fitting value from the allowed values defined below. 
        Allowed values:
        -'<= 1 month': Any time period less than or equal to one month
        -'1 month <= 1 year': Any time period greater than 1 month but less than or equal to 1 year.
        -'1 year <= 5 years': Any time period greater than 1 year but less than or equal to 5 years.
        -'5 years <= 10 years': Any time period greater than 5 years but less than or equal to 10 years.
        -'> 10 years': Any time period greater than 10 years.
        -'None': None of the previous categories suitably describe the time scale, or the information is unavailable or unclear. 

        2) 'duration_description':
        A short summary (3-10 words) describing when the action was implemented, and when the study data were collected. If the information is unavailable, select the default 'None'.
        """,
        "variable exclude":"""
        ** Filtering Criteria ** 
        - DO NOT include time periods mentioned from other studies, background literature, or prior work cited in the article.
        - DO NOT include time periods mentioned as examples, comparisons, or findings from other studies
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - All category names should be unique
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "Project activities began in October 2015 in seven municipalities/sites in four provinces of the Philippines– Occidental Mindoro (Looc and Lubang), Camarines Sur (Tinambac), Surigao del Sur (Cantilan and Cortes) and Negros Oriental (Ayungon and Bindoy)\n Phase 1: Research\n Phase 1 was undertaken through three research analyses:• Coastal Livelihood Studies- Landscape overview of livelihood projects in coastal communities over the last 30 years and an in-depth analysis of selected livelihood projects with project implementers and recipients."
                    example_assistant:{{'time_scale': '> 10 years','duration_description':"The action was implemented in 2015 and the study lasted over 30 years."}}
                    Reason: The project start was in 2015, and the analysis duration occurred over 30 years, placing the time_scale as greater than 10 years.
                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=TimeScaleParser.get_format_instructions()),
        "variable parser": TimeScaleParser
    }





## Study result ---------------------------------------------------

class StudyResult(BaseModel):
    result_description: str = Field(
        default="None",
        description="A short description of the result."
    )
    result_type: List[Literal['Ecological','Social','Management','Economic']] = Field(
        default_factory=list,
        description="Select the best-fitting category to describe the result from the following allowed values: ['Ecological','Social','Management','Economic']. If none apply, or the answer is unclear, return an empty list.")
    data_type: Literal['Quantitative','Qualitative','None'] = Field(
        default = "None",
        description="The type of data used to report the result/finding. Select the best-fitting category from the allowed values: ['Quantitative','Qualitative','None']. If none apply, or the answer is unclear, select the default 'None'.")
    result_effect: Literal['Positive','Negative','Neutral','None'] = Field(
        default = "None", #default_factory=str,
        description="The resulting effect on fisheries adaptation. Select the best-fitting category from the allowed values:['Positive','Negative','Neutral', 'None']. If none apply, or the answer is unclear, select the default 'None'."
    )


class StudyResultList(BaseModel):
    # Note this field must always be named 'labels'
    study_results: List[StudyResult] = Field(
        default_factory=list,  # Default to an empty list
        description="A list of all study findings/results/outcomes identified as relevant to the adaptation action. If none are identified, return an empty list."
    )    

# make a parser
StudyResultParser = PydanticOutputParser(pydantic_object=StudyResultList)

## test
# StudyResultList.model_validate({'study_result':[{'result_description': 'savings club allowed fishing households to save and establish social protection','result_type':['Social'],'data_type':'Quantitative','result_effect':'Positive'}]})


StudyResult_dict = {
        "variable name": "study results",
        "variable faissK": 10,
        "variable question": """
        What do the study's results/findings indicate regarding whether the adaptation action (e.g. action, strategy, technology, policy, etc.) studied in the article improved the ability of the fishery (including fish stocks, landings/catch, fishers, the fishing industry) to adapt to climate change? 
        
        Respond with a List named 'study_results'. Each item in the list represents a relevant result from the study. If no relevant results are found, return an empty list (e.g. {{'study_results':[]}}). If relevant results are found, for each relevant result, respond with the following metadata fields:

        1) 'result_description':
        A short summary of the result, and whether the adaptation action improved the fishery's adaptation. If no results are found, return 'None'.

        2) 'result_type':
        A list of group(s) the adaptation result was reported in. Select the best fitting values from the allowed values defined below:
        -'Ecological': marine/coastal organisms, fish stock health, habitats, environment.
        -'Social': humans, human welfare, fishers.
        -'Management': how institutions, policies/practices are managed
        -'Economic': commerical business, finances, industry, or the economy, grants
        If none apply, return the default empty list.

        3) 'data_type':
        The type of data used to measure/report the result. Select the best fitting value from the allowed values defined below:
        -'Quantitative' (i.e. numerical data or measurements, metrics, statistics) 
        -'Qualitative' (i.e. descriptive, observational)
        -'None': None of the previous categories suitably describe the data type, or the information is unavailable or unclear. 

        4) 'result_effect':
        The resulting effect on adaptation. Select the best fitting value from the allowed values defined below:
        -'Positive' (success, improvement, adaptation, increase)
        -'Negative' (failure, mal-adaptation, decrease)
        -'Neutral' (no significant change or effect on adaptation reported, no directionality)
        -'None': None of the previous categories suitably describe the resulting effect, or the information is unavailable or unclear. 
        """,
        "variable exclude":"""
        ** Filtering Criteria ** 
        - DO NOT include results that do not result from the adaptation action (e.g. ecological impacts from climate change without the mediation of an adaptation action).
        - DO NOT include speculative statements (e.g. that are likely from the discussion section)
        - DO NOT include results mentioned from other studies, background literature, or prior work cited in the article.
        - DO NOT include results mentioned as examples, comparisons, or findings from other studies
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - All category names should be unique
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "The approach was able to mobilize more than PhP 14.5 million (US $290,000) in savings over twenty-two months (as of March 2018) in 102 savings clubs with 2237 total members (female– 1693 (76%) and male 544 (24%)). The savings club approach enabled fishing households to save, invest, and establish social protections through emergency funds."
                    example_assistant:{{'study_results':[{{'result_description': 'savings club allowed fishing households to save and establish social protection','result_type':['Social'],'data_type':'Quantitative','result_effect':'Positive'}}]}}
                    Reason: The result social groups (households), was measured using quantitative metrics, and had a positive impact (saving, social protection) on adaptation.

                    --

                    example_text: "Billions have been allocated to fisheries to support nutrition and livelihoods worldwide. Yet, from 2010 to 2015, fisheries allocations decreased by>30%, while grants for non-fisheries sectors increased by>13%. Globally, grants for climate change adaptation and mitigation fell for fisheries, while rapidly increasing in sectors like agriculture and forestry."
                    example_assistant:{{'study_results':[{{'result_description': 'fisheries development grants have fallen in recent years.','result_type':['Economic'],'data_type':'Quantitative','result_effect':'Negative'}}]}}

                    --

                    example_text: "Landings after El Niño 1997–1998 recovered rapidly to 7.8 million metric tons in 1999 and 9.9 million metric tons in 2000."
                    example_assistant:{{'study_results': [{{'result_description': 'Landings rapidly recovered','result_type':['Ecological'],'data_type':'Quantitative','result_effect':'Positive'}}]}}
                    Reason: The recovery of fishery landings (another term for catch) is an indicator of the health of the fish stock and therefore 'Ecological'. This was measured using quantitative metrics, and indicates recovery and a positive adaptation response.

                    --

                    example_text: "These include controlled production based on market demand; and decoupling of fishmeal prices from those of other protein-rich feed substitutes like soybean. This research shows that there are concrete lessons to be learned from successful adaptations to cope with climate change-related extreme climatic events."
                    example_assistant: {{'study_results':[{{'result_description': 'Decoupling fishmeal prices improved adaptation','result_type':['Economic'],'data_type':'Qualitative','result_effect':'Positive'}}]}}
                    Reason: The financial adaptation action of decoupling fishmeal prices ('Economic') was described ('Qualitative') as producing an adaptive response to help the fishery cope with climate change ('Positive').

                    --

                    example_text: "Fishermen rely on past experiences but need scientific understanding for future adaptation due to climate change unpredictability."
                    example_assistant: {{'study_results':[{{'result_description': 'None','result_type':[],'data_type':'None','result_effect':'None'}}]}}
                    Reason: There is no adaptation response to an adaptation action, technology, etc.

                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=StudyResultParser.get_format_instructions()),
        "variable parser": StudyResultParser
    }

# ## For testing
# variable = StudyResult_dict
# variable_name = variable.get("variable name")
# variable_question = variable.get("variable question")
# variable_prompt = variable.get("variable prompt")
# variable_parser = variable.get("variable parser")
# variable_exclude = variable.get("variable exclude")
# variable_faissK = variable.get("variable faissK")

# chain = variable_prompt | model1 | variable_parser

# result = chain.invoke(
#     {"context":"In this article, we compare four fishing-based areas in Thailand and the Philippines to examine if and how small-scale fishing communities are able to escape marginalisation. The case studies illustrate various degrees of adaptive successes that result from integration of top-down and bottom-up initiatives, and availability and access to livelihood strategies.",
#     "variable question": variable_question,
#     "variable exclude": variable_exclude,
#     })
# result


## Procedural, Governance bodies, Rules of Law--------


class ProceduralEquity(BaseModel):
    procedural_equity: bool = Field(default=False,description= "Was procedural equity considered in the design or implementation of the adaptation action? Examples of procedural equity include: communities having a voice in the decision making process; inclusive engagement; considerations make for gender equity, social justice, inclusiveness; factoring in of local or indigenous knowledge; participatory approaches.")
    procedural_equity_description: str = Field(default='None', description="A short summary (max 50 words) of how procedural equity was considered. If the information is unavailable or unclear, return 'None' as a default.")

    
ProceduralEquityParser = PydanticOutputParser(pydantic_object=ProceduralEquity)

ProceduralEquity_dict = {
        "variable name": "procedural equity",
        "variable faissK": 3,
        "variable question": """
        Was PROCEDURAL EQUITY considered in the design or implementation of the adaptation strategy/action/policy? Respond with the following metadata fields:

        1) 'procedural_equity':
        A boolean ('True' or 'False') indicating whether procedural equity was clearly considered.  
        Procedural equity means that communities had **a voice in decision-making processes**, and that planning and implementation were carried out through **inclusive, fair, and diverse engagement mechanisms**.  
        
        Examples of procedural equity include:
        - Use of inclusive, transparent consultation processes
        - Consideration of gender, class, or social equity in decision-making
        - Integration of indigenous/local knowledge through equitable mechanisms
        - Explicit reference to justice, equity, participation, or inclusion in governance or strategy design
        
        Important:
        - ✅ A community *having influence or power in the decision-making process* counts
        - ❌ A community *merely implementing* or *benefiting from* an action does **not** imply procedural equity
        - ❌ Descriptions like “community-based,” “local participation,” or “co-management” **do not qualify unless equity or inclusion is clearly emphasized**
        
        If procedural equity is not clearly addressed or is ambiguous, return 'False'.
        
        ---

        2) 'procedural_equity_description':
        A short summary (max 50 words) of how procedural equity was considered.

        If 'False' or the information is unavailable or unclear, return 'None' as a default.
        
        """,
        "variable exclude":"""
        ** Filtering Criteria ** 
        - DO NOT include recommendations for how procedural equity could be implemented/is needed in future if it has not already been implemented
        - DO NOT include information mentioned from other studies, background literature, or prior work cited in the article.
        - DO NOT include information mentioned as examples, comparisons, or findings from other studies
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - All category names should be unique
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "Increasingly, Tribes and other indigenous groups in the United States, as in other nations, are turning to litigation as a source of adaptation funding and capacity (e.g., Bookman, 2022; Native Village of Kivalina v. ExxonMobil Corp, 696 F.3d 849 (9th Cir, 2012, cert. denied, 569 U.S. 1000 (2013).)"
                    example_assistant:{{'procedural_equity': True,'procedural_equity_description': 'Indigenous groups are having a voice in the adaptation response'}}
                    Reason (do not include in output): Indigenous groups are having a voice in the adaptation response via litigation, so procedural equity is present. 

                    example_text: "Harvesters were purposively selected by the research team to speak to changes on the land and the links between health and traditional foods. A discussion among the community-academic research team identified a coding structure for the interviews and key themes."
                    example_assistant:{{'procedural_equity': False,'procedural_equity_description': 'None'}}
                    Reason (do not include in output): The research method was participatory, but there is no evidence that procedural equity was considered in the adaptation action.  
                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=ProceduralEquityParser.get_format_instructions()),
        "variable parser": ProceduralEquityParser
    }


class Governance(BaseModel):
    governance_body: List[Literal['Community-based','National government','Regional (e.g. RFMOs)','International','Private organizations/companies']] = Field(default_factory=list, description="Select the best-fitting categories to describe the institution/institutions responsible for governing the activities of the adaptation action from the following allowed values: ['Community-based','National government','Regional (e.g. RFMOs)','International','Private organizations/companies']. If none apply, or the answer is unclear, return an empty list."
    )
    rules_of_law: List[Literal['Law (binding)','Non-binding']] = Field(default_factory=list, description="How is the adaptation action governed? Select the best-fitting categories to describe how the action is governed from the following allowed values: ['Law (binding)', 'Non-binding']. If none apply, or the answer is unclear, return an empty list.")

    
GovernanceParser = PydanticOutputParser(pydantic_object=Governance)

Governance_dict = {
        "variable name": "governance",
        "variable faissK": 5,
        "variable question": """
        Do the authors of the article mention **governance enabling conditions** relevant to their studied adaptation action (e.g. action, policy, law, management strategy, infrastructure, or behavioral change)?

        If so, respond with the following two metadata fields:
        
        ---


        1) 'governance_body':
        A list of governing bodies (institutions or actors) responsible for governing or enabling the adaptation action. If multiple levels of governance are mentioned, list all applicable categories.  
        
        Select the best-fitting values from the list below:
        
        -'Community-based': Local communities, municipal authorities, or indigenous organizations governing or directly managing adaptation actions. Examples: coastal villages managing marine resources; local fishers forming co-management groups; decisions made by town councils or municipalities.

        -'National government': National-level ministries, agencies, or legislative bodies involved in designing, regulating, funding, or enforcing adaptation strategies. Examples: national fisheries departments, environmental ministries, climate legislation.

        -'Regional (e.g. RFMOs)': Regional governance bodies, such as Regional Fisheries Management Organizations (RFMOs), responsible for the sustainable management of highly migratory or straddling fish species.
        
        -'International': Global or international institutions, frameworks, or treaties that influence or govern fisheries climate change adaptation. Examples: UNCLOS, IPCC guidance, CBD (Convention on Biological Diversity), international maritime law.

        -'Private organizations/companies': Non-government actors from the private sector directly governing or enabling the adaptation action. Examples: seafood corporations creating traceability policies; insurers or carbon credit companies managing adaptation finance; private certification bodies.

        
        **If the information is missing, unclear, or none of the categories fit, return an empty list.**
        

        2) 'rules_of_law':
        A list of the best-fitting categories to describe how the action is governed. Select the best fitting values from the allowed values defined below:
        
        -'Law (binding)': Legislation, laws, national or international laws, legal agreements, regulatory mandates, or other binding governance instruments. Examples: marine protection laws, national fisheries legislation, treaties, binding UN conventions.
        
        -'Non-binding': Non-binding instruments such as policy documents, codes of conduct, voluntary guidelines, or informal agreements. Examples: voluntary community bylaws, NGO codes of practice, national policy strategies, stakeholder agreements.
        
        **If the article does not specify governance instruments clearly, or if no category applies, return an empty list.**

        """,
        "variable exclude":"""
        ** Filtering Criteria ** 
        - Identify only governance actors or rules that directly influence the adaptation action described in the article.
        - If governance is only mentioned in general terms (e.g. “better policies are needed”), and no actors or instruments are named, return empty lists.
        - DO NOT include information mentioned from other studies, background literature, or prior work cited in the article.
        - DO NOT include information mentioned as examples, comparisons, or findings from other studies
        """,
        "variable prompt": ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    ## TASK:
                    You are a scientific research assistant. You will be given text extracts from a scientific article. From the information in these text extracts:
                    
                    {variable question}  
                    {variable exclude}
                    
                    ## INSTRUCTIONS:
                    - Provide the most complete response possible. 
                    - All category names should be unique
                    - DO NOT MAKE ANYTHING UP.
                    - Adhere strictly to the formatting instructions
                    - Wrap the output in the `json` tags: {format_instructions}

                    # Here are some examples of responses:
                    
                    example_text: "Increasingly, Tribes and other indigenous groups in the United States, as in other nations, are turning to litigation as a source of adaptation funding and capacity (e.g., Bookman, 2022; Native Village of Kivalina v. ExxonMobil Corp, 696 F.3d 849 (9th Cir, 2012, cert. denied, 569 U.S. 1000 (2013).)"
                    example_assistant:{{'governance_body': ['National government'],'rules_of_law':['Law (binding)']}}
                    Reason (do not include in output): Indigenous groups are having a voice in the adaptation response via litigation, so procedural equity is present. The united states government is mentioned, therefore the 'governance_body' is 'National government'. Litigation refers to the implementation of law, therefore 'rules_of_law' is 'Law (binding)'. 

                    example_text: "In this article, we compare four fishing-based areas in Thailand and the Philippines to examine if and how small-scale fishing communities are able to escape marginalisation. The case studies illustrate various degrees of adaptive successes that result from integration of top-down and bottom-up initiatives, and availability and access to livelihood strategies."
                    example_assistant:{{'governance_body': ['Community-based'],'rules_of_law':['Law (binding)','Non-binding']}}
                    Reason (do not include in output): Communities are implementing and governing the action, therefore the 'governance_body' is 'Community-based'. Both top-down (i.e. binding) and bottom-up (i.e. non-binding) actions are mentioned, therefore 'rules_of_law' is ['Law (binding)','Non-binding']. 
                    """
                ),
                ("human", """
                ## Article text extracts:
                {context}
                """)
            ]
        ).partial(format_instructions=GovernanceParser.get_format_instructions()),
        "variable parser": GovernanceParser
    }

## For testing
# variable = StudyResults_dict
# variable_name = variable.get("variable name")
# variable_question = variable.get("variable question")
# variable_prompt = variable.get("variable prompt")
# variable_parser = variable.get("variable parser")
# variable_exclude = variable.get("variable exclude")
# variable_faissK = variable.get("variable faissK")

# chain = variable_prompt | model1 | variable_parser

# result = chain.invoke(
#     {"context":"In this article, we compare four fishing-based areas in Thailand and the Philippines to examine if and how small-scale fishing communities are able to escape marginalisation. The case studies illustrate various degrees of adaptive successes that result from integration of top-down and bottom-up initiatives, and availability and access to livelihood strategies.",
#     "variable question": variable_question,
#     "variable exclude": variable_exclude,
#     })
# result






############ Write variable definitions ##########################

allVariables = [
    SafeFish_dict,
    InterventionInstiutional_dict,
    InterventionTechnology_dict,
    InterventionInfrastructure_dict,
    ClimaticImpactDriver_dict,
    StudyMethod_dict,
    StudyLocation_dict,
    TimeScale_dict,
    StudyResult_dict,
    ProceduralEquity_dict,
    Governance_dict
] 





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


async def answer_variable_deepseek(related_documents, variable_question, variable_prompt,variable_exclude=None):
    chain = variable_prompt | model1 
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


def remove_duplicate_labels(d):
    return {
        k: list(dict.fromkeys(v)) if isinstance(v, list) else v
        for k, v in d.items()
    }


def get_default_values(parser):
    schema = parser.pydantic_object
    defaults = {}

    for field_name, field_info in schema.model_fields.items():
        if field_info.default_factory is not None:
            defaults[field_name] = field_info.default_factory()
        elif field_info.default is not None:
            defaults[field_name] = field_info.default
        else:
            defaults[field_name] = None  # or use ... to indicate missing

    return defaults



def get_nan_values(parser):
    schema = parser.pydantic_object
    defaults = {}

    for field_name, field_info in schema.model_fields.items():
        if field_info.default_factory is not None:
            defaults[field_name] = field_info.default_factory()
        elif field_info.default is not None:
            defaults[field_name] = field_info.default
        else:
            defaults[field_name] = None  # or use ... to indicate missing

    return defaults


def get_nan_values(parser):
    schema = parser.pydantic_object
    return {
        k: np.nan if v.default is not None else None
        for k, v in schema.model_fields.items()
        if not v.is_required()
    }


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
    error_messages = []
    raw_outputs = []

    # while True:
    while error_attempts < max_retries_error and none_attempts < max_retries_none:
        try:

            answer = await answer_variable_deepseek(
                related_documents,
                variable_question,
                variable_prompt,
                variable_exclude=variable_exclude
            )
            await asyncio.sleep(2)
            raw_outputs.append(str(answer))
            
            thinkTags = getThinkTag(answer)
            raw_answer = getAnswer(answer)
            
            fixingParser = OutputFixingParser.from_llm(
                parser=variable_parser,
                llm=model2
            )
            if raw_answer:
                answer_structured = await fixingParser.ainvoke(raw_answer)
            else:
                answer_structured = await fixingParser.ainvoke(answer)

            # answer_structured = await structure_variable_deepseek(
            #     related_documents,
            #     variable_question,
            #     variable_prompt,
            #     fixingParser,
            #     variable_exclude=variable_exclude
            # )

            answer_dict = answer_structured.model_dump()
            

            # # remove duplicate labels?
            # answer_dict = remove_duplicate_labels(answer_dict)

            
            # Retry if all values are None
            if all_values_none(answer_dict):
                none_attempts += 1
                if none_attempts >= max_retries_none:
                    error_messages.append("Max retries exceeded: All values are 'None'")
                    break
                await asyncio.sleep(2)
                    # raise ValueError("Max retries exceeded: All values are 'None'")
                continue  # Retry due to all-None values

            # Successful parse
            # add source text
            answer_dict[f'{variable_name} source text'] = [doc.page_content for doc in related_documents]
            answer_dict[f'{variable_name} raw output'] = raw_outputs
            return answer_dict

        except Exception as e:
            error_attempts += 1
            # print(f'{variable_name} Attempt {error_attempts}: error: {str(e)}')
            error_messages.append(f"Attempt {error_attempts}: {str(e)}")
            
            if error_attempts >= max_retries_error:
                break
            await asyncio.sleep(2)
            #     return {
            #         f"{variable_name} error_message": str(e),
            #         f"{variable_name} source text": [doc.page_content for doc in related_documents]
            #     }
    # If we reach here, it means it failed
    # Final result: conditional fallback depending on retry type
    # If all values none, return default values
    if none_attempts >= max_retries_none:
        fallback_answer = get_default_values(variable_parser)
        fallback_answer[f"{variable_name} error_message"] = error_messages
        fallback_answer[f"{variable_name} source text"] = [doc.page_content for doc in related_documents]
        fallback_answer[f'{variable_name} raw output'] = raw_outputs
        return fallback_answer

    # If other error, return nan
    else:
        fallback_answer = get_nan_values(variable_parser)
        fallback_answer[f"{variable_name} error_message"] = error_messages
        fallback_answer[f"{variable_name} source text"] = [doc.page_content for doc in related_documents]
        fallback_answer[f'{variable_name} raw output'] = raw_outputs
        return fallback_answer




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
            # text = load_pdf(pdf_path)
            # if text:
            #     chunked = split_text(text, chunk_size, chunk_overlap)
            # else:
            result = {'id': int(file), 'pdf reading error': 'PDF corruption detected could not extract content.'}
            with open(os.path.join(answer_directory, f"{file}_code.txt"), 'w') as f:
                json.dump(result, f)
            return file
            
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

    result = {'id': int(file), 'coding response': [codeResults]} 

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



## Utils for rescuing json output from error
import json
import re
from typing import Any, Optional

def extract_json_candidates(text: str) -> list[str]:
    """
    Finds candidate JSON strings by looking for balanced bracket structures.
    Returns a list of strings that look like JSON objects or arrays.
    """
    candidates = []
    stack = []
    start_idx = None

    for i, char in enumerate(text):
        if char in '{[':
            if not stack:
                start_idx = i
            stack.append(char)
        elif char in '}]' and stack:
            opening = stack.pop()
            if not stack:
                end_idx = i + 1
                candidates.append(text[start_idx:end_idx])
    return candidates

def rescue_json(response: str) -> Optional[Any]:
    """
    Attempts to extract and parse valid JSON (object or array) from noisy LLM responses.

    Parameters:
        response (str): Raw LLM output with possible embedded JSON.

    Returns:
        Parsed JSON (dict or list) if successful, else None.
    """
    if response == "Max retries exceeded: All values are 'None'":
        return []

    if "EOF (status code:" in response:
        return np.nan
    
    # Step 1: Extract JSON blocks inside ```json ... ```
    fenced_blocks = re.findall(r'```(?:json)?(.*?)```', response, re.DOTALL | re.IGNORECASE)

    # Step 2: Use bracket matching to extract inline JSON candidates
    inline_candidates = extract_json_candidates(response)

    candidates = fenced_blocks + inline_candidates

    for candidate in candidates:
        candidate = candidate.strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Attempt cleanup
            cleaned = (
                candidate
                .replace("“", "\"")
                .replace("”", "\"")
                .replace("‘", "'")
                .replace("’", "'")
            )
            cleaned = re.sub(r'\b(True|False|null)\b', lambda m: m.group(0).lower(), cleaned)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                continue

    return None
