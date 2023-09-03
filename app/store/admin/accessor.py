import typing
from hashlib import sha256
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        # TODO: создать админа по данным в config.yml здесь
        admin = await self.create_admin(email=self.app.config.admin.email, password=self.app.config.admin.password)
        self.app.database.admins.append(admin)

    async def get_by_email(self, email: str) -> Optional[Admin]:
        for admin in self.app.database.admins:
            if email == admin.email:
                return admin

    async def create_admin(self, email: str, password: str) -> Admin:
        id_ = len(self.app.database.admins) + 1
        password = sha256(password.encode()).hexdigest()
        return Admin(id=id_, email=email, password=password)
