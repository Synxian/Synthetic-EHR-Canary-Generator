import os
import json
import asyncio
import argparse
import itertools
import traceback
from tqdm.asyncio import tqdm as atqdm
from tqdm import tqdm
from dotenv import load_dotenv
from openai import RateLimitError
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StdOutCallbackHandler
from meddocan import meddocan_prompt
from utils import read_json, write_xml, prepare_input
load_dotenv()

async def run_async_process(llm, output_dir, input_file, n_samples, mode, prompts):
    semaphore = asyncio.Semaphore(20)
    inputs = read_json(input_file)
    if mode == 'single':
        chain = prompts[mode] | llm
        files = await asyncio.gather(
            *(
                generate_canaries(chain, output_dir, inputs, semaphore)
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
    elif mode == 'history':
        await atqdm.gather(
            *(
                generate_canaries_story(llm, output_dir, inputs[i], semaphore,\
                    n_samples, i+1, prompts)
                for i in range(len(inputs))
            ),
            desc='Generating histories'
        )

async def generate_canaries(chain, output_dir, inputs, semaphore):
    os.makedirs(output_dir, exist_ok=True)
    requests = [ai_request(chain, prepare_input(input), semaphore) for input in inputs]
    files = await atqdm.gather(*requests, desc='Generating canaries')
    return [file for file in files if file is not None]

async def generate_canaries_story(llm, output_dir, input, semaphore, n_samples, set, prompts):
    os.makedirs(output_dir, exist_ok=True)
    base_chain = prompts['single'] | llm
    base = await ai_request(base_chain, prepare_input(input), semaphore)
    file = base.content
    write_xml(f'{output_dir}/canary_{set}_1.xml', file)
    chain = prompts['history'] | llm
    for i in tqdm(range(1, n_samples), desc=f'Generating history {set}'):
        response = await ai_request(chain, file, semaphore)
        file = response.content
        write_xml(f'{output_dir}/canary_{set}_{i+1}.xml', file)

async def ai_request(chain, input, semaphore):
    attempts = 0
    while attempts < 3:
        async with semaphore:
            try:
                req = await chain.ainvoke(
                    {"user_input": input}
                )
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

def set_callback_handler():
    handler = StdOutCallbackHandler()
    return handler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your program description')

    parser.add_argument(
        '-o',
        '--output_dir',
        help='Directory to save generated canaries',
        default='generated_canaries'
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
        help='Model temperature',
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
        prompts = {'single': meddocan_prompt('single'), 'history': meddocan_prompt('history')}
    asyncio.run(
        run_async_process(
            llm, args.output_dir, args.input_file, args.n_samples, args.mode, prompts
        )
    )
