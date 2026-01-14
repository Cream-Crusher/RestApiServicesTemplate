class BaseApiError(Exception):

    def __init__(self, status_code: int, error: str, message: str | None = None, detail: dict | None = None):
        self.success = False
        self.status_code = status_code
        self.error = error
        self.message = message
        self.detail = detail
        super().__init__()

    def __str__(self):
        return str({"error": self.error, "message": self.message, "detail": self.detail})
