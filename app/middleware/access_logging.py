"""
Enterprise Access Logging Middleware.

Responsibilities:
- Generate Request ID
- Measure processing time
- Log request and response
- Add response headers
"""

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging.logger import get_logger

logger = get_logger(__name__)


class AccessLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        start_time = time.perf_counter()
        
        response = await call_next(request)

        elapsed_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{elapsed_ms} ms"

        logger.info(
            "HTTP Request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": elapsed_ms,
                "client_ip": request.client.host if request.client else "-",
            },
        )

        return response