# tests/conftest.py
import pytest
from unittest.mock import Mock
from langchain.schema import BaseMemory
from src.config.settings import Settings, get_settings
from src.core.llm import CreditCardAssistant
from src.core.vector_store import DocumentStore
from src.utils.cache import Cache
from src.utils.metrics import MetricsTracker

@pytest.fixture
def test_settings():
    """Fixture for test settings."""
    return Settings(
        OPENAI_API_KEY="test-key",
        ENABLE_TRACING=False,
        ENABLE_METRICS=False,
        VECTOR_STORE_PATH="./test_vector_store",
        UPLOAD_FOLDER="./test_uploads"
    )

@pytest.fixture
def mock_memory():
    """Fixture for mocked conversation memory."""
    memory = Mock(spec=BaseMemory)
    memory.load_memory_variables.return_value = {"chat_history": []}
    return memory

@pytest.fixture
def mock_cache():
    """Fixture for mocked cache."""
    return Mock(spec=Cache)

@pytest.fixture
def mock_metrics():
    """Fixture for mocked metrics tracker."""
    return Mock(spec=MetricsTracker)

@pytest.fixture
def assistant(mock_memory, mock_cache, mock_metrics):
    """Fixture for credit card assistant with mocked dependencies."""
    return CreditCardAssistant(
        memory=mock_memory,
        cache=mock_cache,
        metrics_tracker=mock_metrics
    )

@pytest.fixture
def doc_store():
    """Fixture for document store."""
    return DocumentStore()