from typing import Dict, List
from config import Config


class ConversationManager:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.history: List[Dict[str, str]] = []

    def clear_history(self):
        self.history = []

    def get_memory_stats(self) -> Dict:
        return {"total_messages": len(self.history)}

    def _format_sources(self, docs) -> List[str]:
        sources = []
        for d in docs:
            src = d.metadata.get("file_name") or d.metadata.get("source") or "unknown"
            src = src.split("/")[-1]
            sources.append(src)
        return list(dict.fromkeys(sources))

    def _style(self, question: str) -> str:
        q = question.lower()
        if "one line" in q or "1 line" in q:
            return "Return exactly ONE sentence."
        if "short" in q or "brief" in q:
            return "Return 2-3 short sentences."
        if "bullet" in q:
            return "Return 4-7 bullet points."
        return "Return 4-6 clear sentences."

    def _make_prompt(self, question: str, context: str) -> str:
        style = self._style(question)
        return (
            "You are a helpful assistant.\n"
            "Use ONLY the content in CONTEXT.\n"
            "If CONTEXT doesn't contain enough info, say: \"I can't find that in the uploaded file.\"\n"
            "Do not mention how the system works.\n"
            "Do not repeat the prompt.\n\n"
            f"{style}\n\n"
            "QUESTION:\n"
            f"{question}\n\n"
            "CONTEXT:\n"
            f"{context}\n"
        )

    def get_response(self, question: str) -> Dict:
        docs = self.vector_store.similarity_search(question, k=Config.TOP_K_RESULTS)

        sources = self._format_sources(docs)

        max_chars = Config.MAX_CONTEXT_CHARS
        per_doc = max(300, max_chars // max(1, len(docs)))

        parts = []
        used = 0
        for d in docs:
            text = (d.page_content or "").strip()
            text = text[:per_doc]
            if not text:
                continue
            if used + len(text) > max_chars:
                remaining = max_chars - used
                if remaining <= 0:
                    break
                text = text[:remaining]
            parts.append(text)
            used += len(text)
            if used >= max_chars:
                break

        context = "\n\n---\n\n".join(parts).strip()
        prompt = self._make_prompt(question, context)

        self.history.append({"role": "user", "content": question})

        return {
            "answer_prompt": prompt,
            "sources": sources,
            "num_sources": len(sources)
        }
