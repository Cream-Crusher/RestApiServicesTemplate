from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from Infrastructure.Redis.Client import async_redis_client

RPS_LIMIT = 1


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> JSONResponse | Response:
        key = f"rate:{request.client.host}:{request.url.path}"

        counter = await async_redis_client.incr(key)
        if counter == 1:
            await async_redis_client.expire(key, RPS_LIMIT)
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
