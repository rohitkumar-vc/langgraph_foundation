from typing import TypedDict, Literal
import random

from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    curr_state: str

def node_1(state: State) -> str:
    return {"curr_state": state["curr_state"] + ", I am"}

def node_2(state: State) -> str:
    return {"curr_state": state["curr_state"] + " a graph"}

def node_3(state: State) -> str:
    return {"curr_state": state["curr_state"] + " a state graph"}

def conditional_edge(state: State) -> Literal["node_2", "node_3"]:
    return random.choice(["node_2", "node_3"])


builder = StateGraph(State)

# add nodes
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# add edges
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", conditional_edge)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

if __name__ == "__main__":
    graph = builder.compile()
    result = graph.invoke({"curr_state": "Hello"})
    print(result)