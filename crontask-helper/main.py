#!/usr/bin/env python3
#coding: utf-8

#from ollama import generate
#from ollama._types import Options
#from ollama import ChatResponse
#from ollama import chat

import sys

from typing import List
from typing import Dict
from typing import Union
from typing import Tuple
from typing import Optional
from typing import Any


from agents import ask_agent
from agents import model_unload


def main(
    prompt: Optional[str] = None,
    execute: Optional[str] = None,
    model: Optional[str] = "qwen2.5:0.5b",
    ollama_base_url: Optional[str] = "http://localhost:11434",
    unload: Optional[bool] = False,
):
    try:
        ask_agent(prompt, execute, model, ollama_base_url)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if unload:
            model_unload(model, ollama_base_url)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CronTask Helper')
    parser.add_argument('-p', '--prompt', type=str, default=None, help='Explaination of the task to be done')
    parser.add_argument('-e', '--execute', type=str, default=None, help='Command to be executed')
    parser.add_argument('-m', '--model', type=str, default="qwen2.5:0.5b", help='Model to use')
    parser.add_argument('-u', '--ollama_base_url', type=str, default="http://localhost:11434", help='Ollama base URL')
    parser.add_argument('-U', '--unload', action='store_true', default=False, help='Unload the model after end of this script')
    args = parser.parse_args()

    try:
        main(
            prompt=args.prompt,
            execute=args.execute,
            model=args.model,
            ollama_base_url=args.ollama_base_url,
            unload=args.unload
        )
    except KeyboardInterrupt:
        print("Program interrupted by user", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)