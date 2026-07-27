def clean_llm_json(       
        text: str,
    ) -> str:
        """
        Remove Markdown code fences returned by LLMs.

        Example:

        ```json
        {...}
        ```

        becomes

        {...}
        """

        text = text.strip()

        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()