'''
generate task1 prompts
requires:
- task1_annotation.csv (columns: book, quote, context, pre)
python task1_prompt_gen.py

On README.md, add:
- task1_prompt.csv (columns: book, quote, context, pre, prompt)
To generate the prompts for task1 autotask, run:
python task1_prompt_gen.py

Step 1: Generate the prompts
python task1_prompt_gen.py

Step 2: Run the benchmark prompts individually for specific models
python ../prompt_openrouter.py --file task1_prompt.csv --model anthropic/claude-3.7-sonnet:thinking --content-column prompt --output-dir task1_bench/ &


Or run all models with a predefined model list:
python batch_task1_run.py (attention: this will take a long time to run and consume a lot of API tokens!)

'''
import pandas as pd
df = pd.read_csv('task1_dataset/task1_annotation.csv')
print(df.columns)
df["pre"] = df.apply(lambda x: str(int(x["idx_claim"])) + "." + x["Claim"], axis =1)
print(df.shape)

df_task1 = df.groupby(["book", "quote", "context"], as_index=False)["pre"].agg("; ".join)

prompt_template = '''You are an expert in literary analysis and translation. Your task is to evaluate a set of claims based on the provided literary context and a direct quotation.
You may use your general literary knowledge where relevant, but your reasoning must be explicit and grounded in the given context and quote.

For each claim, determine whether it is True or False, and clearly justify your judgment.

Context:
{context}

Quote:
{quote}

Claims:
{claims}

Output Format: Return the result as a JSON array, where each element corresponds to one claim and has the following fields:
[
  {{
    "idx": 1,
    "judgment": "True",
    "reasoning": "Your detailed justification here."
  }}
]

Important Instructions:
Base your judgment primarily on the provided context and quote.
External literary knowledge may be used only if it supports or clarifies the interpretation.
The reasoning must explicitly explain why the claim is true or false.
Do not include any text outside the JSON output.
'''

for idx, row in df_task1.iterrows():
    prompt_ = prompt_template.format(context = row["context"], quote = row["quote"], 
    claims = row["pre"])
    df_task1.loc[idx, "prompt"] = prompt_

df_task1.to_csv("task1_dataset/task1_prompt.csv", index = False)