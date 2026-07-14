"""
OpenAPI configuration for the Enterprise AI Orchestration Platform.
"""

from fastapi import FastAPI

from app.core.config import settings


def configure_openapi(app: FastAPI) -> None:
    """
    Configure OpenAPI metadata.
    """

    app.title = settings.app_name

    app.version = settings.app_version

    app.description = """
# Enterprise AI Orchestration Platform

A production-grade enterprise AI platform providing:

- Agentic AI
- LangGraph Workflow Orchestration
- MCP Integration
- Enterprise Knowledge Platform (RAG)
- Hybrid Search
- Document Ingestion
- Multi-Agent Architecture
- Enterprise Connectors
"""

    app.contact = {
        "name": "Enterprise AI Platform Team",
        "email": "support@example.com",
    }

    app.license_info = {
        "name": "Proprietary",
    }

    app.openapi_tags = [
        {
            "name": "Health",
            "description": "Health and monitoring endpoints",
        },
        {
            "name": "Documents",
            "description": "Document ingestion and management",
        },
        {
            "name": "Knowledge",
            "description": "Knowledge retrieval APIs",
        },
        {
            "name": "Chat",
            "description": "Conversational AI APIs",
        },
        {
            "name": "Agents",
            "description": "Agent orchestration",
        },
        {
            "name": "Workflows",
            "description": "Workflow execution",
        },
        {
            "name": "Administration",
            "description": "Administrative operations",
        },
    ]