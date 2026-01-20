import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CHUNK_SIZE = 900
    CHUNK_OVERLAP = 100
    TOP_K_RESULTS = 3

    VECTOR_STORE_PATH = "./chroma_db"
    COLLECTION_NAME = "rag_documents"

    MAX_HISTORY_LENGTH = 5

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    LOCAL_ANSWER_MODEL = "google/flan-t5-base"
    MAX_NEW_TOKENS = 180
    MAX_CONTEXT_CHARS = 3500

    @classmethod
    def validate(cls):
        print("✅ Configuration validated successfully!")
        print(f"✅ Local embedding model: {cls.EMBEDDING_MODEL}")
        print(f"✅ Local answer model: {cls.LOCAL_ANSWER_MODEL}")
        return True
