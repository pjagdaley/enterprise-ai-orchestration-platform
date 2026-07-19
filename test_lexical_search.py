"""
Test OpenSearch lexical search.
"""

import asyncio

from app.retrieval.lexical.lexical_retriever import LexicalRetriever


async def main():

    retriever = LexicalRetriever()

    query = "who is Pankaj Jagdaley"

    results = await retriever.search(
        query=query,
        top_k=5,
    )

    print()

    print("=" * 80)
    print("LEXICAL SEARCH RESULTS")
    print("=" * 80)

    if not results:

        print("No results found.")
        return

    for index, result in enumerate(results, start=1):

        print()

        print(f"Result #{index}")
        print(f"Score      : {result.score:.4f}")
        print(f"Document ID: {result.document_id}")
        print(f"Chunk ID   : {result.chunk_id}")
        print(f"Extension  : {result.extension}")
        print(f"Source     : {result.source_path}")

        print("-" * 80)

        preview = result.content.strip()

        if len(preview) > 600:
            preview = preview[:600] + "..."

        print(preview)

        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())