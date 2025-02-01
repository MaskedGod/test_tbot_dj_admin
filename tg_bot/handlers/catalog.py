from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from keyboards.keyboards import (
    get_categories_keyboard,
    get_subcategories_keyboard,
    get_products_keyboard,
)
from database.db import async_session
from tg_bot.database.models import Product, Cart

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
    async with async_session() as session:
        keyboard = await get_products_keyboard(subcategory_id, session)
    await callback.message.edit_text("Выберите товар:", reply_markup=keyboard)


@catalog_router.callback_query(F.data.startswith("product_"))
async def show_product_details(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        product = (
            await session.execute(
                Product.__table__.select().where(Product.id == product_id)
            )
        ).scalar_one_or_none()
    if product:
        text = f"{product.name}\n\n{product.description}\n\nЦена: {product.price} руб."
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Добавить в корзину",
                        callback_data=f"add_to_cart_{product.id}",
                    )
                ]
            ]
        )
        await callback.message.answer_photo(
            photo=product.photo_url, caption=text, reply_markup=keyboard
        )
    else:
        await callback.message.answer("Товар не найден.")


@catalog_router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id
    async with async_session() as session:
        cart_item = (
            await session.execute(
                Cart.__table__.select().where(
                    Cart.user_id == user_id, Cart.product_id == product_id
                )
            )
        ).scalar_one_or_none()
        if cart_item:
            cart_item.quantity += 1
        else:
            new_item = Cart(user_id=user_id, product_id=product_id)
            session.add(new_item)
        await session.commit()
    await callback.answer("Товар добавлен в корзину!")
