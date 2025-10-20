from fastapi import Query


class Pagination:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="page > 1"),
        size: int = Query(default=100, le=100, description="size > 1 and <= 100"),
    ):

        self.page: None | int = page
        self.size: int | None = size
        self.skip: int | None = (page - 1) * size if page and size else 0
        self.limit: int | None = size
