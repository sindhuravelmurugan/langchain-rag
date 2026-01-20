from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from conversation_manager import ConversationManager
from typing import List, Dict, Tuple


class RAGSystem:
    def __init__(self):
        print("\n" + "=" * 60)
        print("🚀 Initializing RAG System")
        print("=" * 60 + "\n")

        self.doc_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        self.conversation_manager = None
        self.is_initialized = False

        print("✓ RAG System components ready\n")

    def initialize_from_files(self, files: List[Tuple[str, str]]) -> Dict:
        print("\n" + "=" * 60)
        print("📚 INITIALIZING FROM DOCUMENTS")
        print("=" * 60 + "\n")

        try:
            chunks = self.doc_processor.process_documents(files)

            if not chunks:
                return {"success": False, "message": "Could not prepare the uploaded file(s).", "stats": {}}

            vector_store = self.vector_store_manager.create_vector_store(chunks)

            self.conversation_manager = ConversationManager(vector_store)
            self.is_initialized = True

            stats = self.doc_processor.get_stats(chunks)

            return {
                "success": True,
                "message": f"Ready! Loaded {stats['total_documents']} file(s).",
                "stats": stats
            }

        except Exception as e:
            return {"success": False, "message": f"Initialization error: {str(e)}", "stats": {}}

    def load_existing(self) -> Dict:
        try:
            vector_store = self.vector_store_manager.load_vector_store()
            self.conversation_manager = ConversationManager(vector_store)
            self.is_initialized = True

            count = self.vector_store_manager.get_collection_count()

            return {
                "success": True,
                "message": f"Loaded saved content ({count} items).",
                "stats": {"total_chunks": count}
            }

        except Exception as e:
            return {"success": False, "message": f"Failed to load saved content: {str(e)}", "stats": {}}

    def add_documents(self, files: List[Tuple[str, str]]) -> Dict:
        if not self.is_initialized:
            return self.initialize_from_files(files)

        try:
            chunks = self.doc_processor.process_documents(files)

            if not chunks:
                return {"success": False, "message": "Could not prepare the uploaded file(s)."}

            self.vector_store_manager.add_documents(chunks)
            stats = self.doc_processor.get_stats(chunks)

            return {
                "success": True,
                "message": f"Added {stats['total_documents']} file(s).",
                "stats": stats
            }

        except Exception as e:
            return {"success": False, "message": f"Error adding documents: {str(e)}"}

    def query(self, question: str) -> Dict:
        if not self.is_initialized:
            return {"answer": "Please upload a file first.", "sources": [], "num_sources": 0}

        return self.conversation_manager.get_response(question)

    def clear_conversation(self) -> None:
        if self.conversation_manager:
            self.conversation_manager.clear_history()

    def reset_system(self) -> None:
        self.vector_store_manager.delete_vector_store()
        self.conversation_manager = None
        self.is_initialized = False

    def get_system_stats(self) -> Dict:
        if not self.is_initialized:
            return {"initialized": False, "documents": 0, "conversation_length": 0}

        vector_count = self.vector_store_manager.get_collection_count()
        memory_stats = self.conversation_manager.get_memory_stats() if self.conversation_manager else {}

        return {
            "initialized": True,
            "documents": vector_count,
            "conversation_length": memory_stats.get("total_messages", 0)
        }
