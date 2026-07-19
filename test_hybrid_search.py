"""
Test Hybrid Search (Semantic + Lexical using RRF).
"""

import asyncio

from app.retrieval.hybrid.hybrid_retriever import HybridRetriever


async def main():

    retriever = HybridRetriever()

    query = "What is Retrieval-Augmented Generation?"

    results = await retriever.search(
        query=query,
        top_k=5,
    )

    print()

    print("=" * 80)
    print("HYBRID SEARCH RESULTS")
    print("=" * 80)

    if not results:

        print("No results found.")
        return

    for index, result in enumerate(results, start=1):

        print()

        print(f"Result #{index}")
        print(f"Hybrid Score: {result.score:.6f}")
        print(f"Document ID : {result.document_id}")
        print(f"Chunk ID    : {result.chunk_id}")
        print(f"Extension   : {result.extension}")
        print(f"Source      : {result.source_path}")

        print("-" * 80)

        preview = result.content.strip()

        if len(preview) > 600:
            preview = preview[:600] + "..."

        print(preview)

        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())