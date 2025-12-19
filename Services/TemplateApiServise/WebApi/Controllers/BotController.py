import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import APIRouter, Depends

from config import config
from Services.TelegramBotService.get_bot import get_bot
from Services.TelegramBotService.get_dispatcher import get_dispatcher

bot_router = APIRouter()

tasks = set()


@bot_router.post(f"/bot/{config.bot_config.webhook_path}", include_in_schema=False)
async def process_tg_webhook(
    update: Update,
    bot: Bot = Depends(get_bot),
    dp: Dispatcher = Depends(get_dispatcher),
):
    task = asyncio.create_task(dp.feed_update(bot, update))
    tasks.add(task)
    task.add_done_callback(lambda t: tasks.remove(t))

    return {"status": "ok"}
