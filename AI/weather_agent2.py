import json
import os
import subprocess
from typing import Optional

from google import genai
import requests
from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv() # This loads the variables from .env into the system environment

geminiClient = genai.Client() # Now this works!

# geminiClient=genai.Client(api_key='GEMINI_API_KEY')

MODEL = "gemini-2.5-flash-lite"



INSTRUCTIONS='''
    You're an expert AI assistant.
    ***RULES:
    - Strictly follow the JSON format.
    - Only run one step at a time.
    - Sequence: START -> PLAN -> TOOL -> OUTPUT.    
'''

AVAILABLE_TOOLS='''
 -get_weather: Takes city name as an input (string)-> returns the weather information about the city.
 -run_cmd: Executes terminal command (string)
'''

EXAMPLES='''

    EXAMPLE1: 
    START: What is the weather in Oslo right now?
    PLAN: {step:"PLAN", "content": "Seems like user is interested in knowing the current weather in Oslo"}
    PLAN: {step:"PLAN", "content": "Lets see if we have a tool to fetch the current weather in Oslo"}
    TOOL: {step:"TOOL", "tool": "get_weather", "input": "Oslo"}
    PLAN: {step:"OBSERVE", "tool": "Seems like the weather in Oslo is chilly, 20 degree Celcius"}
    PLAN: {step:"PLAN", "content": "Great,I got the weather in Oslo"}=
    OUTPUT: {step:"OUTPUT", "content": "Hi, current weather in Olso is chilly with 20 degree Celcius."}

    EXAMPLE2:
    START: Make a directory named Krishna
    PLAN: {step:"PLAN", "content": "Seems like user wants to create a directory named Krishna"}
    PLAN: {step:"PLAN", "content": "Lets see if we have a tool to create a directory"}
    TOOL: {step:"TOOL", "tool": "run_cmd", "input": "mkdir Krishna"}
    PLAN: {step:"OBSERVE", "tool": "Directory named Krishna has been created"}
    OUTPUT: {step:"OUTPUT", "content": "Hi, directory Krishna has been created"}
'''



class MyOutputFormat(BaseModel):

    step: str = Field(description="The ID of the step. Example PLAN, TOOL, OUTPUT")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call ")
    input: Optional[str] = Field(None, description="The input parameters for the tool")

SYSTEM_PROMPT = INSTRUCTIONS + AVAILABLE_TOOLS

# def clean_schema(schema):
#     """Recursively removes 'default' keys from the schema dictionary."""
#     if isinstance(schema, dict):
#         return {k: clean_schema(v) for k, v in schema.items() if k != "default"}
#     elif isinstance(schema, list):
#         return [clean_schema(v) for v in schema]
#     return schema

# # 2. Convert Pydantic to a Dict and clean it manually
# raw_schema = MyOutputFormat.model_json_schema()
# cleaned_schema = clean_schema(raw_schema)


def run_cmd(cmd: str):
    result= "Command execution failed!"
    try:
        subprocess.run(cmd, shell=True)
        result = "Command execution was succesfull"
    except:
        pass
    return result


def get_weather(city: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(f"https://wttr.in/{city.lower()}?format=%C=%t")

        if response.status_code == 200:
            return response.text
        else:
            return "Error fetching weather"
    except Exception as e:
        return f"Connection Error {e}"


available_tools = {"get_weather": get_weather, 
                   "run_cmd": run_cmd}

# Initialize History
MESSAGE_HISTORY = []

def call_gemini(client: genai.Client , message: list=[]):
    if MODEL is None:
        return '{"step": "OUTPUT", "content": "API client not initiated"}'

    print(f"-----Calling model {MODEL}-----")

    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=message,
        config={
        "response_mime_type": "application/json",
        "response_json_schema": MyOutputFormat.model_json_schema(),
    },
    )
    recipe = MyOutputFormat.model_validate_json(response.text)
    # return MyOutputFormat(**(json.loads(response.text)))
    print(recipe)




# user_prompt = input("👉🏼 ")
# MESSAGE_HISTORY.append({"role": "user", "content": user_prompt})
# while True:
#     try:
#         parsed_response = call_gemini(geminiClient, message=MESSAGE_HISTORY)

#         if parsed_response.step == 'START':
#             print(f"🔥 {parsed_response.content}")
#             continue
#         elif parsed_response.step == 'PLAN':
#             print(f"🧠 {parsed_response.content}")
#             message = {"role": "user", "content": parsed_response.content}
#             MESSAGE_HISTORY.append(message)
#         elif parsed_response.step == 'TOOL':  
#             tool_to_call = parsed_response.tool
#             tool_input = parsed_response.input
#             print(f"🛠️ {tool_to_call}({tool_input})")
#             tool_response = available_tools[tool_to_call](tool_input)
#             message = {"role": "user", "content": json.dumps({"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response})}
#             MESSAGE_HISTORY.append(message)
#         elif parsed_response.step == 'OUTPUT':
#             print(f"➡️ {parsed_response.content}")
#             break
#         else:
#             # Fallback if the model forgets the 'step' key
#             print(f"🤖 {parsed_response.content}")

#     except json.JSONDecodeError:
#         print(f"⚠️ Error parsing JSON: {parsed_response}")

# Inside the folder named todo_app can you create a todo app using html, css, js while using all crud operations. Also add a feature to toggle dark mode. Keep the theme as orange

call_gemini(geminiClient, message="What is the temperature in Mumbai")