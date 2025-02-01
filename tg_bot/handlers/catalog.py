from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import get_categories_keyboard, get_subcategories_keyboard
from database.db import async_session

catalog_router = Router()


@catalog_router.message(F.text == "Каталог")
async def show_catalog(message: Message):
    async with async_session() as session:
        keyboard = await get_categories_keyboard(session)
    await message.answer("Выберите категорию:", reply_markup=keyboard)


@catalog_router.callback_query(F.data.startswith("category_"))
async def show_subcategories(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        keyboard = await get_subcategories_keyboard(category_id, session)
    await callback.message.edit_text("Выберите подкатегорию:", reply_markup=keyboard)


@catalog_router.callback_query(F.data.startswith("subcategory_"))
async def show_products(callback: CallbackQuery):
    subcategory_id = int(callback.data.split("_")[1])
    await callback.message.answer(f"Товары из подкатегории {subcategory_id}")
