"""
Test document ingestion into Qdrant.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import asyncio

print("Script started")

from app.rag.ingestion.ingest_service import IngestService

print("Imports completed")


async def main():

    print("Creating service...")

    service = IngestService()

    print("Calling ingest...")

    sample_pdf = (
        Path(__file__).parent
        / "sample-data"
        / "rag.pdf"
    )


    chunks = await service.ingest(
        sample_pdf
    )

    print("Returned from ingest")

    print(chunks)


if __name__ == "__main__":
    print("Running main()")
    asyncio.run(main())