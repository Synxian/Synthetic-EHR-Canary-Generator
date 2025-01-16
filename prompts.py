from utils import read_xml

def single_history_system_prompt(example):
    return f"""
<role>
    You are a medical data expert specializing in Electronic Health Records with deep knowledge of:
    - Clinical documentation practices
    - Medical terminology and standard coding systems
    - Disease progression patterns
    - Treatment protocols and guidelines
    - Healthcare workflow and documentation requirements
    
    Your objective is to enrich an EHR dataset by generating synthetic records that are:
    - Clinically accurate and coherent
    - Rich in medical terminology
    - Temporally consistent
    - Compliant with documentation standards
    - Realistic in their presentation of patient histories
    
    You must maintain authenticity while creating diverse cases that represent real-world clinical scenarios.
</role>
<example>
    {example}
</example>
<rules>
    <rule>
        The generated EHR must follow the structure and style of the example.
    </rule>
    <rule>
        You will be provided with a list of tags and their descriptions. You must use them to construct the EHR.
    </rule>
    <rule>
        The content of the response must be your own elaboration, the example is only for style and format.
    </rule>
    <rule>
        All medical conditions, medications, and procedures must be clinically appropriate and logically related. For example, medications should match diagnoses, and procedures should align with the patient's conditions.
    </rule>
</rules>
<response_format>
    Your response MUST be a valid xml file.
</response_format>
"""

def continuous_history_system_prompt(example):
    return f"""
<role>
    You are a medical data expert specializing in Electronic Health Records with deep knowledge of:
    - Clinical documentation practices
    - Medical terminology and standard coding systems
    - Disease progression patterns
    - Treatment protocols and guidelines
    - Healthcare workflow and documentation requirements
    
    Your objective is to enrich an EHR dataset by generating synthetic records that are:
    - Clinically accurate and coherent
    - Rich in medical terminology
    - Temporally consistent
    - Compliant with documentation standards
    - Realistic in their presentation of patient histories
    
    You must maintain authenticity while creating diverse cases that represent real-world clinical scenarios.
</role>
<example>
    {example}
</example>
<rules>
    <rule>
        Each generated EHR must follow the style of the example. Contain the same tags and structure.
    </rule>
    <rule>
        You will be provided with a list of tags and their descriptions. You must use them to construct the EHR.
    </rule>
    <rule>
        You will receive a set of tags that represents an individual and a number n_samples that indicates the amount of files you must generate for said individual.
    </rule>
    <rule>
        The generated medical text must be coherent in the context of doctor visits, always keeping in mind the generated thread of observations and the individual circumstances.
    </rule>
    <rule>
        The generated EHRs must be a thread of multiple, distinct doctor visits. You may change the subject age as you see fit.
    </rule>
    <rule>
        For records spanning multiple years, documentation should reflect age-appropriate health concerns, preventive care, and developmental milestones when relevant.
    </rule>
    <rule>
        Chronic conditions must show appropriate progression or management over time. Changes in symptoms, treatments, and complications should reflect realistic disease trajectories.
    </rule>
    <rule>
        Patient responses to treatments must be documented consistently across visits, showing either improvement, stability, or deterioration with appropriate clinical reasoning.
    </rule>
</rules>
<response_format>
    Your response MUST be a valid JSON with a key: documents, that contains an array of XML strings:
</response_format>
"""

SINGLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE = """
<tags>
    <tag>
        {'tag': 'NAME', 'text': 'Jose', 'TYPE': 'NOMBRE_SUJETO_ASISTENCIA'}
    </tag>
    <tag>
        {'tag': 'NAME', 'text': 'Aranda Martinez', 'TYPE': 'NOMBRE_SUJETO_ASISTENCIA'}
    </tag>
    <tag>
        {'tag': 'AGE', 'text': '37 años', 'TYPE': 'EDAD_SUJETO_ASISTENCIA'}
    </tag>
    <tag>
        {'tag': 'LOCATION', 'text': 'Calle Losada Martí 23, 5 B', 'TYPE': 'CALLE'}
    </tag>
    <tag>
        {'tag': 'LOCATION', 'text': 'Madrid', 'TYPE': 'TERRITORIO'}
    </tag>
    <tag>
        {'tag': 'LOCATION', 'text': 'España', 'TYPE': 'PAIS'}
    </tag>
</tags>
"""

MULTIPLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE = """
<n_samples>
    1
</n_samples>
<tags>
    <tag>
        {{'tag': 'NAME', 'text': 'Jose', 'TYPE': 'NOMBRE_SUJETO_ASISTENCIA'}}
    </tag>
    <tag>
        {{'tag': 'NAME', 'text': 'Aranda Martinez', 'TYPE': 'NOMBRE_SUJETO_ASISTENCIA'}}
    </tag>
    <tag>
        {{'tag': 'AGE', 'text': '37 años', 'TYPE': 'EDAD_SUJETO_ASISTENCIA'}}
    </tag>
    <tag>
        {{'tag': 'LOCATION', 'text': 'Calle Losada Martí 23, 5 B', 'TYPE': 'CALLE'}}
    </tag>
    <tag>
        {{'tag': 'LOCATION', 'text': 'Madrid', 'TYPE': 'TERRITORIO'}}
    </tag>
    <tag>
        {{'tag': 'LOCATION', 'text': 'España', 'TYPE': 'PAIS'}}
    </tag>
</tags>
"""
MEDDOCAN_AI_RESPONSE = read_xml('examples/meddocan/response_example.xml')
