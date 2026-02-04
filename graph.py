from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from state import State, Plan, Task
from nodes import orchestrator, worker, reducer, fanout

def build_graph():
    g = StateGraph(State)
    g.add_node("orchestrator", orchestrator)
    g.add_node("worker", worker)
    g.add_node("reducer", reducer)
    g.add_edge(START, "orchestrator")
    g.add_conditional_edges("orchestrator", fanout, ["worker"])
    g.add_edge("worker", "reducer")
    g.add_edge("reducer", END)
    return g.compile()
