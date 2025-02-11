import anyio
from alembic import command
from alembic.config import Config

from Services.TemplateApiServise.WebApi.app import uvicorn_server
from Services.TemplateApiServise.WebApi.config import settings


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_config.url)
    command.upgrade(alembic_cfg, "head")


async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(uvicorn_server.serve)
        # tg.start_soon(bot_main)


if __name__ == "__main__":
    run_migrations()
    anyio.run(main)
