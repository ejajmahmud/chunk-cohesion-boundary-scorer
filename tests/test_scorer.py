"""Unit tests for chunk-cohesion-boundary-scorer."""
import unittest
from chunk_cohesion_boundary_scorer.scorer import ChunkCohesionScorer

class TestChunkCohesionScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ChunkCohesionScorer(min_chunk_words=5, max_chunk_words=30)

    def test_topic_shift_boundary_creation(self):
        doc = (
            "Distributed algorithms ensure consensus across network nodes. Consensus requires quorum votes. "
            "Apples and oranges are rich in vitamin C and dietary fiber. Fruit nutrition is essential."
        )
        chunks = self.scorer.split_into_chunks(doc)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertIn("Consensus", chunks[0].text)
        self.assertIn("Apples", chunks[1].text)
