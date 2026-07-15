"""
Document parsers.

Responsible for extracting text from supported document formats.
"""

import json
from io import BytesIO
from pathlib import Path

from openpyxl import load_workbook
from pypdf import PdfReader
from docx import Document


class DocumentParser:
    """
    Extract text from supported document types.
    """

    def parse(
        self,
        file_path: str,
    ) -> str:
        """
        Parse a document and return extracted text.

        Args:
            file_path:
                Path to the document.

        Returns:
            Extracted text.
        """

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self._parse_pdf(file_path)

        if extension == ".docx":
            return self._parse_docx(file_path)

        if extension == ".txt":
            return self._parse_txt(file_path)

        if extension == ".json":
            return self._parse_json(file_path)

        if extension == ".xlsx":
            return self._parse_xlsx(file_path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    def _parse_pdf(
        self,
        file_path: str,
    ) -> str:
        """
        Extract text from PDF.
        """

        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    def _parse_docx(
        self,
        file_path: str,
    ) -> str:
        """
        Extract text from Word document.
        """

        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    def _parse_txt(
        self,
        file_path: str,
    ) -> str:
        """
        Extract text from a text file.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            return file.read()

    def _parse_json(
        self,
        file_path: str,
    ) -> str:
        """
        Convert JSON into formatted text.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return json.dumps(
            data,
            indent=2,
        )

    def _parse_xlsx(
        self,
        file_path: str,
    ) -> str:
        """
        Extract text from an Excel workbook.
        """

        workbook = load_workbook(
            filename=file_path,
            data_only=True,
        )

        rows = []

        for sheet in workbook.worksheets:

            rows.append(f"Sheet: {sheet.title}")

            for row in sheet.iter_rows(values_only=True):

                values = [
                    str(cell)
                    for cell in row
                    if cell is not None
                ]

                if values:
                    rows.append(
                        " | ".join(values)
                    )

        return "\n".join(rows)