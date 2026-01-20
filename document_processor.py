from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain.schema import Document
from typing import List, Tuple
import os
from config import Config


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
            add_start_index=True
        )

    def load_document(self, file_path: str, display_name: str) -> List[Document]:
        file_extension = os.path.splitext(file_path)[1].lower()

        try:
            if file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file_extension == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")
                documents = loader.load()
            elif file_extension == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
                documents = loader.load()
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")

            for doc in documents:
                doc.metadata["file_type"] = file_extension
                doc.metadata["file_name"] = display_name
                doc.metadata["source"] = display_name

            print(f"✓ Loaded: {display_name} ({len(documents)} pages/sections)")
            return documents

        except Exception as e:
            print(f"✗ Error loading {display_name}: {str(e)}")
            return []

    def split_documents(self, documents: List[Document]) -> List[Document]:
        chunks = self.text_splitter.split_documents(documents)

        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)
            chunk.metadata["token_count"] = len(chunk.page_content) // 4

        return chunks

    def process_documents(self, files: List[Tuple[str, str]]) -> List[Document]:
        print(f"\n📄 Processing {len(files)} file(s)...")

        all_documents: List[Document] = []

        for file_path, display_name in files:
            docs = self.load_document(file_path, display_name)
            all_documents.extend(docs)

        if not all_documents:
            print("✗ No documents were successfully loaded")
            return []

        print(f"\n✂️  Preparing content (size={Config.CHUNK_SIZE}, overlap={Config.CHUNK_OVERLAP})...")

        try:
            chunks = self.split_documents(all_documents)
        except Exception as e:
            print(f"✗ Error while preparing content: {str(e)}")
            return []

        print(f"✓ Prepared {len(chunks)} sections from {len(all_documents)} document(s)\n")
        return chunks

    def get_stats(self, chunks: List[Document]) -> dict:
        if not chunks:
            return {
                "total_chunks": 0,
                "total_documents": 0,
                "sources": [],
                "avg_chunk_size": 0,
                "total_characters": 0,
                "estimated_tokens": 0
            }

        sources = list(set([
            chunk.metadata.get("file_name", "unknown")
            for chunk in chunks
        ]))

        total_chars = sum(len(chunk.page_content) for chunk in chunks)
        avg_chunk_size = total_chars / len(chunks)
        estimated_tokens = total_chars // 4

        return {
            "total_chunks": len(chunks),
            "total_documents": len(sources),
            "sources": sources,
            "avg_chunk_size": round(avg_chunk_size, 2),
            "total_characters": total_chars,
            "estimated_tokens": estimated_tokens,
            "file_types": list(set([chunk.metadata.get("file_type", "unknown") for chunk in chunks]))
        }
