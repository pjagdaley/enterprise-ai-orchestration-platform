"""
Health check endpoints.
"""

from fastapi import APIRouter

from app.core.config import settings

from app.core.exceptions import ResourceNotFoundException

router = APIRouter(tags=["Health"])


@router.get(
    "/",
    summary="Root Endpoint",
    description="Returns basic application information.",
)
async def root():
    """
    Root endpoint.
    """
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running",
    }


@router.get(
    "/health",
    summary="Health Check",
    description="Returns application health status.",
)
async def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
    }


@router.get(
    "/live",
    summary="Liveness Probe",
    description="Kubernetes/Cloud Run liveness probe.",
)
async def live():
    """
    Liveness probe.
    """
    return {
        "status": "alive",
    }


@router.get(
    "/ready",
    summary="Readiness Probe",
    description="Kubernetes/Cloud Run readiness probe.",
)
async def ready():
    """
    Readiness probe.
    """

    # Future checks:
    # - Firestore
    # - Vertex AI
    # - Qdrant
    # - MCP
    # - Tool Registry

    return {
        "status": "ready",
    }

# For testing error handling, you can use this endpoint to raise a ResourceNotFoundException.
@router.get("/test-error")
async def test_error():
    raise ResourceNotFoundException("Document")

@router.get("/large-response")
async def large_response():
    return {
        "data": ["Enterprise AI Platform"] * 5000
    }