import anyio
from alembic import command
from alembic.config import Config
from anyio.abc import TaskGroup
from loguru import logger

from config import config
from Infrastructure.Argparse.setup_argparse import setup_argparse
from Infrastructure.Logging.logger import setup_logging
from Infrastructure.Scheduler.scheduler import setup_scheduler
from Services.TelegramBotService.start_polling_bot import start_polling_bot
from Services.TemplateApiServise.WebApi.app import uvicorn_server


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", config.database_config.url)
    command.upgrade(alembic_cfg, "head")


async def start_web(tg: TaskGroup):
    await uvicorn_server.serve()

    tg.cancel_scope.cancel()


async def main():
    setup_logging(config.app_config.log_level)
    parse_args = setup_argparse()

    if all(arg is False for arg in parse_args.__dict__.values()):
        logger.critical("Please check your arguments or --help  show this help message and exit.")
        raise SystemExit

    async with anyio.create_task_group() as tg:
        tg.start_soon(setup_scheduler)  # type: ignore

        if parse_args.server:
            tg.start_soon(start_web, tg)

        if parse_args.bot:
            tg.start_soon(start_polling_bot)


if __name__ == "__main__":
    try:
        run_migrations()
        anyio.run(main)
    except SystemExit:  # /NOSONAR
        logger.info("Exiting")
