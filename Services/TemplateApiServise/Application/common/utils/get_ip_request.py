from starlette_context import context


def get_ip_request() -> str:
    x_forwarded_for = context.data["X-Forwarded-For"]
    return context.data["X-Forwarded-For"].split(",")[0] if x_forwarded_for is not None else "None"
