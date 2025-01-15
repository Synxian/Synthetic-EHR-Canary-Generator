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