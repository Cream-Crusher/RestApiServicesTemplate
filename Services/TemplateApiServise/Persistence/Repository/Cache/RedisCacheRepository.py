from redis.asyncio import Redis


class RedisCacheRepository(Redis):

    def __init__(self, host: str) -> None:
        super().__init__(host=host, decode_responses=True)  # type: ignore
