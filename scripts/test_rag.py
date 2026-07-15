"""
Test the complete RAG pipeline.

Question
    ↓
Semantic Search
    ↓
Reranker
    ↓
Gemini
    ↓
Answer
"""

import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.ai.llm.factory import LLMFactory
from app.ai.llm.models import LLMRequest
from app.rag.models import SearchRequest
from app.rag.retrieval.reranker import Reranker
from app.rag.retrieval.search_service import SearchService


async def main():

    question = "Explain Retrieval-Augmented Generation."

    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    #
    # Search
    #

    search_service = SearchService()

    results = await search_service.search(
        SearchRequest(
            query=question,
            top_k=5,
        )
    )

    #
    # Rerank
    #

    reranker = Reranker()

    results = await reranker.rerank(
        question,
        results,
    )

    #
    # Build Context
    #

    context = "\n\n".join(
        result.chunk.content
        for result in results
    )

    print()
    print("=" * 80)
    print("RETRIEVED CONTEXT")
    print("=" * 80)
    print(context[:1000])
    print()

    #
    # Build Prompt
    #

    prompt = f"""
You are an Enterprise AI Assistant.

Answer ONLY using the supplied context.

If the answer is not present in the context, reply:

"I could not find the answer in the knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""

    #
    # LLM
    #

    llm = LLMFactory.create()

    response = await llm.generate(
        LLMRequest(
            prompt=prompt,
        )
    )

    print("=" * 80)
    print("AI ANSWER")
    print("=" * 80)
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())