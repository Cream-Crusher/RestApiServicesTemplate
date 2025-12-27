class RateLimitError(Exception):

    def __init__(self, key: str, max_calls: int, period_seconds: int):
        self.key = key
        self.max_calls = max_calls
        self.period_seconds = period_seconds

    def __str__(self):
        return str(
            {
                "message": f"Too Many Requests by {self.key}", "detail": {
                    "key": self.key, "rps_limit": self.max_calls / self.period_seconds
                }
            }
        )
