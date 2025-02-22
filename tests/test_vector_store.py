# tests/test_vector_store.py
import pytest
import os
from src.core.vector_store import DocumentStore

@pytest.fixture
def sample_pdf(tmp_path):
    """Create a sample PDF file for testing."""
    pdf_path = tmp_path / "test.pdf"
    # Create minimal PDF content
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n")
    return str(pdf_path)

def test_document_store_initialization(doc_store):
    """Test proper initialization of document store."""
    assert doc_store is not None
    assert doc_store.embeddings is not None
    assert doc_store.vector_store is None

def test_add_document_success(doc_store, sample_pdf):
    """Test successful document addition."""
    # Act
    doc_store.add_document(sample_pdf)
    
    # Assert
    assert doc_store.vector_store is not None

def test_query_document_no_documents(doc_store):
    """Test querying when no documents are loaded."""
    # Act
    result = doc_store.query_document("test query")
    
    # Assert
    assert "No documents available" in result

def test_query_document_with_documents(doc_store, sample_pdf):
    """Test document querying with loaded documents."""
    # Arrange
    doc_store.add_document(sample_pdf)
    
    # Act
    result = doc_store.query_document("test query")
    
    # Assert
    assert isinstance(result, str)
    assert len(result) > 0