import json
import re
from mcp_server.server import MCPServer
from memory.chroma import load_vectorstore
from memory.conversation import ConversationMemory

class ExecutorAgent:
    def __init__(self):
        self.mcp = MCPServer()
        self.db = load_vectorstore()
        self.chat_memory = ConversationMemory()

    def execute(self, decision_json: str, query: str):
        query_lower = query.lower()

        # 1️⃣ GREETING HANDLING (HIGHEST PRIORITY)
        greetings = ["hi", "hello", "hey", "hii", "hai"]
        if query_lower.strip() in greetings:
            name = self.chat_memory.get_name()
            if name:
                return f"Hi {name}! 😊 How can I assist you today?"
            return "Hi! 😊 How can I assist you today?"

        # 2️⃣ STORE NAME
        name_match = re.search(r"my name is (\w+)", query_lower)
        if name_match:
            name = name_match.group(1).capitalize()
            self.chat_memory.store_name(name)
            return f"Hi {name}, nice to meet you! How can I assist you?"

        # 3️⃣ RETRIEVE NAME
        if "what is my name" in query_lower:
            name = self.chat_memory.get_name()
            if name:
                return f"Your name is {name}."
            return "I don't know your name yet. Please tell me 😊"

        # 4️⃣ TOOL / KNOWLEDGE DECISION
        decision = json.loads(decision_json)

        if decision["action"] == "weather":
            return self.mcp.weather(decision["input"])

        if decision["action"] == "calculator":
            return self.mcp.calculator(decision["input"])

        # 5️⃣ KNOWLEDGE BASE (LAST OPTION)
        docs = self.db.similarity_search(query, k=1)
        return docs[0].page_content
