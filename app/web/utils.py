from typing import Any, Optional

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


def json_response(data: Any = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: Optional[str] = None,
    data: Optional[dict] = None,
):
    from app.web.middlewares import HTTP_ERROR_CODES
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": HTTP_ERROR_CODES[http_status],
            "message": str(message),
            "data": data,
        },
    )
