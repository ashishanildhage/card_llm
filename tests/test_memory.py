# tests/test_memory.py
import pytest
from src.core.memory import get_memory

def test_memory_initialization():
    """Test conversation memory initialization."""
    # Act
    memory = get_memory()
    
    # Assert
    assert memory is not None
    assert memory.memory_key == "chat_history"
    assert memory.return_messages is True

def test_memory_save_and_load():
    """Test saving and loading memory variables."""
    # Arrange
    memory = get_memory()
    test_input = {"human_input": "test question"}
    
    # Act
    memory.save_context(test_input, {"assistant": "test response"})
    result = memory.load_memory_variables({})
    
    # Assert
    assert "chat_history" in result
    assert len(result["chat_history"]) > 0