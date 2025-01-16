from utils import read_xml

def single_history_system_prompt(example):
  return f"""
<role>
  You are a medical data expert. Your objecive is to enrich an EHR dataset following a set of rules.
</role>
<example>
  {example}
</example>
<rules>
  <rule>
    The generated EHR must follow the style of the example. Contain the same tags and structure.
  </rule>
  <rule>
    Your response must be a valid XML file.
  </rule>
  <rule>
    You will be provided with a list of tags and their descriptions. You must use them to construct the EHR.
  </rule>
  <rule>
    The content of the response must be your own elaboration, the example is only for style and format.
  </rule>
</rules>
"""

def continuous_history_system_prompt(example):
    return f"""
<role>
  You are a medical data expert. Your objecive is to enrich an EHR dataset following a set of rules.
</role>`
<example>
  {example}
</example>
<rules>
  <rule>
    The generated EHR must follow the style of the example. Contain the same tags and structure.
  </rule>
  <rule>
    Your response must be a valid XML file.
  </rule>
  <rule>
    You will be provided with a list of tags and their descriptions. You must use them to construct the EHR.
  </rule>
  <rule>
    You will receive a set of tags that represents an individual and a number n_samples that indicates the amount of files you must generate for said individual.
  </rule>
  <rule>
    The generated medical text must be coherent in the context of doctor visits, always keeping in mind the generated thread of observations and the individual circumstances.
    It must be rich in medical language, remember that your job is to enrich a dataset composed of multiple EHRs.
  </rule>
  <rule>
    The generated EHRs must be a thread of multiple, distinct doctor visits. You may change the subject age as you see fit.
  </rule>
</rules>
"""

SINGLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE = """
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
  {'tag': 'LOCATION', 'text': 'Madrid', 'TYPE': 'TERRITORIO'},
</tag>
<tag>
  {'tag': 'LOCATION', 'text': 'España', 'TYPE': 'PAIS'},
</tag>
"""

MULTIPLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE = """
<n_samples>
  1
</n_samples>
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
  {'tag': 'LOCATION', 'text': 'Madrid', 'TYPE': 'TERRITORIO'},
</tag>
<tag>
  {'tag': 'LOCATION', 'text': 'España', 'TYPE': 'PAIS'},
</tag>
"""
MEDDOCAN_AI_RESPONSE = read_xml('examples/meddocan/response_example.xml')
