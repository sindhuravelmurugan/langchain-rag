import os
import tempfile
import streamlit as st
from rag_system import RAGSystem
from config import Config


st.set_page_config(page_title="RAG Assistant", layout="wide")

if "rag" not in st.session_state:
    Config.validate()
    st.session_state.rag = RAGSystem()

if "chat" not in st.session_state:
    st.session_state.chat = []

def run_local_answer(prompt: str) -> str:
    from transformers import pipeline
    if "local_pipe" not in st.session_state:
        st.session_state.local_pipe = pipeline(
            "text2text-generation",
            model=Config.LOCAL_ANSWER_MODEL,
            max_new_tokens=Config.MAX_NEW_TOKENS,
            truncation=True
        )
    out = st.session_state.local_pipe(prompt)[0]["generated_text"]
    return out.strip()


st.sidebar.title("Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload files",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

stats = st.session_state.rag.get_system_stats()
col1, col2, col3 = st.columns(3)
col1.metric("Saved content", stats.get("documents", 0))
col2.metric("Files ready", len(uploaded_files) if uploaded_files else 0)
col3.metric("Messages", len(st.session_state.chat))

st.title("RAG Assistant")
st.caption("Upload documents → the app prepares them → ask questions and get answers with references.")

if st.sidebar.button("Prepare Documents", use_container_width=True):
    if not uploaded_files:
        st.sidebar.error("Please upload at least one file.")
    else:
        pairs = []
        for uf in uploaded_files:
            suffix = "." + uf.name.split(".")[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uf.getbuffer())
                temp_path = tmp.name
            pairs.append((temp_path, uf.name))

        res = st.session_state.rag.initialize_from_files(pairs)
        if res.get("success"):
            st.sidebar.success(res.get("message", "Ready!"))
        else:
            st.sidebar.error(res.get("message", "Something went wrong."))

if st.sidebar.button("Load Saved Documents", use_container_width=True):
    res = st.session_state.rag.load_existing()
    if res.get("success"):
        st.sidebar.success(res.get("message", "Loaded."))
    else:
        st.sidebar.error(res.get("message", "Could not load."))

if st.sidebar.button("Clear Chat", use_container_width=True):
    st.session_state.chat = []
    st.session_state.rag.clear_conversation()
    st.rerun()

if st.sidebar.button("Reset System", use_container_width=True):
    st.session_state.chat = []
    st.session_state.rag.reset_system()
    st.rerun()

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("References"):
                for s in msg["sources"]:
                    st.write(f"- {s}")

prompt = st.chat_input("Ask a question about your documents...")

if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Working on it...")

        result = st.session_state.rag.query(prompt)
        answer_prompt = result.get("answer_prompt", "")
        sources = result.get("sources", [])

        answer = run_local_answer(answer_prompt)
        placeholder.write(answer)

        st.session_state.chat.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })

        if sources:
            with st.expander("References"):
                for s in sources:
                    st.write(f"- {s}")
