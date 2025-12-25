from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional
import subprocess

load_dotenv()
client = OpenAI()

INSTRUCTIONS='''
    You're an expert AI assistant in resolving user queries using chain of thought.
    You work on a START, PLAN, TOOL and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps. 
    You can also call a  TOOL to execute the plan and resolve user queries.
    The TOOL can be a function defined in some python module which is mentioned in the list of available tools. 
    Once you are done with planning and a possible use of TOOLS, you can give the OUTPUT. 
    After running the TOOL, wait for the OBSERVE step which is the output from the TOOL called

    ***RULES:
    - Strictly follow the JSON format
    - Only run one step at a time. 
    - The sequence of steps is START(where user gives the input), PLAN(Where you split the problem into parts, analyse and it a nd figure out a way to solve it.), TOOL(Need based use of given functions or utilities to resolve user queries), OUTPUT(The final output.)

    OUTPUT JSON FORMAT:
    {"step": "START"|"PLAN"|"TOOL"|"OUTPUT", "content":"string", "tool":"string", "city": "string", "input": "string"}
'''

AVAILABLE_TOOLS='''
 -get_weather: Takes city name as an input string and returns the weather information about the city.
 -run_cmd: Executes the given command on the terminal
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

SYSTEM_PROMPT = INSTRUCTIONS + AVAILABLE_TOOLS + EXAMPLES

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


def call_openai_api(client: OpenAI, messages: list=[], model="gpt-4o"):
    if client is None:
        return '{"step": "OUTPUT", "content": "API client not initiated"}'

    print(f"-----Calling model {model}-----")

    response = client.chat.completions.parse(
        model=model,
        response_format=MyOutputFormat,
        messages=messages,  # <--- FIXED: Passed directly, not wrapped!
        temperature=0.0
    )

    return response.choices[0].message.parsed

# Initialize History
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

available_tools = {"get_weather": get_weather, 
                   "run_cmd": run_cmd}

user_prompt = input("👉🏼 ")
message_history.append({"role": "user", "content": user_prompt})

while True:



    # Call API

    # 3. FIXED ROLE: OpenAI strictly requires 'assistant' for the bot's role

    try:
        parsed_response = call_openai_api(client, messages=message_history)
        message_history.append({"role": "assistant", "content": parsed_response.model_dump_json()})
        
        if parsed_response.step == 'START':
            print(f"🔥 {parsed_response.content}")
            continue
        elif parsed_response.step == 'PLAN':
            print(f"🧠 {parsed_response.content}")
            message_history.append({"role": "assistant", "content": parsed_response.content})
        elif parsed_response.step == 'TOOL':  
            tool_to_call = parsed_response.tool
            tool_input = parsed_response.input
            print(f"🛠️ {tool_to_call}({tool_input})")
            tool_response = available_tools[tool_to_call](tool_input)
            message_history.append({"role": "developer", "content": json.dumps({"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response})})
        elif parsed_response.step == 'OUTPUT':
            print(f"➡️ {parsed_response.content}")
            break
        else:
            # Fallback if the model forgets the 'step' key
            print(f"🤖 {parsed_response.content}")

    except json.JSONDecodeError:
        print(f"⚠️ Error parsing JSON: {parsed_response}")

# Inside the folder named todo_app can you create a todo app using html, css, js while using all crud operations. Also add a feature to toggle dark mode. Keep the theme as orange
