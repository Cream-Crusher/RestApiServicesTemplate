import argparse
from argparse import Namespace


def setup_argparse() -> Namespace:
    parser = argparse.ArgumentParser(description="Run servise")
    parser.add_argument(
        "--server",
        action="store_true",
        help="Run uvicorn_server servise",
    )
    parser.add_argument(
        "--bot",
        action="store_true",
        help="Run telegram_bot servise",
    )
    return parser.parse_args()
