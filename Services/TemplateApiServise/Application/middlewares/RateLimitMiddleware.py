from http import HTTPStatus

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from Services.TemplateApiServise.Persistence.Repository.Cache.CacheInstanceRepository import cache_repository_instance

PER_SECONDS_LIMIT = 50


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> JSONResponse | Response:
        key = f"rate:{request.client.host}:{request.url.path}"

        counter = await cache_repository_instance.incr(key)
        if counter == 1:
            await cache_repository_instance.expire(key, PER_SECONDS_LIMIT)
        elif counter > PER_SECONDS_LIMIT:
            return JSONResponse(status_code=HTTPStatus.TOO_MANY_REQUESTS, content="Too Many Requests")

        return await call_next(request)
