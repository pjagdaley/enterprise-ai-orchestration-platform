"""
RAG Tool.

Retrieves relevant documents from the enterprise knowledge base
and generates an answer using the configured LLM.
"""

from app.ai.llm.factory import LLMFactory
from app.ai.llm.models import LLMRequest
from app.ai.tools.base_tool import BaseTool
from app.ai.tools.models import ToolRequest
from app.ai.tools.models import ToolResponse
from app.rag.models import SearchRequest
from app.rag.retrieval.reranker import Reranker
from app.rag.retrieval.search_service import SearchService


class RAGTool(BaseTool):
    """
    Enterprise Retrieval-Augmented Generation tool.
    """

    @property
    def name(self) -> str:
        return "rag"

    @property
    def description(self) -> str:
        return "Answers questions using the enterprise knowledge base."

    def __init__(self) -> None:

        self._search_service = SearchService()

        self._reranker = Reranker()

        self._llm = LLMFactory.create()

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResponse:
        """
        Execute the RAG workflow.
        """

        #
        # Retrieve relevant documents
        #

        results = await self._search_service.search(
            SearchRequest(
                query=request.input,
                top_k=5,
            )
        )

        #
        # Rerank
        #

        results = await self._reranker.rerank(
            request.input,
            results,
        )

        #
        # Build context
        #

        context = "\n\n".join(
            result.chunk.content
            for result in results
        )

        #
        # Build prompt
        #

        prompt = f"""
Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context,
reply with:

"I could not find relevant information."

Context:
{context}

Question:
{request.input}
"""

        #
        # Generate answer
        #

        response = await self._llm.generate(
            LLMRequest(
                prompt=prompt,
            )
        )

        return ToolResponse(
            success=True,
            result=response.content,
        )