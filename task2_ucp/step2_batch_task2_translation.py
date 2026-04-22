import asyncio
import pandas as pd
import argparse
import os
import sys
import json
import subprocess

temperature = "0.7"
content_columns = ["base", "p1", "p2", "p3"]

df = pd.read_csv("../model_list.txt", header=None, names=["model"])
models = df["model"].tolist()
print(models)

for model in models:
    for col in content_columns:
        cmd = [
                sys.executable,  # same python interpreter
                "prompt_openrouter.py",
                "--file", "task2_ucp/dataset/intermediate/Chinese_prompt4_translation.csv",
                "--model", model,
                "--temperature", temperature,
                "--content-column", col,
                "--output-dir", "task2_ucp/dataset/Chinese/",
            ]

        print("Running:", " ".join(cmd))
            # Call prompt_openrouter.py
        subprocess.run(cmd, check=True)