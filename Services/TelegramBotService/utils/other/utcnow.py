from datetime import datetime, timezone


def utcnow(**kw) -> datetime:
    return datetime.now(timezone.utc).replace(**kw, tzinfo=None)
