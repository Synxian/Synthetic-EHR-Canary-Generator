import os
import json
from prompts import (single_history_system_prompt, continuous_history_system_prompt,
    SINGLE_HISTORY_MEDDOCAN_HUMAN_EXAMPLE, SINGLE_HISTORY_I2B2_HUMAN_EXAMPLE)
from langchain_core.prompts import ChatPromptTemplate

def read_xml(path):
    with open(path, 'r', encoding='utf8') as file:
        xml = file.read()
    return xml

def write_xml(path, content):
    with open(path, "w") as f:
        f.write(content)

def read_json(path):
    with open(path, 'r') as file:
        json_data = json.load(file)
    return json_data

def prepare_input(input):
    tags = [f'<tag>\n{tag}\n</tag>' for tag in input]
    return f"<tags>\n{os.linesep.join(tags)}</tags>"

def file_sample(dataset):
    return read_xml(f'examples/{dataset}/example.xml')

def single_human_prompt_example(dataset):
    dataset = dataset.upper()
    return globals()[f"SINGLE_HISTORY_{dataset}_HUMAN_EXAMPLE"]

def ai_response_example(dataset):
    return read_xml(f'examples/{dataset}/response_example.xml')

def prompt(mode, dataset):
    if mode == 'single':
        return ChatPromptTemplate([
            ('system', single_history_system_prompt(file_sample(dataset))),
            ('human', single_human_prompt_example(dataset)),
            ('ai', ai_response_example(dataset)),
            ('human', "{user_input}")
        ])
    elif mode == 'history':
        return ChatPromptTemplate([
            ('system', continuous_history_system_prompt()),
            ('human', "{user_input}")
        ])

