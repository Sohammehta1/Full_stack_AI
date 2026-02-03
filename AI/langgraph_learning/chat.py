from langchain.messages import AnyMessage
from typing_extensions import TypedDict
from langgraph.graph import add_messages, StateGraph, START, END
from dotenv import load_dotenv
from typing import Annotated

from langchain.chat_models import init_chat_model  

load_dotenv()

llm = init_chat_model(
    model='gpt-4.1-mini', 
    model_provider="openai"
)

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    llm_calls: int

graph_builder = StateGraph(MessagesState)

def chatNode(state: MessagesState):

    # Do some processing and update the state
    response = llm.invoke(input=state.get('messages'))
    return {'messages': [response]}

def sampleNode(state: MessagesState):

    return {'messages': ['Sample message appended']}

graph_builder.add_node("chatNode", chatNode)
graph_builder.add_node("sampleNode", sampleNode)

graph_builder.add_edge(START, "chatNode")
graph_builder.add_edge("chatNode", "sampleNode")
graph_builder.add_edge("sampleNode", END)

graph = graph_builder.compile()

# to start the workflow -> invoke(init_state)
updated_state = graph.invoke(MessagesState({'messages': ['Hi, my name is Sam']}))
print(f"Updated state: {updated_state}")