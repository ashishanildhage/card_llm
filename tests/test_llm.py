# tests/test_llm.py
import pytest
from unittest.mock import patch, Mock
from src.core.llm import CreditCardAssistant
from src.models.query import QueryRequest, QueryResponse

def test_assistant_initialization(assistant):
    """Test proper initialization of the assistant."""
    assert assistant is not None
    assert assistant.memory is not None
    assert assistant.cache is not None
    assert assistant.metrics is not None

@pytest.mark.asyncio
async def test_process_query_success(assistant):
    """Test successful query processing."""
    # Arrange
    query = "What are the reward points on Amazon purchases?"
    expected_response = "You earn 5% reward points on Amazon purchases."
    assistant.chain.run = Mock(return_value=expected_response)
    
    # Act
    response = await assistant.process_query(query)
    
    # Assert
    assert response.content == expected_response
    assert response.success is True
    assistant.metrics.track_query.assert_called_once()
    assistant.cache.get.assert_called_once_with(query)

@pytest.mark.asyncio
async def test_process_query_with_cache(assistant):
    """Test query processing with cache hit."""
    # Arrange
    query = "What are the card charges?"
    cached_response = "Annual fee is ₹500"
    assistant.cache.get.return_value = cached_response
    
    # Act
    response = await assistant.process_query(query)
    
    # Assert
    assert response.content == cached_response
    assert response.cached is True
    assistant.chain.run.assert_not_called()

@pytest.mark.asyncio
async def test_process_query_error_handling(assistant):
    """Test error handling during query processing."""
    # Arrange
    query = "Invalid query"
    assistant.chain.run.side_effect = Exception("LLM Error")
    
    # Act & Assert
    with pytest.raises(Exception):
        await assistant.process_query(query)
    assistant.metrics.track_error.assert_called_once()


