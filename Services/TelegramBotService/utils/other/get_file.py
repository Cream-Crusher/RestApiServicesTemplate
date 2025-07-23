import io

from aiogram import Bot
from aiogram.types.file import File
from async_lru import alru_cache

from Services.TelegramBotService.get_bot import get_bot
from Services.TemplateApiServise.Persistence.Repository.S3.MinioRepository import (
    s3_manager,
)


@alru_cache
async def get_bot_file_url(file_id: str, content_type: str = "image/png") -> str:
    bot: Bot = get_bot()
    object_data = io.BytesIO()
    file: File = await bot.get_file(file_id=file_id)
    assert file.file_path is not None, f"File path is None for file_id: {file_id}"

    await bot.download_file(file_path=file.file_path, destination=object_data)
    object_data.seek(0)

    file_url: str = await s3_manager.update(
        body=object_data,
        object_name=f"{file_id}.png",
        bucket_name="user-avatar",
        content_type=content_type,
    )

    return file_url
