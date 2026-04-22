import asyncio
import pandas as pd
import argparse
import os
import sys
import json
import subprocess

temperature = "0" # eval for reproducibility

models = ["qwen/qwen3-next-80b-a3b-thinking"] 
for model in models:
    cmd = [
                sys.executable,  
                "prompt_openrouter.py",
                "--file", "task2_ucp/dataset/intermediate/Chinese_prompt4_eval.csv", 
                "--model", model,
                "--temperature", temperature,
                "--content-column", "prompt_chinese",
                "--output-dir", "task2_ucp/dataset/result/",
            ]

    print("Running:", " ".join(cmd))
            # Call prompt_openrouter.py
    subprocess.run(cmd, check=True)

    