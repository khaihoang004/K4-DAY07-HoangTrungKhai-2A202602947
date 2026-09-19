from __future__ import annotations

from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            import chromadb  # noqa: F401

            self._chroma_client = chromadb.Client()
            
            # Clean up the collection if it already exists to ensure a fresh start
            # for each EmbeddingStore instance, which prevents state leakage across tests.
            try:
                self._chroma_client.delete_collection(name=self._collection_name)
            except Exception:
                pass
                
            self._collection = self._chroma_client.get_or_create_collection(
                name=self._collection_name,
                metadata={"hnsw:space": "ip"}  # Inner product to match dot product scoring
            )
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        chunk_id = str(self._next_index)
        
        metadata = getattr(doc, "metadata", {})
        if metadata is None:
            metadata = {}
        else:
            metadata = metadata.copy()
            
        doc_id = getattr(doc, "id", None)
        if doc_id is not None:
            metadata["doc_id"] = doc_id

        content = getattr(doc, "content", "")
        embedding = self._embedding_fn(content)
        
        return {
            "id": chunk_id,
            "content": content,
            "metadata": metadata,
            "embedding": embedding,
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        query_embedding = self._embedding_fn(query)
        scored_records = []
        
        for record in records:
            score = _dot(query_embedding, record["embedding"])
            scored_records.append((score, record))
            
        # Sort by highest score (similarity) descending
        scored_records.sort(key=lambda x: x[0], reverse=True)
        
        # Return records up to top_k, adding the score to the dict
        results = []
        for score, record in scored_records[:top_k]:
            result_record = record.copy()
            result_record["score"] = score
            results.append(result_record)
            
        return results

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        For ChromaDB: use collection.add(ids=[...], documents=[...], embeddings=[...])
        For in-memory: append dicts to self._store
        """
        if not docs:
            return

        if self._use_chroma and self._collection is not None:
            ids = []
            documents = []
            embeddings = []
            metadatas = []

            for doc in docs:
                chunk_id = str(self._next_index)
                self._next_index += 1
                
                content = getattr(doc, "content", "")
                ids.append(chunk_id)
                documents.append(content)
                embeddings.append(self._embedding_fn(content))
                
                meta = getattr(doc, "metadata", {})
                if meta is None:
                    meta = {}
                else:
                    meta = meta.copy()
                    
                doc_id = getattr(doc, "id", None)
                if doc_id is not None:
                    meta["doc_id"] = doc_id
                    
                metadatas.append(meta if meta else None)

            # If all metadata entries are None, omit the parameter entirely
            if all(m is None for m in metadatas):
                self._collection.add(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings
                )
            else:
                self._collection.add(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
        else:
            for doc in docs:
                record = self._make_record(doc)
                self._next_index += 1
                self._store.append(record)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        For in-memory: compute dot product of query embedding vs all stored embeddings.
        """
        return self.search_with_filter(query, top_k=top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        if self._use_chroma and self._collection is not None:
            return self._collection.count()
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        filter_dict = metadata_filter or {}

        if self._use_chroma and self._collection is not None:
            query_embedding = self._embedding_fn(query)
            
            # ChromaDB expects `where` to be None if there is no filter.
            where_clause = filter_dict if filter_dict else None
            
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_clause,
                include=["documents", "metadatas", "embeddings"]
            )
            
            formatted_results = []
            if results and results.get("ids") and len(results["ids"]) > 0:
                for i in range(len(results["ids"][0])):
                    meta = {}
                    if results.get("metadatas") and results["metadatas"][0] and results["metadatas"][0][i] is not None:
                        meta = results["metadatas"][0][i]
                    
                    emb = results["embeddings"][0][i]
                    score = _dot(query_embedding, emb)
                        
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": meta,
                        "score": score
                    })
                    
                # Ensure results are strictly sorted by score descending
                formatted_results.sort(key=lambda x: x["score"], reverse=True)
                
            return formatted_results
        else:
            filtered_records = []
            if filter_dict:
                for record in self._store:
                    record_meta = record.get("metadata", {})
                    # Check if all key/value pairs in the filter match the record's metadata
                    if all(record_meta.get(k) == v for k, v in filter_dict.items()):
                        filtered_records.append(record)
            else:
                filtered_records = self._store

            return self._search_records(query, filtered_records, top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        if self._use_chroma and self._collection is not None:
            initial_count = self._collection.count()
            self._collection.delete(where={"doc_id": doc_id})
            return self._collection.count() < initial_count
        else:
            initial_len = len(self._store)
            self._store = [
                record for record in self._store 
                if record.get("metadata", {}).get("doc_id") != doc_id
            ]
            return len(self._store) < initial_len