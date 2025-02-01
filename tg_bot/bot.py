import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError
from dotenv import load_dotenv
from database.db import init_db
from handlers.catalog import catalog_router
from handlers.cart import cart_router
from handlers.faq import faq_router
from handlers.export import export_router


load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
dp.include_router(catalog_router)
dp.include_router(cart_router)
dp.include_router(faq_router)
dp.include_router(export_router)


CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))


@dp.message(commands=["start"])
async def start(message: Message):
    user_id = message.from_user.id

    try:
        channel_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if channel_member.status not in ["member", "administrator", "creator"]:
            await message.answer(
                "Пожалуйста, подпишитесь на наш канал, чтобы продолжить."
            )
            return
    except TelegramAPIError:
        await message.answer("Произошла ошибка при проверке подписки на канал.")
        return

    try:
        group_member = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        if group_member.status not in ["member", "administrator", "creator"]:
            await message.answer(
                "Пожалуйста, присоединитесь к нашей группе, чтобы продолжить."
            )
            return
    except TelegramAPIError:
        await message.answer("Произошла ошибка при проверке подписки на группу.")
        return

    await message.answer("Спасибо за подписку! Вы можете использовать бота.")


async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
