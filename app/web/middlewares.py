import json
import typing

from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPUnauthorized, HTTPForbidden, HTTPConflict, \
    HTTPMethodNotAllowed, HTTPNotFound
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import session_middleware, SimpleCookieStorage

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: 'Request', handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401],
            message=e.reason,
            data=e.text,
        )
    except HTTPForbidden as e:
        return error_json_response(
            http_status=e.status_code,
            status=HTTP_ERROR_CODES[403],
            message=e.reason,
            data=e.text,
        )
    except HTTPNotFound as e:
        return error_json_response(
            http_status=404,
            status=HTTP_ERROR_CODES[404],
            message=e.reason,
            data=e.text,
        )
    except HTTPMethodNotAllowed as e:
        return error_json_response(
            http_status=405,
            status=HTTP_ERROR_CODES[405],
            message=e.reason,
            data=e.text,
        )
    except HTTPConflict as e:
        return error_json_response(
            http_status=409,
            status=HTTP_ERROR_CODES[409],
            message=e.reason,
            data=e.text,
        )
    except Exception as server_error:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=str(server_error),
        )
    # TODO: обработать все исключения-наследники HTTPException и отдельно Exception, как server error
    #  использовать текст из HTTP_ERROR_CODES


def setup_middlewares(app: 'Application'):
    app.middlewares.append(session_middleware(SimpleCookieStorage()))
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
