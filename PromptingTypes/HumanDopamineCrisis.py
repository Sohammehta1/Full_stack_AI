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

COT_INSTRUCTION='''
1. Let's analyze this complex sociological question step-by-step. Assume the role of a Cultural Analyst.
2. **Define Key Terms:** First, clearly define the key concepts: "Gen Z" (approximate birth years) and "Existential Crisis" in a modern context.
3. **Analyze the "Neither/Nor" Conflict:** Identify the specific points of conflict where Gen Z stands between the "previous generation" (Boomers/Gen X) and the "ultra smart future."
    * *Factor A: Economic.* Analyze high student debt, housing affordability, and job market precarity compared to previous generations.
    * *Factor B: Digitalization and Social Media.* Analyze the effect of constant social comparison, performance culture, and the dissolution of physical community.
    * *Factor C: Global Crises.* Analyze the impact of climate change and political instability on their future outlook.
4. **Address the "Most Depressed" Claim:** Synthesize the analysis from steps 2 & 3. Explain *why* these factors uniquely compound to create a mental health crisis often labeled as "the most depressed generation," giving a nuanced conclusion instead of a single cause.
'''

PROBLEM_STATEMENT='''
    Why is it, that the generation right now, the so called Gen Zs are facing an existential crisis.
    In this era of digitalization, gen zs belong neither to the previous generation with their stubborn beliefs, 
    nor do they belong to the new ultra smart generation. But this problem would have happened with every generation.
    Why is the current generation being called the most depressed generation ever.
'''

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
