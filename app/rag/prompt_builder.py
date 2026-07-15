"""
Prompt builder for the Enterprise RAG Platform.
"""


class PromptBuilder:
    """
    Builds prompts for Retrieval-Augmented Generation (RAG).
    """

    NO_ANSWER_MESSAGE = (
        "I could not find the answer in the knowledge base."
    )

    def build_rag_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build a prompt for Retrieval-Augmented Generation.

        Args:
            question:
                User question.

            context:
                Retrieved document context.

        Returns:
            Prompt ready to send to the LLM.
        """

        return f"""
You are an Enterprise AI Assistant.

Your job is to answer user questions using ONLY the supplied context.

Guidelines:
1. Use only the supplied context.
2. Do not invent or assume information.
3. If the answer is not available in the context, reply exactly:
   "{self.NO_ANSWER_MESSAGE}"
4. Keep answers clear, concise, and professional.
5. If the context contains multiple relevant sections, combine them into a single coherent answer.
6. Do not mention that you were provided with context.

============================================================
CONTEXT
============================================================

{context}

============================================================
QUESTION
============================================================

{question}

============================================================
ANSWER
============================================================
"""

    def build_summary_prompt(
        self,
        context: str,
    ) -> str:
        """
        Build a document summarization prompt.
        """

        return f"""
You are an Enterprise AI Assistant.

Summarize the following document.

============================================================
DOCUMENT
============================================================

{context}

============================================================
SUMMARY
============================================================
"""

    def build_compare_prompt(
        self,
        document1: str,
        document2: str,
    ) -> str:
        """
        Build a document comparison prompt.
        """

        return f"""
You are an Enterprise AI Assistant.

Compare the following two documents.

============================================================
DOCUMENT 1
============================================================

{document1}

============================================================
DOCUMENT 2
============================================================

{document2}

============================================================
Provide:

1. Similarities
2. Differences
3. Key observations
============================================================
"""

    def build_custom_prompt(
        self,
        instruction: str,
        context: str,
    ) -> str:
        """
        Build a custom prompt.
        """

        return f"""
You are an Enterprise AI Assistant.

Instruction:

{instruction}

============================================================
CONTEXT
============================================================

{context}

============================================================
RESPONSE
============================================================
"""