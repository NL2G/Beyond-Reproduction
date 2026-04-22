import asyncio
import pandas as pd
import argparse
import os
import sys
import json
import subprocess
'''
task 1 code: 
python ../prompt_openrouter.py --file task1_prompt.csv --model anthropic/claude-3.7-sonnet:thinking --content-column prompt --output-dir task1_bench/ &
'''

temperature = "0.3"
content_columns = ["prompt"]

df = pd.read_csv("model_list_ablation.txt", header=None, names=["model"])
models = df["model"].tolist()
print(models)

for model in models:
    for col in content_columns:
        cmd = [
                sys.executable,  # same python interpreter
                "../prompt_openrouter.py",
                "--file", "task1_dataset/adversarial_task1_prompt.csv", #"task1_prompt.csv", 
                "--model", model,
                "--temperature", temperature,
                "--content-column", col,
                "--output-dir", "task1_adversarial_bench_result/", #task1_bench_result/
            ]

        print("Running:", " ".join(cmd))
            # Call prompt_openrouter.py
        subprocess.run(cmd, check=True)