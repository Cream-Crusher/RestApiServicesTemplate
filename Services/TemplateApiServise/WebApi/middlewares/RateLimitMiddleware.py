from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from Services.TemplateApiServise.Persistence.Repository.Cache.CacheInstanceRepository import cache_repository_instance

RPS_LIMIT = 1


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> JSONResponse | Response:
        key = f"rate:{request.client.host}:{request.url.path}"

        counter = await cache_repository_instance.incr(key)
        if counter == 1:
            await cache_repository_instance.expire(key, RPS_LIMIT)
        elif counter > RPS_LIMIT:
            return JSONResponse(
                status_code=429,
                content={
                    "status": "error",
                    "error": "TOO_MANY_REQUESTS",
                    "message": f"Too Many Requests by {key}",
                    "detail": {"key": key, "rps_limit": RPS_LIMIT},
                },
            )

        return await call_next(request)
