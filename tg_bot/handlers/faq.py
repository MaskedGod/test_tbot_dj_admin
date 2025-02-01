from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import get_faq_keyboard
from database.db import async_session
from tg_bot.database.models import FAQ

faq_router = Router()


@faq_router.message(F.text == "FAQ")
async def show_faq(message: Message):
    async with async_session() as session:
        keyboard = await get_faq_keyboard(session)
    await message.answer("Часто задаваемые вопросы:", reply_markup=keyboard)


@faq_router.callback_query(F.data.startswith("faq_"))
async def show_faq_answer(callback: CallbackQuery):
    faq_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        faq = (
            await session.execute(FAQ.__table__.select().where(FAQ.id == faq_id))
        ).scalar_one_or_none()
    if faq:
        await callback.message.answer(f"{faq.question}\n\n{faq.answer}")
    else:
        await callback.message.answer("Вопрос не найден.")
