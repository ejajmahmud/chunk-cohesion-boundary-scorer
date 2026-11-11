"""CLI for chunk-cohesion-boundary-scorer."""
import sys
import argparse
from .scorer import ChunkCohesionScorer

def main():
    parser = argparse.ArgumentParser(description="Chunk Cohesion Boundary Scorer CLI")
    parser.add_argument("--demo", action="store_true", help="Chunk sample multi-topic text")
    args = parser.parse_args()

    if args.demo:
        scorer = ChunkCohesionScorer(min_chunk_words=10, max_chunk_words=40)
        doc = (
            "Kubernetes orchestrates containerized workloads across compute clusters. "
            "It manages pods, replica sets, and ingress traffic controllers automatically. "
            "Recipe for chocolate cake: Mix flour, sugar, and cocoa powder in a large bowl. "
            "Bake at 350 degrees for 30 minutes until a toothpick comes out clean."
        )
        chunks = scorer.split_into_chunks(doc)
        print(f"Segmented into {len(chunks)} cohesive chunks:")
        for c in chunks:
            print(f"  [Chunk {c.chunk_id} ({c.token_count} words)]: {c.text}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
