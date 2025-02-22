# src/core/vector_store.py
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from typing import List, Optional
import os
import logging

logger = logging.getLogger(__name__)

class DocumentStore:
    """Manages document storage and retrieval using FAISS."""
    
    def __init__(self):
        """Initialize the document store with OpenAI embeddings."""
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        
    def add_document(self, file_path: str) -> None:
        """
        Add a PDF document to the vector store.
        
        Args:
            file_path: Path to the PDF file
            
        Raises:
            Exception: If document processing fails
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                self.vector_store.add_documents(documents)
                
            logger.info(f"Added document: {file_path}")
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            raise
            
    def query_document(self, query: str, k: int = 3) -> str:
        """
        Query the document store for relevant content.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            Combined relevant document content
        """
        if not self.vector_store:
            return "No documents available. Please upload a document first."
            
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return "\n\n".join(doc.page_content for doc in docs)
        except Exception as e:
            logger.error(f"Document query error: {str(e)}")
            raise