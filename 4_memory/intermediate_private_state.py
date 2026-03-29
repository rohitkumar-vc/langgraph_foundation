# private states are the states that are not userful for the user in input and output 
# but are important for the agents in intermediate states

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class OverallState(TypedDict):
    io: str
    
class PrivateState(TypedDict):
    intermeditate: str
    
def node_1(state: OverallState) -> PrivateState:
    print("--Node 1--")
    return {"intermeditate" : state["io"] + " hello"}

def node_2(state: PrivateState) -> OverallState:
    print("-- Node 2 --")
    return {"io" : state["intermeditate"] + " World"}


# here we can have different input and output state by specifying input_schema, output_schema to achieve input and output filters.
# to achieve this we have to take input to the first node as input schema and output to the last node as output schema

"""
class StateGraph(
    state_schema: type[OverallState],
    context_schema: type[None] | None = None,
    *,
    input_schema: type[OverallState] | None = None,
    output_schema: type[OverallState] | None = None,
    **kwargs: **DeprecatedKwargs
)
"""

builder = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

graph = builder.compile()

response = graph.invoke({"io" : "start"})

print(response)



