import anyio
from alembic import command
from alembic.config import Config
from loguru import logger

from config import settings
from Infrastructure.Argparse.setup_argparse import setup_argparse
from Infrastructure.Logging.logger import setup_logging  # type: ignore
from Infrastructure.Scheduler.scheduler import setup_scheduler  # type: ignore
from Services.TelegramBotService.bot_main import bot_main  # type: ignore
from Services.TemplateApiServise.WebApi.app import uvicorn_server  # type: ignore


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_config.url)
    command.upgrade(alembic_cfg, "head")


async def main():
    setup_logging(settings.app_config.log_level)
    parse_args = setup_argparse()

    if any(arg is False for arg in parse_args.__dict__.values()):
        logger.critical("Please check your arguments or --help  show this help message and exit.")

    async with anyio.create_task_group() as tg:
        tg.start_soon(setup_scheduler)  # type: ignore

        if parse_args.server:
            tg.start_soon(uvicorn_server.serve)

        if parse_args.bot:
            tg.start_soon(bot_main)


if __name__ == "__main__":
    try:
        run_migrations()
        anyio.run(main)
    except SystemExit:  # /NOSONAR
        logger.info("Exiting")
