import os
import json
import asyncio
import argparse
import traceback
from tqdm import tqdm
from dotenv import load_dotenv
from openai import RateLimitError
from meddocan import meddocan_prompt
from utils import read_json, write_xml
from langchain_openai import ChatOpenAI
load_dotenv()

async def generate_canaries(chain, output_dir, input_file):
  os.makedirs(output_dir, exist_ok=True)
  inputs = read_json(input_file)
  attempts = 0
  for i in tqdm(range(len(inputs)), desc='Generating canaries'):
    try:
      res = chain.invoke({"user_input": inputs[i]})
      write_xml(f'{output_dir}/canary_{i+1}.xml', res.content)
    except (json.JSONDecodeError, KeyError) as e:
        print(
            f'Attempt {attempts  + 1} failed with error: "{type(e).__name__}: {str(e)}"'
        )
        attempts += 1
    except RateLimitError:
        print("Rate limited, reattempting in 10s")
        await asyncio.sleep(10)
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Your program description')

  parser.add_argument(
    '--output_dir',
    help='Directory to save generated canaries'
  )
  parser.add_argument(
    '--dataset',
    help='The reference dataset for canary generation',
    default='meddocan'
  )
  parser.add_argument(
    '--input_file',
    help='JSON file for the canaries options'
  )
  parser.add_argument(
    '-t',
    '--temperature',
    type=float,
    help='GPT temperature',
    default=0
  )
  args = parser.parse_args()

  
  model_name = "gpt-4o-mini"
  llm = ChatOpenAI(model=model_name, temperature=args.temperature)
  if args.dataset == 'meddocan':
    chain = meddocan_prompt() | llm
  asyncio.run(
    generate_canaries(chain, args.output_dir, args.input_file)
  )
