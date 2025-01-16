from langchain_core.prompts import ChatPromptTemplate
from utils import read_xml
from prompts import (single_history_system_prompt, continuous_history_system_prompt,
    SINGLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE, MULTIPLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE,
    MEDDOCAN_AI_RESPONSE)

def meddocan_example():
    return read_xml('examples/meddocan/example.xml')

def meddocan_prompt(mode):
    if mode == 'single':
        return ChatPromptTemplate([
            ('system', single_history_system_prompt(meddocan_example())),
            ('human', SINGLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE),
            ('ai', MEDDOCAN_AI_RESPONSE),
            ('human', "{user_input}")
        ])
    return ChatPromptTemplate([
        ('system', continuous_history_system_prompt(meddocan_example())),
        ('human', MULTIPLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE),
        ('ai', f'[{MEDDOCAN_AI_RESPONSE}]'),
        ('human', "{user_input}")
    ])
