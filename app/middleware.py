import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("task-manager")

class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        method = request.method
        path = request.url.path
        query = str(request.query_params) if request.query_params else ""

        start_time = time.perf_counter()

        logger.info(f"[{request_id}] -> {method} {path} {query}")

        try:
            response = await call_next(request)
        except Exception as e:
            process_time = (time.perf_counter() - start_time) * 1000
            logger.error(f"[{request_id}] x {method} {path} - Error: {str(e)} ({process_time:.2f}ms)")
            raise
        process_time = (time.perf_counter() - start_time) * 1000

        status_emoji = "✓" if response.status_code < 400 else "x"
        logger.info(
            f"[{request_id}] {status_emoji} {method} {path}"
            f"- {response.status_code} ({process_time:.2f}ms)"
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response