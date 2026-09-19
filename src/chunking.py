from __future__ import annotations

import math
import re


class FixedSizeChunker:
    """
    Split text into fixed-size chunks with optional overlap.

    Rules:
        - Each chunk is at most chunk_size characters long.
        - Consecutive chunks share overlap characters.
        - The last chunk contains whatever remains.
        - If text is shorter than chunk_size, return [text].
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks


class SentenceChunker:
    """
    Split text into chunks of at most max_sentences_per_chunk sentences.

    Sentence detection: split on ". ", "! ", "? " or ".\n".
    Strip extra whitespace from each chunk.
    """

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []

        sentences = re.split(r"(?<=[.!?])(?:\s+)", text.strip())

        sentences = [s.strip() for s in sentences if s.strip()]
        chunks = []

        for i in range(0, len(sentences), self.max_sentences_per_chunk):
            chunk = " ".join(
                sentences[i:i + self.max_sentences_per_chunk]
            ).strip()

            if chunk:
                chunks.append(chunk)

        return chunks


class RecursiveChunker:
    """
    Recursively split text using separators in priority order.

    Default separator priority:
        ["\n\n", "\n", ". ", " ", ""]
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        self.separators = self.DEFAULT_SEPARATORS if separators is None else list(separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        return self._split(text, self.separators)

    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        if len(current_text) <= self.chunk_size:
            return [current_text]

        # Find the first separator that actually exists in the text
        separator = ""
        next_separators = []
        for i, sep in enumerate(remaining_separators):
            if sep == "" or sep in current_text:
                separator = sep
                next_separators = remaining_separators[i + 1:]
                break

        # Split using the identified separator
        if separator == "":
            splits = list(current_text)
        else:
            splits = current_text.split(separator)

        # Recombine small splits into chunks of up to `chunk_size`
        final_chunks = []
        current_chunk = []
        current_length = 0

        for split in splits:
            if len(split) > self.chunk_size:
                # If a single split is still too large, finish the current accumulated chunk
                if current_chunk:
                    final_chunks.append(separator.join(current_chunk))
                    current_chunk = []
                    current_length = 0
                # Recursively split the oversized chunk with the remaining separators
                final_chunks.extend(self._split(split, next_separators))
            else:
                # Check if adding the new split exceeds the chunk limit
                separator_length = len(separator) if current_chunk else 0
                new_length = current_length + len(split) + separator_length
                
                if new_length > self.chunk_size:
                    final_chunks.append(separator.join(current_chunk))
                    current_chunk = [split]
                    current_length = len(split)
                else:
                    current_chunk.append(split)
                    current_length = new_length

        if current_chunk:
            final_chunks.append(separator.join(current_chunk))

        return final_chunks


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    cosine_similarity = dot(a, b) / (||a|| * ||b||)

    Returns 0.0 if either vector has zero magnitude.
    """
    if not vec_a or not vec_b:
        return 0.0

    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return _dot(vec_a, vec_b) / (norm_a * norm_b)


class ChunkingStrategyComparator:
    """Run all built-in chunking strategies and compare their results."""

    def compare(self, text: str, chunk_size: int = 200) -> dict:
        strategies = {
            "fixed_size": FixedSizeChunker(chunk_size=chunk_size, overlap=20),
            "by_sentences": SentenceChunker(max_sentences_per_chunk=3),
            "recursive": RecursiveChunker(chunk_size=chunk_size)
        }

        comparison_results = {}

        for strategy_name, chunker in strategies.items():
            chunks = chunker.chunk(text)
            count = len(chunks)
            avg_length = sum(len(c) for c in chunks) / count if count > 0 else 0.0
            
            comparison_results[strategy_name] = {
                "count": count,
                "avg_length": avg_length,
                "chunks": chunks
            }

        return comparison_results