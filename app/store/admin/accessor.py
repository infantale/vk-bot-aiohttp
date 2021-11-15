import typing
from hashlib import sha256
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: 'Application'):
        self.app = app
        # TODO: создать админа по данным в config.yml здесь
        admin_email = self.app.config.admin.email
        admin_password = sha256(self.app.config.admin.password.encode())
        await self.create_admin(admin_email, admin_password)

    async def disconnect(self, _: 'Application'):
        self.app = None

    async def get_by_email(self, email: str) -> Optional[Admin]:
        if email == self.app.database.admins[0].email:
            return self.app.database.admins[0]
        else:
            return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = Admin(id=1, email=email, password=password)
        self.app.database.admins.append(admin)