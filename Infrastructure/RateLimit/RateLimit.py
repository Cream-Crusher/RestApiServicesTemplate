import asyncio
import time
from collections import deque
from typing import Any

from typing_extensions import Deque


class RateLimitExceeded(Exception):
    pass


class RateLimit:
    def __init__(self, max_calls: int, period_seconds: int):
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls_by_key: dict[Any, Deque[float]] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, key: str = "base"):
        async with self._lock:
            now = time.time()
            dq = self.calls_by_key.get(key)
            if dq is None:
                dq = deque()
                self.calls_by_key[key] = dq

            while dq and now - dq[0] > self.period:
                dq.popleft()

            if len(dq) >= self.max_calls:
                raise RateLimitExceeded(f"Превышен лимит запросов для ключа: {key}")

            dq.append(now)


ip_limiter = RateLimit(5, 600)
# Пример использования: await ip_limiter.acquire(x_forwarded_for)
