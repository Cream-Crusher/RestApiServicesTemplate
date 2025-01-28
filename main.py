import anyio
import uvicorn.config
from alembic import command
from alembic.config import Config

from Services.TemplateApiServise.WebApi.config import settings
from Services.TemplateApiServise.WebApi.app import app
from Services.TelegramBotService.bot import main as bot_main

config = uvicorn.config.Config(
    app,
    host="0.0.0.0",
    port=8011,
)
server = uvicorn.Server(config=config)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_config.url)
    command.upgrade(alembic_cfg, "head")


async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(server.serve)
        # tg.start_soon(bot_main)


if __name__ == "__main__":
    run_migrations()
    anyio.run(main)
