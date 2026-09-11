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


def run_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", config.database_config.url)
    command.upgrade(alembic_cfg, "head")


async def start_web(task_group: TaskGroup) -> None:
    await uvicorn_server.serve()
    task_group.cancel_scope.cancel()


async def run_services() -> None:
    setup_logging(config.app_config.log_level)
    parsed_args = setup_argparse()
    if not parsed_args.server and not parsed_args.bot:
        logger.error("Select --server or --bot. Use --help for details.")
        return

    async with anyio.create_task_group() as task_group:
        task_group.start_soon(setup_scheduler)

        if parsed_args.server:
            task_group.start_soon(start_web, task_group)

        if parsed_args.bot:
            task_group.start_soon(start_polling_bot)


if __name__ == "__main__":
    try:
        run_migrations()
        anyio.run(run_services)
    except SystemExit:  # NOSONAR
        logger.info("Exiting")
