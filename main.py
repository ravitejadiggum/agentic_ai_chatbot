from agent_graph import agent

while True:
    q = input("You: ")
    if q == "exit":
        break
    result = agent.invoke({"query": q})
    print("Agent:", result["result"])
