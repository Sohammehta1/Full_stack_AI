import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client: OpenAI = None
try:
    client = OpenAI()
except Exception as e:
    print(f"Exception {e}")

# 1. UPDATED INSTRUCTION: Added instructions for the 'step' key so your Python logic works
COT_INSTRUCTION = '''
    You are an expert trip planner. 
    1. First, acknowledge the user request (step: START).
    2. Then, create a detailed plan (step: PLAN). 
    3. Finally, present the itinerary to the user (step: OUTPUT).
    
    Your role is to answer the queries of users who want to plan their trip.
'''

NOTE = '''
    NOTE ***
    Output JSON ONLY. Format:
    {"step": "START" | "PLAN" | "OUTPUT", "content": "<text content>"}
'''

NOTE2 = '''
    NOTE ***
    Continue the step plan until the user specifically prompts for final plan. 
    Only when the user asks for final plan, with their confirmation, give the OUTPUT step
'''

SYSTEM_INSTRUCTION = COT_INSTRUCTION + NOTE + NOTE2

# 2. FIXED FUNCTION: Pass 'messages' directly
def call_openai_api(client: OpenAI, messages: list, model="gpt-3.5-turbo"):
    if client is None:
        return '{"step": "OUTPUT", "content": "API client not initiated"}'
    
    print(f"-----Calling model {model}-----")

    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=messages,  # <--- FIXED: Passed directly, not wrapped!
        temperature=0.0
    )

    return response.choices[0].message.content

# Initialize History
message_history = [
    {"role": "system", "content": SYSTEM_INSTRUCTION}
]

while True:
    user_prompt = input("👉🏼 ")

    # Append user input
    message_history.append({"role": "user", "content": user_prompt})

    # Call API
    raw_response = call_openai_api(client, messages=message_history)
    
    # 3. FIXED ROLE: OpenAI strictly requires 'assistant' for the bot's role
    message_history.append({"role": "assistant", "content": raw_response})
    
    try:
        result = json.loads(raw_response)
        
        if result.get("step") == 'START':
            print(f"🔥 {result.get('content')}")
        elif result.get("step") == 'PLAN':
            print(f"🧠 {result.get('content')}")
        elif result.get("step") == 'OUTPUT':
            print(f"➡️ {result.get('content')}")
            break
        else:
            # Fallback if the model forgets the 'step' key
            print(f"🤖 {result.get('content')}")
            
    except json.JSONDecodeError:
        print(f"⚠️ Error parsing JSON: {raw_response}")

'''Hi, I want to plan a trip to Matheran on the 22th and 23th of December. we are 3 members in total, one is my mother and one is my brother. So one room for 1 night will be sufficient. We live in Pune and do not have a car. So could you plan a trip for us?'''
