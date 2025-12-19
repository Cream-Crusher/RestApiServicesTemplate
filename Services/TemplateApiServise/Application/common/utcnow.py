from datetime import datetime, timezone
from typing import Any


def utcnow(**kw: Any) -> datetime:
    return datetime.now(timezone.utc).replace(**kw)
