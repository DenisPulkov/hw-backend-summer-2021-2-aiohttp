from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden


class AuthRequiredMixin:
    # TODO: можно использовать эту mixin-заготовку для реализации проверки авторизации во View
    async def _iter(self) -> StreamResponse:
        if not self.request.cookies:
            raise HTTPUnauthorized
        if not getattr(self.request, "admin", None):
            raise HTTPForbidden
        return await super(AuthRequiredMixin, self)._iter()
