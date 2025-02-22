# src/core/memory.py
from langchain.memory import ConversationBufferMemory

def get_memory() -> ConversationBufferMemory:
    """Create and return a conversation memory instance."""
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )