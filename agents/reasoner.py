from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class ReasoningAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )

    def decide(self, query: str):
        prompt = f"""
Decide how to answer the query below.

Query: "{query}"

Respond ONLY in JSON:
{{
  "action": "weather" | "calculator" | "knowledge",
  "input": "string"
}}
"""
        # NEW LANGCHAIN API
        response = self.llm.invoke(prompt)
        return response.content
