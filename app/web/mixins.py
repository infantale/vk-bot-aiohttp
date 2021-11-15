from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp_session import get_session


class AuthRequiredMixin:
    # TODO: можно использовать эту mixin-заготовку для реализации проверки авторизации во View
    # YWRtaW5AYWRtaW4uY29tOmFkbWlu
    async def auth_required(self):
        session = await get_session(self.request)
        # session['Authorization'] = None
        if not session['Authorization']:
            raise HTTPUnauthorized
