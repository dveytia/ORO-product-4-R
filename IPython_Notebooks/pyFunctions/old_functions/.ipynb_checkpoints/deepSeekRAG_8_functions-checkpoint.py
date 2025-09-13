


## STEP 0: DEFINE SCHEMAS FOR MULTIPLE CHOICE LABELS

## Screening question
class SafeFish(BaseModel):
    include: bool = Field(default=True,description= "Does this research study a fisheries climate change adaptation action? If yes, reply True and if no, reply False. If the information is unavailable or unclear, reply with True.")


SafeFishParser = PydanticOutputParser(pydantic_object=SafeFish)

SafeFish_dict = {
        "variable name": "safe fish",
        "variable faissK": 10,
        "variable question": """
        ** Answer the question (True/False)**: Does this article study outcomes resulting from an action aiming to help marine fisheries adapt to climate change? 
        
        Use the following term definitions to guide your interpretation and assessment of the question: 
        
        - action: any action. The definition of 'action' is broad, and includes intitutional/management actions (e.g. governance, law, policy (non-binding), practices, fisheries management), socio-behavioural actions or responses (e.g. community-based strategies, fisher/fishing community adaptive actions, changing fishing practices, migration), economic (e.g. market mechanisms), built infrastructure (e.g. sea walls), nature-based coastal protection (e.g. restoration/conservation actions, shore nourishment),  technology (e.g. early warning systems, new fishing technologies) 
        - fisheries: any fishery (commercial, subsistence, artisinal), including: fishers, fishing community, commerically fished species (e.g. population health, stock size, landings, catch), or fishing business. 
        - adaptation: the process of adjustment to actual or expected climate and its effects, in order to moderate harm or exploit beneficial opportunities. Adapation outcomes can be ecological, economic or social.
        - climate change: any climate change impact, including 'climatic impact drivers': marine/coastal environmental pressures/hazards linked to climate change, such as ocean acidification, ocean warming, marine heatwaves, sea level rise, storm surges, extreme weather, harmful algal bloom (HAB) linked to climate change.
        - outcome: a result or finding derived from the study conducted by the authors. Outcomes can be qualitative (descriptive, anecdotal) or quantitative. Outcomes can evaluate the intended effect of the action (e.g. whether it was effective at improving adaptation), as well as unintended effects (e.g. side-effects, trade-offs, co-benefits, enabling factors, barriers or limits).


        **FILTERING CRITERIA**
        Include:
        - articles where fisheries are directly affected by the action, even if 'fishery' is not explicitly mentioned (e.g. fisheries management, ocean governance with fisheries implications, improving adaptation to climate change in the marine sector/marine natural resources).
        - analyses (including descriptive/qualitative analyses) of the impacts of existing management policies/laws/documents
        
        """,
        "variable exclude":"""
        Exclude: 
        - *articles where the action is NOT implemented*. For example:
            - vulnerability assessments
            - planning or design or an action but the action is not implemented
            - the article provides action reccomendation with no implementation
        - coastal adaptation actions with NO fishery relevance (e.g. aquaculture, mariculture, coastal community adaptation with no fishery context).
        - actions adapting to other pressures (e.g. overfishing/pollution) without mention of climate change or a valid climatic impact driver.
        - freshwater fisheries
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
                    - DO NOT MAKE ANYTHING UP.
                    - DO NOT include <think> tags in your response.
                    - **Wrap the output in the following `json` tags, and adhere STRICTLY to this schema:**
                    
                    {format_instructions}

                    ## Here are some examples of responses:
                    
                    example_text: "In this article, we compare four fishing-based areas in Thailand and the Philippines to examine if and how small-scale fishing communities are able to escape marginalisation. Three questions guide our inquiry: (i) How have fishing communities been affected by overfishing, climate change and other pressures? (ii) What adaptive strategies have these communities employed to mitigate socio-economic and environmental challenges? "
                    example_assistant: {{'include': True}} 
                    Reason: Include because fishing communities, climate change and implemented adaptation actions are all present. 
                    
                    --
                    
                    example_text: "Many municipalities undertake actions individually and/or collectively, in cooperation with central administrations, regional authorities, the private sector, and other municipalities (both nationally and internationally). This paper aims to examine how they use transnational municipal networks (TMNs) as a tool for cooperation that supports marine governance in the context of climate change adaptation and mitigation. "
                    example_assistant: {{'include': False}}
                    Reason: Exclude because not specific to fishery

                    --

                    example_text:"Faced with rising seas, eroding coastlines, and depleting fish stocks and biodiversity, Guet Ndarians abroad and at home respond to the ensuing degradation of livelihoods and the destruction of homes by altering their mobility patterns"
                    example_assistant: {{'include': True}}
                    Reason: The article discusses how fishing communities adapt to climate change through their practices and movements (implemented action).

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
        Respond with a List of all SOCIO-INSTITUTIONAL actions/strategies to help marine fisheries adapt to climate change that are studied in the article. In general, actions relevant to changes in POLICY, PRACTICE, MANAGEMENT, LAW, ECONOMICS/FINANCE or SOCIAL BEHAVIOUR will fall into one of these categories. List elements must be selected from the **allowed values** ['Institutional','Fisheries management','Socio-behavioural','Economic'] defined below. If no eligible socio-institutional actions are identified, respond with an empty list.
        
        **Allowed value definitions**:
        
        - **Institutional**: Changes to institutional structures, policies, laws, or governance frameworks that support climate adaptation in marine fisheries. These are typically top-down actions by governments or institutions. Examples include:
              - New or reformed ocean governance frameworks
              - International or inter-institutional agreements
              - Marine spatial planning (MSP)
              - Integrated coastal zone management (ICZM)
              - Legal reforms or environmental legislation relevant to fisheries

        - **Fisheries management**: Changes to how fisheries are managed or fishing is conducted, often led by management authorities but sometimes involving community participation. These actions directly regulate or influence fishing activity. Examples include:
              - Co-management, community-based management, or adaptive management
              - Ecosystem-based fisheries management
              - Quotas, seasonal closures, or gear restrictions
              - Population assessments or fish stocking
              - Restoration of fish habitats

        - **Socio-behavioural**: Actions taken voluntarily by individual fishers, households, or communities to adapt their behavior or livelihoods in response to climate change impacts. These are bottom-up, behavioral or social responses rather than imposed regulations. Examples include:
              - Switching fishing gear, target species, or fishing grounds
              - Adjusting the timing or frequency of fishing
              - Seasonal mobility or relocation to follow fish
              - Livelihood diversification (e.g. fish processing, aquaculture, tourism)
              - Human migration or planned retreat from coastal areas
              - Voluntarily exiting the fishery
              - Participating in community knowledge-sharing or adaptive learning

        - **Economic**: Actions that involve the use of financial, market-based, or economic instruments to support adaptation in marine fisheries. These strategies focus on monetary, market, or financial aspects. Examples include:
              - Insurance programs for fishers
              - Access to finance or credit
              - Market-based mechanisms (e.g. carbon credits, fishing rights)
              - Alternative or value-added seafood markets
              - Financial incentives or compensation schemes
              - Economic diversification related to fisheries (e.g. eco-tourism, new product development)
             

        Note: Use the examples provided in the definitions to guide your inclusion decisions. If no eligible socio-institutional action is identified, respond with an empty list.

        **Examples**:
        - A fisher changes target species due to warming waters ➤ Socio-behavioural
        - A policy bans fishing in certain areas ➤ Fisheries management
        - A community starts migrating away from the coast ➤ Socio-behavioural
        - A government creates a new integrated coastal management law ➤ Institutional
        - Fishers receive subsidies to offset losses ➤ Economic


        ** Filtering Criteria **
        ALL ACTIONS MUST aim to help **marine fisheries** (including fishing communities, fishers, fishing industries, commercially fished populations) **adapt** to **climate change** (including marine/coastal environmental pressures/hazards linked to climate change, such as ocean acidification, ocean warming, marine heatwaves, sea level rise, storm surges, extreme weather) 
    
        """,
        "variable exclude":"""
        EXCLUDE: 
        - Adaptation actions that are NOT socio-institutional**. For example, the following types of actions would be EXCLUDED: disaster response programs, technologies, built infrastructure, beach, dunes, shore nourishment
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

                    ## Here are some examples of responses:
                    
                    example_text: "Results showed eight coping strategies to reduce impacts on the fishery. These included: low cost intensive monitoring; rapid flexible management."
                    example_assistant: "intervention_institutional": ['Fisheries management']
                    Reason: The monitoring and management of fishery activities falls under 'Fisheries management'. 

                    --
                    
                    example_text: "Results showed eight coping strategies to reduce impacts on the fishery. These included: opportunistic utilization of invading fish populations."
                    example_assistant: "intervention_institutional": ['Socio-behavioural']
                    Reason: opportunistic utilization of invading fish populations demonstrates a change in fishing behaviour/practices on behalf of the fishers, and therefore constitutes 'Socio-behavioural'. 

                    --

                    example_text: "Results showed eight coping strategies to reduce impacts on the fishery. These included: simultaneous ownership of fishing fleet and processing factories; reduction of fishmeal price uncertainty through controlled production based on market demand."
                    example_assistant: "intervention_institutional": ['Economic']
                    Reason: Financial ownership of a part of a business (i.e. fishing fleet and processing factories) and manipulating prices through market demand are economic coping mechanisms and therefore are classified as 'Economic'. 
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
        - **Adaptation actions that are NOT TECHNOLOGIES**. For example, the following types of actions would be EXCLUDED: changes to policy, laws, fisheries management, economics, behaviour, built infrastructure (e.g. sea walls), nature-based solutions (e.g. shore nourishment, restoration).
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

                    example_assistant: "intervention_technology": ['Disaster response technologies']
                    Reason: **Technology** was mentioned as being employed to help *fishers* adapt to extreme weather (a coastal hazard linked to climate change). 

                    --

                    example_text:" The main driver of anchovy stock variability is the El Niño Southern Oscillation (ENSO), and 
three extreme ENSO warm events were recorded in 1972–1973, 1983–1984 and 1997–1998. This study investigates the evolution of coping strategies developed by the anchovy fisheries to deal with climate variability and extreme ENSO events. Results showed eight coping strategies to reduce impacts on the fishery. These included: decentralized installation of anchovy processing factories; simultaneous ownership of fishing fleet and processing factories; low cost intensive monitoring; rapid flexible management; reduction of fishmeal price uncertainty through controlled production based on market demand; and decoupling of fishmeal prices from those of other protein-rich feed substitutes like soybean. "
                    example_assistant: "intervention_technology": []
                    Reason: Although these adaptation actions respond to extreme events/coastal hazards, they are NOT technologies -- they are better classified as 'socio-institutional' and 'infrastructure'.

                    --

                    example_text: "Over the longer term, fishermen and the fishing industry more broadly will face the challenges and costs of adapting processing and fishing infrastructure as well as fishing gear to take advantage of the opportunities provided by new species."
                    example_assistant: "intervention_technology": []
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
        - **adaptation actions that are NOT INFRASTRUCTURE**. For example, the following types of actions would be EXCLUDED: changes to policy, laws, fisheries management, economics, behaviour, new technologies, distaster response programs, early warning systems.
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
                    example_assistant: "intervention_infrastructure": ['Built infrastructure']
                    Reason: Climate change causes increasingly extreme ENSO events, affecting fishers. Low-cost facilities consitutes the use of a new built infrastructure to improve adaptation.

                    example_text: "Successful initiatives have included disaster risk reduction measures, mangrove planting, and setting up fish sanctuaries and oyster cultures. "
                    example_assistant: "intervention_infrastructure": ['Nature-based']
                    Reason: Mangroves attenuate storm surges and therefore planting or restoring mangroves to reduce coastal hazard risk in the context of fisheries adaptation is 'Soft infrastructure'.

                    --

                    example_text: "Over the longer term, fishermen and the fishing industry more broadly will face the challenges and costs of adapting processing and fishing infrastructure as well as fishing gear to take advantage of the opportunities provided by new species."
                    example_assistant:"intervention_infrastructure": []
                    Reason: The statement is speculative and does not indicate that the infrastructure (processing and fishing infrastructure) was implemented.

                    --

                    example_text: "a broad-based outcome, including material goals such as economic yield, food supplies, and employ-ment, as well as nonmaterial aspects such as safe, decent, and nondiscriminatory work conditions. It also encompasses the preservation of marine and coastal ecosystems (International Labour Organi-', 'the heritage of the fishing community (i.e., the built environment) is protected and that 2) access to affordable housing is provided. These measures, if implemented, should caution against overdevelopment and property value inflation at the expense of local residents."
                    example_assistant: "intervention_infrastructure": []
                    Reason: Vague references to the built environment, ecoystem health and socio-ecological ecosystems is insufficient evidence for classification as infrastructure implemented to help marine/coastal fisheries/fishing communities adapt to climate change. 
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
                    example_assistant: "climatic_impact_driver": ['Climate change in general']
                    Reason: Climate change was mentioned as motivating the fishers to adapt, but no specific mechanisms were identified

                    example_text: "Fishers have had a variety of adaptation strategies to cope with the decreased catch and extreme weather (see Table 2)."
                    example_assistant: "climatic_impact_driver": ["Storms/extreme weather"]
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
    study_method: List[Literal['Experiment','Quantitative analysis','Qualitative analysis', 'Observation', 'Workshop','Interview','Survey','Case study/anecdotal']] = Field(
        default_factory = list, description="A list of the types of study methods used in the study, selected from a list of pre-defined allowed values: ['Experiment','Quantitative analysis','Qualitative analysis', 'Observation', 'Workshop','Interview','Survey','Case study/anecdotal']")


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
        -'Survey': Social science research method involving standardized data collection through questionnaires, polls, or forms administered to individuals or groups. This does NOT include ecological field surveys which are categorized as 'Observational'
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
                    example_assistant: "study_method": ['Survey']
                    Reason: A survey is conducted as a part of the current study (there is no indication (e.g. citation) that this survey was conducted in another study)

                    --

                    example_text: "While doing face-to-face interviews with 133 participants with a standardized open-ended questionnaire (Patton 2002, 344–346), I also used observation, sometimes called field research or ethnography (Neuman 2006), and took notes that were then used to analyze the data."
                    example_assistant: "study_method": ['Interview','Case study/anecdotal']
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
    country_names: List[CountryShortName] = Field(
        default_factory=list,
        description="A list of countries in short name format (as expected by pydantic CountryShortName) where the study was conducted. If this information is unavailable, return an empty list."
    )

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

        2) 'country_names':
        A list of countries in short name format (as expected by pydantic CountryShortName) where the study was conducted. If this information is unavailable, return an empty list. If a study location smaller than the country is mentioned, but the country can be matched, do so. For example if the text mentions 'Los Angeles', respond with 'United States'.

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
                    example_assistant:{{'spatial_scale': 'Local','country_names':['Thailand', 'Philippines']}}
                    Reason: 'Local' spatial scale was most appropriate because references were made to 'small-scale' and 'communities'. Country names were extracted and formatted as expected to conform with pydantic CountryShortName and listed in 'country_names'.
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
    data_type: Literal['Quantitative','Qualitative','Mixed','None'] = Field(
        default = "None",
        description="The type of data used to report the result/finding. Select the best-fitting category from the allowed values: ['Quantitative','Qualitative','Mixed','None']. If none apply, or the answer is unclear, select the default 'None'.")
    result_effect: Literal['Positive','Negative','Neutral','Mixed','Uncertain','None'] = Field(
        default = "None", #default_factory=str,
        description="The resulting effect on fisheries adaptation. Select the best-fitting category from the allowed values:['Positive','Negative','Neutral','Mixed','Uncertain', 'None']. If none apply, or the answer is unclear, select the default 'None'."
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
        -'Economic': commerical business, finances, industry, or the economy, grands
        If none apply, return the default empty list.

        3) 'data_type':
        The type of data used to measure/report the result. Select the best fitting value from the allowed values defined below:
        -'Quantitative' (i.e. numerical data or measurements, metrics, statistics) 
        -'Qualitative' (i.e. descriptive, observational)
        -'Mixed' (i.e. a combination of various quantitative and qualitative metrics all needed to represent the same result)
        -'None': None of the previous categories suitably describe the data type, or the information is unavailable or unclear. 

        4) 'result_effect':
        The resulting effect on adaptation. Select the best fitting value from the allowed values defined below:
        -'Positive' (success, improvement, adaptation, increase)
        -'Negative' (failure, mal-adaptation, decrease)
        -'Neutral' (no significant change or effect on adaptation reported, no directionality)
        -'Mixed' (positive on some aspects, negative on others)
        -'Uncertain' (results were not clear)
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
    procedural_equity: bool = Field(default=False,description= "Was actions equity considered in the design or implementation of the adaptation action? Examples of procedural equity include: communities having a voice in the decisionmaking process; inclusive engagement; considerations make for gender equity, social justice, inclusiveness; factoring in of local or indigenous knowledge; participatory approaches.")
    procedural_equity_description: str = Field(default='None', description="A short summary (max 50 words) of how procedural equity was considered. If the information is unavailable or unclear, return 'None' as a default.")

    
ProceduralEquityParser = PydanticOutputParser(pydantic_object=ProceduralEquity)

ProceduralEquity_dict = {
        "variable name": "procedural equity",
        "variable faissK": 3,
        "variable question": """
        Was PROCEDURAL EQUITY considered in the design or implementation of the adaptation strategy/action/policy? Respond with the following metadata field:

        1) 'procedural_equity':
        A boolean (True or False) response indicating whether procedural equity (i.e. communities having a voice in decisionmaking processes, and that adaptation planning and implementation are done through diverse and inclusive engagement processes) was considered in the design or implementation of the adaptation strategy/action/policy. Examples of procedural equity include: inclusive engagement; considerations make for gender equity, social justice, inclusiveness; factoring in of local or indigenous knowledge; participatory approaches.

        If the information is unavailable or unclear, return 'False' as a default.

        2) 'procedural_equity_description':
        A short summary (max 50 words) of how procedural equity was considered.

        If the information is unavailable or unclear, return 'None' as a default.
        """,
        "variable exclude":"""
        ** Filtering Criteria ** 
        - DO NOT include reccomendations for how procedural equity could be implemented/is needed in future if it has not already been implemented
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
    rules_of_law: List[Literal['Law (binding)','Non-binding']] = Field(default_factory=list, description="How is the adaptation action governed? Select the best-fitting categories to describe how the action is goverened from the following allowed values: ['Law (binding)', 'Non-binding']. If none apply, or the answer is unclear, return an empty list.")

    
