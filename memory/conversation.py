class ConversationMemory:
    def __init__(self):
        self.memory = {}

    def store_name(self, name: str):
        self.memory["name"] = name

    def get_name(self):
        return self.memory.get("name")
