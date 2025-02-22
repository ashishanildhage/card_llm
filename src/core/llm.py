# src/core/llm.py
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMemory
from src.config.settings import settings
from typing import Dict, Any, Optional
import mlflow
import logging

logger = logging.getLogger(__name__)


class CreditCardAssistant:
    """Credit card assistant using LangChain and MLflow for tracking."""
    
    def __init__(self, memory):
        """Initialize the assistant with LLM and memory components."""
        self.llm = ChatOpenAI(model_name=settings.LLM_MODEL_NAME)
        self.memory = memory
        self.prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""You are a financial assistant specialized in Amazon ICICI Credit Cards. 
            Answer user queries based on given data: {query}
            
            Provide clear, concise answers with accurate information."""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template, memory=self.memory)
        
        # Initialize MLflow
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
    
    def process_query(self, user_input: str) -> str:
        """
        Process user query and return response with MLflow tracking.
        
        Args:
            user_input (str): User's question or command
            
        Returns:
            str: Assistant's response
        """
        try:
            response = self.chain.run(user_input)
            
            # Log interaction to MLflow
            with mlflow.start_run(nested=True):
                mlflow.log_params({
                    "query": user_input,
                    "model": settings.LLM_MODEL_NAME
                })
                mlflow.log_metrics({
                    "response_length": len(response),
                })
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise