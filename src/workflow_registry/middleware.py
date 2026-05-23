"""Request context middleware — propagates KDD platform tracing headers."""

import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_CONTEXT_HEADERS = (
    "X-Request-ID",
    "X-Workflow-ID",
    "X-Trace-ID",
    "X-Actor-ID",
    "X-Session-ID",
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        ctx: dict = {}
        for header in _CONTEXT_HEADERS:
            value = request.headers.get(header)
            if header == "X-Request-ID" and not value:
                value = str(uuid.uuid4())
            ctx[header] = value
            request.state.__dict__[header.lower().replace("-", "_")] = value

        response: Response = await call_next(request)
        for header, value in ctx.items():
            if value:
                response.headers[header] = value
        return response
