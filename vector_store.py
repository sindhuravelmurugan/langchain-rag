import os
import shutil
from typing import List, Tuple

from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from config import Config


class VectorStoreManager:
    def __init__(self):
        print("\n🔧 Initializing local embeddings...")
        self.embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        self.vector_store = None
        print(f"✅ Using embedding model: {Config.EMBEDDING_MODEL}\n")

    def create_vector_store(self, documents: List[Document]) -> Chroma:
        if not documents:
            raise ValueError("Cannot create vector store with empty documents")

        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=Config.COLLECTION_NAME,
            persist_directory=Config.VECTOR_STORE_PATH,
            collection_metadata={"hnsw:space": "cosine"},
        )

        count = self.vector_store._collection.count()
        print(f"✅ Saved {count} sections!")
        print(f"💾 Stored at: {Config.VECTOR_STORE_PATH}\n")
        return self.vector_store

    def load_vector_store(self) -> Chroma:
        if not os.path.exists(Config.VECTOR_STORE_PATH):
            raise ValueError(
                f"Saved content not found at {Config.VECTOR_STORE_PATH}. Prepare documents first."
            )

        print(f"📂 Loading saved content from {Config.VECTOR_STORE_PATH}...")
        self.vector_store = Chroma(
            collection_name=Config.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=Config.VECTOR_STORE_PATH,
        )

        count = self.vector_store._collection.count()
        print(f"✅ Loaded saved content with {count} sections\n")
        return self.vector_store

    def add_documents(self, documents: List[Document]) -> List[str]:
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")

        ids = self.vector_store.add_documents(documents)
        print(f"✅ Added {len(ids)} sections successfully\n")
        return ids

    def similarity_search_with_score(
        self, query: str, k: int = None, score_threshold: float = 0.0
    ) -> List[Tuple[Document, float]]:
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")

        k = k or Config.TOP_K_RESULTS
        results = self.vector_store.similarity_search_with_relevance_scores(
            query=query, k=k
        )
        return [(doc, score) for doc, score in results if score >= score_threshold]

    def get_collection_count(self) -> int:
        if self.vector_store is None:
            return 0
        try:
            return self.vector_store._collection.count()
        except Exception:
            return 0

    def delete_vector_store(self) -> None:
        if os.path.exists(Config.VECTOR_STORE_PATH):
            shutil.rmtree(Config.VECTOR_STORE_PATH)
        self.vector_store = None

    def as_retriever(self, search_kwargs: dict = None):
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")

        default_kwargs = {"k": Config.TOP_K_RESULTS}
        if search_kwargs:
            default_kwargs.update(search_kwargs)

        return self.vector_store.as_retriever(
            search_type="similarity", search_kwargs=default_kwargs
        )