GovernanceParser = PydanticOutputParser(pydantic_object=Governance)

Governance_dict = {
        "variable name": "governance",
        "variable faissK": 5,
        "variable question": """
        Do the authors of the article mention governance enabling conditions relevant for their studied adaptation action (e.g. action, policy, law, management strategy, infrastructure, behaviour)? Respond with the following metadata fields:

        1) 'governance_body':
        A list of governing bodies (institution/institutions) responsible for governing the activities of the action. Select the best fitting values from the allowed values defined below:
        -'Community-based' (e.g. communities; municiple governments)
        -'National government': National governments, national laws,
        -'Regional (e.g. RFMOs)': Regional fisheries management organisations (RFMOs), organisations responsible for the sustainable management of highly migratory or straddling fish species.
        -'International': international/global governance (e.g. international agreements)
        -'Private organizations/companies': private organizations/companies
        
        If none of the previous categories suitably describe the governing body, or the information is unavailable or unclear, return the default empty list.

        2) 'rules_of_law':
        A list of the best-fitting categories to describe how the action is governed. Select the best fitting values from the allowed values defined below:
        -'Law (binding)': Legislation, laws, and other forms of binding agreements.
        -'Non-binding': Non-binding forms of governance (e.g. policy, code of conduct, informal rules)
        
        If none of the previous categories suitably describe the rules of law described in the article, or the information is unavailable or unclear, return the default empty list.
        """,
        "variable exclude":"""
        ** Filtering Criteria ** 
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



## LEFT OFF HERE #######




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

            # # remove duplicate labels?
            # answer_dict = remove_duplicate_labels(answer_dict)

            

            # Retry if all values are None
            if all_values_none(answer_dict):
                none_attempts += 1
                if none_attempts >= max_retries_none:
                    raise ValueError("Max retries exceeded: All values are 'None'")
                continue  # Retry

            # add source text
            answer_dict[f'{variable_name} source text'] = [doc.page_content for doc in related_documents]
            return answer_dict

        except Exception as e:
            error_attempts += 1
            if error_attempts >= max_retries_error:
                return {
                    f"{variable_name} error_message": str(e),
                    f"{variable_name} source text": [doc.page_content for doc in related_documents]
                }




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
