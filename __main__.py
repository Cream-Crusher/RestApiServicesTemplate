import anyio
from alembic import command
from alembic.config import Config
from loguru import logger

from Infrastructure.Scheduler.scheduler import setup
from Services.TelegramBotService.bot_main import bot_main
from Services.TemplateApiServise.WebApi.app import uvicorn_server
from config import settings


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_config.url)
    command.upgrade(alembic_cfg, "head")


async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(uvicorn_server.serve)
        tg.start_soon(setup)

        # tg.start_soon(bot_main)


if __name__ == "__main__":
    try:
        run_migrations()
        anyio.run(main)
    except SystemExit:
        logger.info("Exiting")
