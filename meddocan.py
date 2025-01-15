from langchain_core.prompts import ChatPromptTemplate
from utils import read_xml
from prompts import system_prompt, MEDDOCAN_HUMAN_EXAMPLE, MEDDOCAN_AI_RESPONSE

def meddocan_example():
  return read_xml('examples/meddocan/example.xml')

def meddocan_prompt():
  return ChatPromptTemplate([
    ('system', system_prompt(meddocan_example())),
    ('human', MEDDOCAN_HUMAN_EXAMPLE),
    ('ai', MEDDOCAN_AI_RESPONSE),
    ('human', "{user_input}")
  ])
