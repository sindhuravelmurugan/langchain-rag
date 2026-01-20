# 📄 Document Q&A Assistant (RAG-based)

This project is a document-based question answering application where users can upload files (such as PDFs) and ask questions about their content. The system retrieves relevant parts of the uploaded documents and generates answers grounded in those documents.

I built this project to understand and implement the Retrieval-Augmented Generation (RAG) workflow end to end, while keeping the interface simple and easy to use.

---

## 🚀 Features
- Upload PDF documents
- Ask questions in natural language
- Automatically retrieves relevant sections from documents
- Generates answers based on document content
- Simple web interface built with Streamlit

---

## 🛠️ Tech Stack
- **Python**
- **Streamlit** – user interface
- **LangChain** – RAG pipeline orchestration
- **ChromaDB** – vector storage
- **Sentence Transformers** – semantic search embeddings
- **Local / API-based language models** – answer generation (configurable)

---

## ⚙️ How It Works (High Level)
1. The user uploads a document
2. The document is processed and stored for semantic search
3. When a question is asked, relevant sections are retrieved
4. The system generates an answer using the retrieved context
5. The response is displayed to the user

---

## ▶️ Running the App Locally
```bash
pip install -r requirements.txt
streamlit run app.py
