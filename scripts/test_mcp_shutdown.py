import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import asyncio
import logging
import time

from app.ai.mcp.service import MCPService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


async def main():
    print("=" * 80)
    print("Creating MCP Service")
    print("=" * 80)

    service = MCPService(
        command="npx",
        args=[
            "@modelcontextprotocol/server-filesystem",
            r"C:\AI-ML-Projects",
        ],
    )

    print("Connecting...")
    start = time.perf_counter()

    await service.initialize()

    print(f"Connected in {time.perf_counter() - start:.2f} sec")

    print()
    print("=" * 80)
    print("Disconnecting...")
    print("=" * 80)

    start = time.perf_counter()

    await service.shutdown()

    print(f"Disconnected in {time.perf_counter() - start:.2f} sec")


if __name__ == "__main__":
    asyncio.run(main())