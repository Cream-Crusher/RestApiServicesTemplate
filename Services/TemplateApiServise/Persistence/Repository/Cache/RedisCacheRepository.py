from redis.asyncio import Redis


class RedisCacheRepository(Redis):

    def __init__(self, host: str) -> None:
        super().__init__(  # type: ignore
            host=host,
            decode_responses=True
        )
