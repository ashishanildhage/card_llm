# card_llm

This is a sophisticated chatbot built using **LangChain, LangSmith, MLflow, and OpenAI**, with a **Streamlit** frontend. It allows users to query details related to their **Amazon ICICI Credit Card** transactions, including fees, fuel surcharge, Myntra cashback, and more. Additionally, users can upload **PDF statements** for document-based queries.

## Features
- 🚀 **Fast & Scalable** chatbot powered by OpenAI & FAISS.
- 💳 **Predefined Commands**: `FEES`, `FUEL`, `MYNTRA`, etc.
- 📄 **Document Upload**: Query PDF credit card statements.
- 📊 **Observability & Monitoring** with **LangSmith & MLflow**.
- 🎛️ **User-Friendly UI** built with **Streamlit**.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/chatbot.git
   cd chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export LANGCHAIN_TRACING_V2="true"
   export LANGCHAIN_PROJECT="Amazon_ICICI_Chatbot"
   ```
   For Windows (PowerShell):
   ```powershell
   $env:OPENAI_API_KEY="your-openai-api-key"
   $env:LANGCHAIN_TRACING_V2="true"
   $env:LANGCHAIN_PROJECT="Amazon_ICICI_Chatbot"
   ```

4. Start MLflow server (for monitoring):
   ```bash
   mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
   ```

5. Run the chatbot:
   ```bash
   streamlit run your_script.py
   ```

## Usage
- Enter a **predefined command** like `FEES`, `FUEL`, `MYNTRA` to get specific details.
- Upload a **PDF statement** and ask document-based questions using `doc: <your query>`.
- View query monitoring & logs via **MLflow UI**.

## Troubleshooting
- Ensure dependencies are installed (`pip install -r requirements.txt`).
- Check if the **MLflow server** is running on port **5000**.
- Verify that your **OpenAI API key** is set correctly.

## License
MIT License. Contributions are welcome! 🚀
