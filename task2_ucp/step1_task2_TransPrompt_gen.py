import pandas as pd
import argparse

#python3 step1_task2_TransPrompt_gen.py --language Chinese

parser = argparse.ArgumentParser(description='Process prompts from a CSV file.')
parser.add_argument('--test', type=int, default=0, required=False, help='test size')
parser.add_argument("--language", type=str)
args = parser.parse_args()
test = args.test
language = args.language

prompt_template_base = """Please translate the following literary excerpt into {language}. 

Excerpt:
{excerpt}

Output only the {language} translation.
"""

prompt_template_1 = """You are a literary translator. Your goal is to translate the source text into {language} in a way that preserves its meaning, tone, stylistic effects, imagery, voice, and cultural nuance, while producing a fluent and natural target-language text. 

Excerpt:
{excerpt}

Output only the {language} translation.
"""

prompt_template_2 = """You are a literary translator. Your goal is to translate the source text into {language} in a way that preserves its meaning, tone, stylistic effects, imagery, voice, and cultural nuance, while producing a fluent and natural {language} text. You should balance fidelity to the original with selective creative decisions that help recreate literary effects for {language} readers. When a literal rendering would lose nuance or sound awkward, you may adjust expressions or imagery that suits the context.

Excerpt:
{excerpt}

Output only the {language} translation.
"""

prompt_template_3 = """You are a literary translator. This source text is highly creative, and your translation should reflect that creativity in {language}. You may employ Creative Shifts, meaning purposeful departures from a literal rendering that create a more impactful, natural, or culturally resonant translation whenever they meaningfully enhance the literary effect. Maintain the core meaning and emotional intent of the original while allowing yourself broad stylistic freedom.

Excerpt:
{excerpt}

Output only the {language} translation.
"""

df = pd.read_csv("dataset/task2_benchmark_fewshot.csv", sep = ";")
if test>0:
        df = df.loc[:test]
print(f"Processing {len(df)} paragraphs")

lst = []

for i, row in df.iterrows():
    base = prompt_template_base.format(excerpt=row["source"], language = language)
    p1 = prompt_template_1.format(excerpt=row["source"], language = language)
    p2 = prompt_template_2.format(excerpt=row["source"], language = language)
    p3 = prompt_template_3.format(excerpt=row["source"], language = language)
    lst.append((base, p1, p2, p3))

df_ = pd.DataFrame(lst, columns=["base", "p1", "p2", "p3"])
pd.concat([df, df_], axis = 1).to_csv(f"dataset/intermediate/{language}_prompt4_translation.csv".format(language = language), index=False)

    