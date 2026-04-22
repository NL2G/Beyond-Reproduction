import asyncio
from fastllm import RequestBatch, RequestManager, OpenAIProvider, InMemoryCache, DiskCache
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description='Process prompts from a CSV file.')
parser.add_argument('--file', type=str, default="batch1_sample_prompt.csv", required=False, help='Path to the CSV file containing prompts')
parser.add_argument('--model', type=str, default="gpt-4o-mini", required=False, help='Model to use')
parser.add_argument('--temperature', type=float, default=0.3, help='Temperature for the model')
parser.add_argument('--content-column', type=str, default="prompt", required=False, help='Column name containing the content')
parser.add_argument('--output-dir', type=str, default="task2_bench/", help='Output directory')
parser.add_argument('--force', action='store_true', help='Force re-run even if results exist')
parser.add_argument('--test-size', type=int, default=None, help='test the number of prompts to process')

args = parser.parse_args()

# Load the CSV file
df = pd.read_csv(args.file)
if args.test_size:
    df = df.head(args.test_size)

api_key = ""
# Create a provider
provider = OpenAIProvider(
    api_key=api_key,
    api_base="https://openrouter.ai/api/v1", 
)

# Create a cache provider (optional)
cache = DiskCache(directory="./cache") 

# Create a request manager
manager = RequestManager(
    provider=provider,
    concurrency= 5 if args.test_size else 30,  
    show_progress=True,  # Show progress bar
    caching_provider=cache,  # Enable caching
    timeout=180.0,
    retry_attempts=5,
)

async def check_cache(request_ids):
    for request_id in request_ids:
        is_cached = await cache.exists(request_id)
        if is_cached:
            pass 
        else:
            print(f"Request {request_id} is not cached")

# Create a batch of requests
request_ids = []  # Store request IDs for later use
with RequestBatch() as batch:
    # Add requests to the batch
    for i in range(len(df)):
        # create() returns the request ID (caching key)
        request_id = batch.chat.completions.create(
            model=args.model,
            messages=[{
                "role": "user",
                "content": df.iloc[i][args.content_column]
            }],
            temperature=args.temperature,
            include_reasoning=True,  # Optional: include model reasoning
        )
        request_ids.append(request_id)

# Process the batch
responses = manager.process_batch(batch)
df["response"] = [response.response.choices[0].message.content for response in responses]
df["full_response"] = [response.response for response in responses]
df["request_id"] = [responce_id for responce_id in request_ids]
# add csv file name to the output directory
os.makedirs(args.output_dir, exist_ok=True)
output_file = args.output_dir + args.model.replace("/", "_") + "_" + args.file.split("/")[-1] + "_" + args.content_column + str(args.temperature)
df.to_csv(output_file, index=False)

# Process responses
for request_id, response in zip(request_ids, responses):
    if isinstance(response, Exception):
        print(f"Request {request_id} failed: {response}")
        
# Check cache status
asyncio.run(check_cache(request_ids))

