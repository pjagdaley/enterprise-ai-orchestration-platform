import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.models import SearchRequest
from app.rag.retrieval.search_service import SearchService


async def main():

    service = SearchService()

    results = await service.search(
        SearchRequest(
            query="What is RAG?",
            top_k=5,
        )
    )

    print()
    print("=" * 80)
    print("SEARCH RESULTS")
    print("=" * 80)

    for index, result in enumerate(results, start=1):

        print(f"\nResult #{index}")
        print(f"Score : {result.score:.4f}")
        print(f"Source: {result.chunk.source}")
        print("-" * 80)
        print(result.chunk.content[:500])
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main())