import os
import json
import asyncio
import argparse
import itertools
import traceback
from tqdm.asyncio import tqdm
from dotenv import load_dotenv
from openai import RateLimitError
from meddocan import meddocan_prompt
from utils import read_json, write_xml
from langchain_openai import ChatOpenAI
load_dotenv()


async def run_async_process(chain, output_dir, input_file, n_samples):
   semaphore = asyncio.Semaphore(20)
   files = await asyncio.gather(
      *(
            generate_canaries(chain, output_dir, input_file,semaphore)
            for i in range(n_samples)
        )
   )
   files = list(itertools.chain(*files))
   for i in range(len(files)):
      try:
        write_xml(f'{output_dir}/canary_{i+1}.xml', files[i].content)
      except Exception as e:
        print(f'Error writing file: {i}. \n {e}')
        continue

async def generate_canaries(chain, output_dir, input_file, semaphore):
  os.makedirs(output_dir, exist_ok=True)
  inputs = read_json(input_file)
  requests = [process_input(chain, input, semaphore) for input in inputs]
  files = await tqdm.gather(*requests, desc='Generating canaries')
  return [file for file in files if file is not None]

async def process_input(chain, input_data, semaphore):
  attempts = 0
  while attempts < 3:
      async with semaphore:
          try:
              req = await chain.ainvoke({"user_input": input_data})
              return req
          except (json.JSONDecodeError, KeyError) as e:
              print(f'Attempt {attempts + 1} failed: "{type(e).__name__}: {str(e)}"')
              attempts += 1
          except RateLimitError:
              print("Rate limited, reattempting in 10s")
              await asyncio.sleep(10)
              attempts += 1
          except Exception:
              traceback.print_exc()
              attempts += 1
  return None

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Your program description')

  parser.add_argument(
    '-o',
    '--output_dir',
    help='Directory to save generated canaries'
  )
  parser.add_argument(
    '-d',
    '--dataset',
    help='The reference dataset for canary generation',
    default='meddocan'
  )
  parser.add_argument(
    '-i',
    '--input_file',
    help='JSON file for the canaries options'
  )
  parser.add_argument(
    '-t',
    '--temperature',
    type=float,
    help='GPT temperature',
    default=0.5
  )
  parser.add_argument(
    '-n',
    '--n_samples',
    type=int,
    help='How many canaries for each set of tags to make'
  )
  args = parser.parse_args()


  model_name = "gpt-4o-mini"
  llm = ChatOpenAI(model=model_name, temperature=args.temperature)
  if args.dataset == 'meddocan':
    chain = meddocan_prompt() | llm
  asyncio.run(
    run_async_process(chain, args.output_dir, args.input_file, args.n_samples)
  )
