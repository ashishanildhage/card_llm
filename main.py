import os
import streamlit as st
import mlflow
import langsmith
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

# Configure API Keys
os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'Amazon_ICICI_Chatbot'

# Initialize LangSmith for tracing
langsmith.init(project="Amazon_ICICI_Chatbot")

# Initialize MLflow
mlflow.set_tracking_uri("http://localhost:5000")  # Ensure MLflow server is running
mlflow.set_experiment("Amazon_ICICI_Credit_Card_Bot")

# Custom command mapping
COMMANDS = {
    "FEES": "Provide details about fees and charges of the Amazon ICICI credit card.",
    "FUEL": "Give details regarding fuel surcharge and waivers.",
    "MYNTRA": "Calculate total cashback earned and spent on Myntra using this card."
}

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4-turbo")

# Memory for conversation
memory = ConversationBufferMemory()

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["query"],
    template="You are a financial assistant specialized in Amazon ICICI Credit Cards. Answer user queries based on given data: {query}"
)

def process_query(user_input):
    """Handles predefined commands and general queries."""
    if user_input in COMMANDS:
        query = COMMANDS[user_input]
    else:
        query = user_input
    
    chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)
    response = chain.run(query)
    
    # Log query to MLflow
    with mlflow.start_run():
        mlflow.log_param("query", user_input)
        mlflow.log_metric("response_length", len(response))
    
    return response

# File Upload and Processing
vector_store = None
def process_uploaded_file(uploaded_file):
    """Loads PDF file and creates vector database for document search."""
    global vector_store
    file_path = f"./temp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
    return "Document uploaded and indexed!"

def query_document(query):
    """Retrieves answers from uploaded document."""
    if vector_store is None:
        return "No document uploaded."
    results = vector_store.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])

# Streamlit UI
st.title("Amazon ICICI Credit Card Chatbot")
st.sidebar.header("Upload a PDF")
uploaded_file = st.sidebar.file_uploader("Upload PDF statements", type=["pdf"])
if uploaded_file:
    st.sidebar.success(process_uploaded_file(uploaded_file))

user_query = st.text_input("Ask a question about your Amazon ICICI Credit Card:")
if st.button("Submit"):
    if uploaded_file and "doc:" in user_query.lower():
        st.write(query_document(user_query.replace("doc:", "")))
    else:
        st.write(process_query(user_query))
