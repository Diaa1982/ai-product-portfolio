from __future__ import annotations

import math
import re
from pathlib import Path

from .schemas import Evidence


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))


class EnterpriseRAG:
    """Approved-source RAG with Chroma support and an offline fallback."""

    def __init__(self, knowledge_dir: Path, vector_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.vector_dir = vector_dir
        self._documents: list[tuple[str, str]] = []
        self._vector_store = None

    def ingest(self) -> int:
        self._documents.clear()
        for path in sorted(self.knowledge_dir.rglob("*")):
            if path.suffix.lower() not in {".md", ".txt", ".json", ".csv"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for index, chunk in enumerate(self._chunk(text)):
                self._documents.append((f"{path}#chunk-{index}", chunk))
        self._try_build_chroma()
        return len(self._documents)

    def _try_build_chroma(self) -> None:
        try:
            from langchain_chroma import Chroma
            from langchain_core.documents import Document
            from langchain_huggingface import HuggingFaceEmbeddings

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            docs = [
                Document(page_content=text, metadata={"source": source})
                for source, text in self._documents
            ]
            if docs:
                self._vector_store = Chroma.from_documents(
                    docs,
                    embeddings,
                    persist_directory=str(self.vector_dir),
                    collection_name="enterprise_knowledge",
                )
        except Exception:
            self._vector_store = None

    def search(self, query: str, k: int = 5) -> list[Evidence]:
        if not self._documents:
            self.ingest()
        if self._vector_store is not None:
            results = self._vector_store.similarity_search_with_relevance_scores(
                query, k=k
            )
            return [
                Evidence(
                    source=str(doc.metadata.get("source", "unknown")),
                    content=doc.page_content,
                    score=float(score),
                    metadata=dict(doc.metadata),
                )
                for doc, score in results
            ]
        query_tokens = _tokens(query)
        scored: list[Evidence] = []
        for source, content in self._documents:
            doc_tokens = _tokens(content)
            overlap = len(query_tokens & doc_tokens)
            score = overlap / math.sqrt(max(1, len(query_tokens) * len(doc_tokens)))
            scored.append(Evidence(source=source, content=content, score=score))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:k]

    @staticmethod
    def _chunk(text: str, size: int = 1200, overlap: int = 150) -> list[str]:
        normalized = " ".join(text.split())
        if not normalized:
            return []
        step = max(1, size - overlap)
        return [normalized[i : i + size] for i in range(0, len(normalized), step)]

