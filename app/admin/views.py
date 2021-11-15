import base64

from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import get_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response, check_basic_admin_auth


class AdminLoginView(View):
    @docs(tags=['bot admin'], summary='Admin Login', discription='Superadmin login view')
    @request_schema(AdminSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        # print('AdminLoginView')
        session = await get_session(self.request)
        data = await self.request.json()
        email = data['email']
        password = data['password']
        auth_data = email + ':' + password
        auth_data_bytes = auth_data.encode('ascii')
        base64_bytes = base64.b64encode(auth_data_bytes)
        if email == self.request.app.config.admin.email and password == self.request.app.config.admin.password:
            header_value = "Basic " + base64_bytes.decode('ascii')
            session['Authorization'] = header_value
            return json_response(
                data={'id': self.request.app.database.admins[0].id,
                        'email': self.request.app.database.admins[0].email}
            )
        else:
            raise HTTPForbidden


class AdminCurrentView(View):
    @docs(tags=['bot admin'], summary='Current Admin', discription='Get information about current admin')
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        session = await get_session(self.request)
        if not session['Authorization']:
            raise HTTPUnauthorized
        auth_header_value = session['Authorization'].replace('Basic ', '')
        if check_basic_admin_auth(auth_header_value, self.request.app.config.admin.email,
                                  self.request.app.config.admin.password):
            raise HTTPForbidden
        return json_response(
                data={'id': self.request.app.database.admins[0].id,
                    'email': self.request.app.database.admins[0].email}
        )
