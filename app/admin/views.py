from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response
from app.web.mixins import AuthRequiredMixin


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        admin: dict = self.data
        admin['id']: int = 1
        admin_config = await self.store.admins.get_by_email(admin["email"])
        if admin_config:
            if admin_config.is_password_valid(admin["password"]):
                session = await new_session(request=self.request)
                session["admin"] = admin
                return json_response(
                    data={
                        "id": admin_config.id,
                        "email": admin_config.email,
                    },
                )
        raise HTTPForbidden


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        if not self.request.cookies:
            raise HTTPUnauthorized
        if not getattr(self.request, "admin", None):
            raise HTTPForbidden
        check_valid_email_admin = await self.store.admins.get_by_email(self.request.admin.email)
        if check_valid_email_admin and check_valid_email_admin.id == self.request.admin.id:
            return json_response(
                data={
                    "id": self.request.admin.id,
                    "email": self.request.admin.email,
                },
            )


#Добавить middlewares где будет проверяться авторизация и выводиться ответ, либо решить с декоратором, либо проверять наличие для каждого View in self.store.admins