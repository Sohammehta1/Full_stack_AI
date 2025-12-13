import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API key loaded")
else:
    print("API key not loaded")

client: OpenAI = None
try:
    client  = OpenAI()
except Exception as e:
    print(f"Exception {e}")

COT_INSTRUCTION="Let's think step by step to ensure that the calculation is correct"

PROBLEM_STATEMENT = """
A store sells a shirt for $50. A customer buys it for $50 cash. The cashier takes the $50 bill and goes next door to break it at a different store. The cashier returns and gives the customer the shirt and $20 change. Later, the owner of the store next door realizes the $50 bill was counterfeit and demands $50 back from the first store's owner. How much money did the first store owner lose in total?
"""

def call_openai_api(client: OpenAI, prompt_text: str, model="gpt-3.5-turbo"):
    result: any
    if client is None:
        result= "API client not initiated"
    else:
        print(f"-----Calling model {model}-----")

        response= client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", 
                 "content": prompt_text}
            ], 
            temperature=0.0
        )

        return response.choices[0].message.content

## A. Prompt WITHOUT Chain-of-Thought (Baseline)
prompt_no_cot = PROBLEM_STATEMENT

print("## 1. Output WITHOUT CoT\n")
output_no_cot = call_openai_api(client, prompt_no_cot)
print(output_no_cot)

print("\n" + "="*50 + "\n")

## B. Prompt WITH Chain-of-Thought (CoT)
prompt_with_cot = PROBLEM_STATEMENT + "\n\n" + COT_INSTRUCTION

print("## 2. Output WITH CoT\n")
output_with_cot = call_openai_api(client, prompt_with_cot)
print(output_with_cot)
        