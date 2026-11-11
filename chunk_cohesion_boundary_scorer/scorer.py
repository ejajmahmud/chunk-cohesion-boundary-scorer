"""Core Chunk Cohesion Boundary Scorer implementation."""
import math
import re
from dataclasses import dataclass
from typing import List, Set, Tuple

@dataclass
class SemanticChunk:
    chunk_id: int
    text: str
    token_count: int
    cohesion_score: float

class ChunkCohesionScorer:
    """Segments documents into topical chunks by identifying cohesion drop valleys."""
    
    def __init__(self, min_chunk_words: int = 20, max_chunk_words: int = 150):
        self.min_chunk_words = min_chunk_words
        self.max_chunk_words = max_chunk_words

    def tokenize_words(self, text: str) -> Set[str]:
        words = re.findall(r"\b[a-zA-Z0-9_]+\b", text.lower())
        stopwords = {"the", "a", "an", "is", "it", "to", "in", "and", "of"}
        return {w for w in words if w not in stopwords}

    def compute_sentence_overlap(self, s1: str, s2: str) -> float:
        w1, w2 = self.tokenize_words(s1), self.tokenize_words(s2)
        if not w1 or not w2:
            return 0.0
        return len(w1.intersection(w2)) / math.sqrt(len(w1) * len(w2))

    def split_into_chunks(self, document_text: str) -> List[SemanticChunk]:
        # Split sentences by period or double newline
        raw_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n\n+", document_text) if s.strip()]
        if not raw_sentences:
            return []

        chunks = []
        current_sentences = [raw_sentences[0]]
        current_word_count = len(raw_sentences[0].split())
        chunk_id = 1

        for i in range(1, len(raw_sentences)):
            next_sent = raw_sentences[i]
            next_words = len(next_sent.split())
            overlap = self.compute_sentence_overlap(current_sentences[-1], next_sent)

            # Split if reached min_words and low cohesion, or max_words exceeded
            should_split = False
            if current_word_count + next_words > self.max_chunk_words:
                should_split = True
            elif current_word_count >= self.min_chunk_words and overlap < 0.10:
                should_split = True

            if should_split:
                chunk_text = " ".join(current_sentences)
                chunks.append(SemanticChunk(chunk_id, chunk_text, current_word_count, round(overlap, 3)))
                chunk_id += 1
                current_sentences = [next_sent]
                current_word_count = next_words
            else:
                current_sentences.append(next_sent)
                current_word_count += next_words

        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(SemanticChunk(chunk_id, chunk_text, current_word_count, 1.0))

        return chunks
