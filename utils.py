import os
import json

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

def prepare_input(input, mode, n_samples):
    tags = [f'<tag>\n{tag}\n</tag>' for tag in input]
    tags_string =  f"<tags>\n{os.linesep.join(tags)}</tags>"
    if mode == 'single':
        return tags_string
    return f'<n_samples>\n{n_samples}\n</n_samples>\n{tags_string}'
