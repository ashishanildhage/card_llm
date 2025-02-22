# streamlit_app.py
import streamlit as st
from src.core.llm import CreditCardAssistant
from src.core.memory import get_memory
from src.core.vector_store import DocumentStore
from src.config.settings import settings
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session():
    """Initialize or get Streamlit session state variables."""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = CreditCardAssistant(get_memory())
    if 'doc_store' not in st.session_state:
        st.session_state.doc_store = DocumentStore()

def handle_file_upload(uploaded_file):
    """Process uploaded PDF file."""
    try:
        doc_path = os.path.join(settings.UPLOAD_FOLDER, uploaded_file.name)
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
        
        with open(doc_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.doc_store.add_document(doc_path)
        return True
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        return False

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Credit Card Assistant",
        page_icon="💳",
        layout="wide"
    )
    
    initialize_session()
    
    st.title("💳 Amazon ICICI Credit Card Assistant")
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload credit card statements (PDF)",
            type=["pdf"],
            help="Upload your credit card statements for personalized assistance"
        )
        
        if uploaded_file:
            if handle_file_upload(uploaded_file):
                st.success("✅ Document processed successfully!")
            else:
                st.error("❌ Error processing document")
    
    # Main chat interface
    st.markdown("### Ask a question about your credit card:")
    
    # Help text with example queries
    with st.expander("See example queries"):
        st.markdown("""
        - What are the reward points on Amazon purchases?
        - How do I redeem my reward points?
        - What are the card fees and charges?
        - Type 'doc: [your question]' to search uploaded statements
        """)
    
    # Chat interface
    user_query = st.text_input("Your question:", placeholder="Type your question here...")
    
    if st.button("Submit", type="primary"):
        try:
            with st.spinner("Processing your question..."):
                if user_query.lower().startswith("doc:"):
                    clean_query = user_query.replace("doc:", "").strip()
                    response = st.session_state.doc_store.query_document(clean_query)
                else:
                    response = st.session_state.assistant.process_query(user_query)
                
                st.markdown(f"**Response:**\n{response}")
                
        except Exception as e:
            st.error(f"Error processing your question. Please try again.")
            logger.error(f"Query processing error: {str(e)}")

if __name__ == "__main__":
    main()