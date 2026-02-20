import io

from aiogram import Bot
from aiogram.types.file import File
from async_lru import alru_cache

from Services.TelegramBotService.get_bot import get_bot


@alru_cache
async def get_bot_file(
    file_id: str,
) -> io.BytesIO:
    bot: Bot = get_bot()
    object_data = io.BytesIO()
    file: File = await bot.get_file(file_id=file_id)

    if file.file_path is None:
        raise ValueError(f"File path is None for file_id: {file_id}")

    await bot.download_file(file_path=file.file_path, destination=object_data)
    object_data.seek(0)

    return object_data
