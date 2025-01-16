import os
import json
import asyncio
import argparse
import itertools
import traceback
from tqdm.asyncio import tqdm
from dotenv import load_dotenv
from openai import RateLimitError
from langchain_openai import ChatOpenAI
from meddocan import meddocan_prompt
from utils import read_json, write_xml, prepare_input
load_dotenv()

async def run_async_process(chain, output_dir, input_file, n_samples, mode):
    semaphore = asyncio.Semaphore(20)
    inputs = read_json(input_file)
    if mode == 'single':
        files = await asyncio.gather(
            *(
                generate_canaries(chain, output_dir, inputs, semaphore, mode)
                for i in range(n_samples)
            )
        )
    else:
        files = await tqdm.gather(
            *(
                generate_canaries(chain, output_dir, [input], semaphore, mode, n_samples)
                for input in inputs
            ),
            desc='Generating histories'
        )
    files = list(itertools.chain(*files))
    for i in range(len(files)):
        try:
            if mode == 'single':
                write_xml(f'{output_dir}/canary_{i+1}.xml', files[i].content)
            else:
                list_of_files = json.loads(files[i].content)['documents']
                for j in range(len(list_of_files)):
                    write_xml(f'{output_dir}/canary_{i+1}_{j+1}.xml', list_of_files[j])
        except Exception as e:
            print(f'Error writing file: {i}. \n {e}')
            continue

async def generate_canaries(chain, output_dir, inputs, semaphore, mode, n_samples=0):
    os.makedirs(output_dir, exist_ok=True)
    requests = [process_input(chain, input, semaphore, mode, n_samples) for input in inputs]
    files = await tqdm.gather(*requests, desc='Generating canaries')
    return [file for file in files if file is not None]

async def process_input(chain, input_data, semaphore, mode, n_samples):
    attempts = 0
    while attempts < 3:
        async with semaphore:
            try:
                req = await chain.ainvoke({"user_input": prepare_input(input_data, mode, n_samples)})
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
        '-m',
        '--mode',
        type=str,
        choices=['single', 'history'],
        help='''Mode for the canaries generation.
        Single is for single entries.
        History is to generate a thread of connected medical visits for each set of tags.
        ''',
        default='single'
    )
    parser.add_argument(
        '-n',
        '--n_samples',
        type=int,
        help='''How many canaries for each set of tags to make.
        If mode is single, it will generate n_samples for each set of tags.
        If mode is history, it will generate an history composed of n_samples for each set of tags.
        ''',
    )
    args = parser.parse_args()


    model_name = "gpt-4o-mini"
    llm = ChatOpenAI(model=model_name, temperature=args.temperature)
    if args.dataset == 'meddocan':
        chain = meddocan_prompt(args.mode) | llm
    asyncio.run(
        run_async_process(
            chain, args.output_dir, args.input_file, args.n_samples, args.mode
        )
    )
