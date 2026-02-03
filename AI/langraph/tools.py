from langchain_ollama import ChatOllama
from langchain.tools import tool


model = ChatOllama(model='gemma3:1b')

# Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b

@tool
def sub(a: int, b: int) -> int:
    """Subtracts `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a - b


tools = [multiply, add, divide, sub]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools_by_name)