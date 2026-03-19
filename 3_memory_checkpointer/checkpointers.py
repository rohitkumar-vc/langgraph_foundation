import random

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from get_llm import get_model
from pretty_print import print_langchain_messages

def generate_product_id() -> int:
    "Generate a random ID for the product"
    return random.randint(1, 100)

def add_product_to_card(product_id: int) -> str:
    "Simulate adding a product to a shopping cart"
    with open("cart.md", "a") as f:
        f.write(f"Added ITEM-{product_id} to your cart.\n")
    return f"Added ITEM-{product_id} to your cart."

def llm_with_tool(state: MessagesState) -> str:
    "Simulate an LLM that calls a tool to generate a product ID"
    llm = get_model()
    llm_with_tool = llm.bind_tools([generate_product_id, add_product_to_card])
    return {"messages": [llm_with_tool.invoke(state["messages"])]}

# define the graph
builder = StateGraph(MessagesState)

memory = InMemorySaver()

# add nodes
builder.add_node("llm_with_tool", llm_with_tool)
builder.add_node("tools", ToolNode([generate_product_id, add_product_to_card]))

# add edges
builder.add_edge(START, "llm_with_tool")
builder.add_conditional_edges("llm_with_tool", tools_condition)
builder.add_edge("tools", "llm_with_tool")
builder.add_edge("llm_with_tool", END)

if __name__ == "__main__":

    # adding this checkpointer saves the key value pairs of config, graph state in the memory for later use.
    graph = builder.compile(checkpointer=memory)

    configuration = {"configurable" : {"thread_id": "1"}}
    # normal with no tool calls
    # result = graph.invoke({"messages": ["Hello how are you?"]})
    # print_langchain_messages(result["messages"])

    # with tool calls
    result = graph.invoke({"messages": ["Generate a product ID for me."]}, configuration)
    print_langchain_messages(result["messages"])


    print("-" * 10 + " Testing Config " + "-" * 10)


    # now here we are not passing the previous messages yet it will be able to access the previous
    # messages and config from the memory checkpointer and give us the correct response.
    result2 = graph.invoke({"messages": ["Add the generated product id to the cart."]}, configuration)
    print_langchain_messages(result2["messages"])



