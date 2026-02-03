from langchain.messages import AnyMessage
from typing_extensions import TypedDict
from langgraph.graph import add_messages, StateGraph, START, END
from dotenv import load_dotenv
from typing import Annotated, Optional

from langchain.chat_models import init_chat_model  
from langchain_core.messages import trim_messages
import datetime
import json



load_dotenv()

llm = init_chat_model(
    model='gpt-4.1-mini', 
    model_provider="openai"
)

trimmer = trim_messages(strategy="last", 
                        token_counter=llm,
                        max_tokens=1000, 
                        start_on='human',
                        include_system=True
)

class llmSession(TypedDict):
    history : Annotated[list, add_messages]
    userQuery: Optional[str]
    rating: Optional[float]
    timestamp: Optional[str]

    

graph_builder = StateGraph(llmSession)


#NODES
def processQuery(session: llmSession):

    # Do some processing and update the state
    response = llm.invoke(input=session.get('userQuery'))
    print("Response", response.content)
    print("***********\n")
    rating = float(input('Rate the current response out of 10: '))
    session['rating'] = rating
    return {'history': [response], 'timestamp': datetime.datetime.now().strftime("%d %B, %Y %I:%M %p")}

def sampleNode(state: llmSession):

    return {'messages': ['Sample message appended']}

def chatWithLLM(session: llmSession):
    userQuery = input("\n\nEnter your query -> ")
    session["userQuery"] = userQuery
    return session

def exitChat(session: llmSession):
    
    return {'history': ['Exiting the chat session']}

#Exit condition evaluator
def exit(session: llmSession)  -> bool:
    userQuery = session["userQuery"]
    
    return True if userQuery.lower() == "exit" else False


#Adding the nodes
graph_builder.add_node("Initiator", chatWithLLM)
graph_builder.add_node("processor", processQuery)
graph_builder.add_node("acknowledgement", sampleNode)
graph_builder.add_node("exitChat", exitChat)

#Mapping the graph
graph_builder.add_edge(START, "Initiator")
graph_builder.add_conditional_edges(
    "Initiator", 
    exit,
    {
        True: "exitChat",
        False: "processor"
    }

)
graph_builder.add_edge("Initiator", "processor")
graph_builder.add_edge("processor", "acknowledgement")

graph_builder.add_conditional_edges(
    "acknowledgement", 
    exit,
    {
        True: "exitChat",
        False: "Initiator"
    }

)
graph_builder.add_edge("exitChat", END)

graph = graph_builder.compile()

# to start the workflow -> invoke(init_state)
updated_state = graph.invoke(llmSession({'messages': ['Hi, my name is Sam']}))


def serialize_state(state):
    # If state is a Pydantic model (not a dict), convert it first
    if hasattr(state, "model_dump"):
        state = state.model_dump()
    elif hasattr(state, "dict"):
        state = state.dict()
    
    # Create a new dict to avoid modifying the original state in memory
    serializable_state = state.copy()
    
    # Manually convert the 'messages' list if it exists
    if "messages" in serializable_state:
        serializable_state["messages"] = [
            # .model_dump() converts LangChain messages to pure dicts
            msg.model_dump() if hasattr(msg, "model_dump") else msg 
            for msg in serializable_state["messages"]
        ]
        
    return serializable_state

clean_state = serialize_state(updated_state)
print(f"Updated state: {updated_state}")
# LOG_FILE = '/Users/sohammehta/Full_stack_AI/AI/langgraph_learning/output.log'
# with open(LOG_FILE, 'a') as f:
#     json_object = json.loads(clean_state)
#     json.dump(json_object, f)
#     # f.write(updated_state)
#     f.write(2*"***************************\n")