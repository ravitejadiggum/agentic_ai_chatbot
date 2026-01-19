from langgraph.graph import StateGraph, END

from agents.planner import PlannerAgent
from agents.reasoner import ReasoningAgent
from agents.executor import ExecutorAgent

# Initialize agents
planner = PlannerAgent()
reasoner = ReasoningAgent()
executor = ExecutorAgent()

# -----------------------
# Graph node functions
# -----------------------

def plan(state: dict) -> dict:
    """
    Planner agent:
    Prepares initial state
    """
    return {
        "query": state["query"]
    }


def reason(state: dict) -> dict:
    """
    Reasoning agent:
    Decides whether to use tool or knowledge
    """
    decision = reasoner.decide(state["query"])
    return {
        "query": state["query"],
        "decision": decision
    }


def execute(state: dict) -> dict:
    """
    Executor agent:
    - Handles conversation memory
    - Calls tools if needed
    - Queries ChromaDB if needed
    """
    result = executor.execute(
        state["decision"],   # JSON from reasoning agent
        state["query"]       # original user query
    )

    return {
        "result": result
    }

# -----------------------
# Build LangGraph
# -----------------------

graph = StateGraph(dict)

graph.add_node("planner", plan)
graph.add_node("reasoner", reason)
graph.add_node("executor", execute)

graph.set_entry_point("planner")

graph.add_edge("planner", "reasoner")
graph.add_edge("reasoner", "executor")
graph.add_edge("executor", END)

# Compile agent
agent = graph.compile()
