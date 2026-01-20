# 🤖 LangChain RAG Application with Google Gemini

A production-ready Retrieval-Augmented Generation (RAG) system using **FREE** Google Gemini API.

### 1. Setup 
```bash
# Create project folder
mkdir langchain-rag-gemini
cd langchain-rag-gemini

# Create all 8 files (copy from above)
# Don't forget the .env file with your API key!

# Install dependencies
pip install -r requirements.txt
```

### 3. Create `.env` File
```bash
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

Opens at: http://localhost:8501

## 📁 Project Structure
```
langchain-rag-gemini/
├── .env                       
├── .gitignore                 # Git ignore rules
├── config.py                  # Configuration
├── document_processor.py      # Document handling
├── vector_store.py           # Vector database
├── conversation_manager.py   # Chat manager
├── rag_system.py             # Main orchestrator
├── app.py                    # Streamlit UI
├── requirements.txt          # Dependencies
└── README.md                 # This file
```
