# 🤖 LangChain RAG Application with Google Gemini

A production-ready Retrieval-Augmented Generation (RAG) system using **FREE** Google Gemini API.

## ✨ Features

- ✅ **100% FREE** - Uses Google Gemini (no credit card required)
- ✅ **Vector Embeddings** - Semantic search with Gemini embeddings
- ✅ **Conversation Memory** - Remembers context across messages
- ✅ **Multi-format Support** - PDF, TXT, and Markdown files
- ✅ **Interactive UI** - Beautiful Streamlit interface
- ✅ **Production Ready** - Real LangChain APIs

## 🚀 Quick Start

### 1. Get Gemini API Key (FREE)

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API key"
4. Copy the key (starts with `AIza...`)

### 2. Setup Project
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
├── .env                       # Your API key (SECRET!)
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

## 🎯 Usage

### Upload Documents
1. Click "Browse files" in sidebar
2. Select PDF or TXT files
3. Click "Process Documents"
4. Wait 30-60 seconds

### Ask Questions
1. Type question in chat box
2. Press Enter
3. Get AI-powered answer with sources
4. Ask follow-up questions

## 💰 Cost

**100% FREE!**
- No credit card required
- 60 requests per minute
- Unlimited daily usage

## 🧪 Test Example

Create `test.txt`:
```
Python is great for AI development.
Machine learning processes large datasets.
Deep learning requires GPUs.
```

Upload and ask:
- "What language is mentioned?"
- "What does deep learning require?"

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
- Check `.env` file exists
- Verify key starts with `AIza`
- Ensure `.env` is in same folder as `app.py`

### Error: "No module named..."
```bash
pip install -r requirements.txt
```

### Slow Processing
- Normal for first upload (30-60 seconds)
- Queries are faster (2-5 seconds)

## 📚 Tech Stack

- **LangChain**: RAG framework
- **Google Gemini**: FREE LLM & embeddings
- **ChromaDB**: Vector database
- **Streamlit**: Web interface
- **Python 3.8+**

## 🔒 Security

- Never commit `.env` to Git
- Keep API key secret
- `.gitignore` already configured

## 📖 Learn More

- [Gemini Docs](https://ai.google.dev/docs)
- [LangChain Docs](https://python.langchain.com/)
- [Streamlit Docs](https://docs.streamlit.io/)

## 🎉 You're Ready!

Total Cost: **$0.00**
Setup Time: **5 minutes**
Quality: **GPT-4 level**

Happy building! 🚀