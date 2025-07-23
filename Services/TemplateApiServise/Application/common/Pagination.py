from fastapi import HTTPException, Query


class Pagination:
    def __init__(
        self,
        page: int | None = Query(default=None, ge=1, description="page > 1"),
        size: int | None = Query(default=None, le=50, description="size > 1 and <= 50"),
    ):

        if (not page and size) or (page and not size):
            raise HTTPException(status_code=400, detail="page and size must be specified together")

        self.page: None | int = page
        self.size: int | None = size
        self.skip: int | None = (page - 1) * size if page and size else 0
        self.limit: int | None = size
