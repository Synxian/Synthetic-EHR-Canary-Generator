from utils import read_xml
def system_prompt(example):
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
MEDDOCAN_HUMAN_EXAMPLE = [
  {'tag': 'NAME', 'text': 'Jose', 'TYPE': 'NOMBRE_SUJETO_ASISTENCIA'},
  {'tag': 'NAME', 'text': 'Aranda Martinez', 'TYPE': 'NOMBRE_SUJETO_ASISTENCIA'},
  {'tag': 'AGE', 'text': '37 años', 'TYPE': 'EDAD_SUJETO_ASISTENCIA'},
  {'tag': 'LOCATION', 'text': 'Calle Losada Martí 23, 5 B', 'TYPE': 'CALLE'}
]

MEDDOCAN_AI_RESPONSE = read_xml('examples/meddocan/response_example.xml')
