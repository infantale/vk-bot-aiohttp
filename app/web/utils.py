import base64
import typing
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
) -> Response:

    if data is None:
        data = {}

    response = aiohttp_json_response(
        data={
            'http_status': http_status,
            'status': status,
            'message': str(message),
            'data': data
        }
    )

    response.set_status(http_status)

    return response


def check_basic_admin_auth(raw_credentials: str, username: str, password: str) -> bool:
    credentials = base64.b64decode(raw_credentials).decode()
    parts = credentials.split(':')
    if len(credentials) != 2:
        return False
    return parts[0] == username and parts[1] == password

