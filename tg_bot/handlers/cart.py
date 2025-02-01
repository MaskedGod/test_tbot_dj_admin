from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import get_cart_keyboard
from database.db import async_session
from tg_bot.database.models import Cart
from utils.payment import create_payment

cart_router = Router()


@cart_router.message(F.text == "Корзина")
async def show_cart(message: Message):
    user_id = message.from_user.id
    async with async_session() as session:
        keyboard = await get_cart_keyboard(user_id, session)
    await message.answer("Ваша корзина:", reply_markup=keyboard)


@cart_router.callback_query(F.data.startswith("cart_item_"))
async def remove_from_cart(callback: CallbackQuery):
    cart_item_id = int(callback.data.split("_")[2])
    async with async_session() as session:
        cart_item = (
            await session.execute(
                Cart.__table__.select().where(Cart.id == cart_item_id)
            )
        ).scalar_one_or_none()
        if cart_item:
            await session.delete(cart_item)
            await session.commit()
            await callback.answer("Товар удален из корзины.")
        else:
            await callback.answer("Товар не найден.")
    user_id = callback.from_user.id
    keyboard = await get_cart_keyboard(user_id, session)
    await callback.message.edit_text("Ваша корзина:", reply_markup=keyboard)


@cart_router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        cart_items = (
            (
                await session.execute(
                    Cart.__table__.select().where(Cart.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        if not cart_items:
            await callback.message.answer("Ваша корзина пуста.")
            return
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        text = "Ваш заказ:\n"
        for item in cart_items:
            product = item.product
            text += f"{product.name} ({item.quantity} шт.) - {product.price * item.quantity} руб.\n"
        text += f"\nИтого: {total_price} руб."
        await callback.message.answer(text)
        await session.execute(Cart.__table__.delete().where(Cart.user_id == user_id))
        await session.commit()
    await callback.message.answer("Спасибо за заказ!")


@cart_router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery):
    user_id = callback.from_user.id
    async with async_session() as session:
        cart_items = (
            (
                await session.execute(
                    Cart.__table__.select().where(Cart.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        if not cart_items:
            await callback.message.answer("Ваша корзина пуста.")
            return
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        text = "Ваш заказ:\n"
        for item in cart_items:
            product = item.product
            text += f"{product.name} ({item.quantity} шт.) - {product.price * item.quantity} руб.\n"
        text += f"\nИтого: {total_price} руб."
        await callback.message.answer(text)

        confirmation_url, payment_id = create_payment(
            total_price, "Оплата заказа", user_id
        )
        await callback.message.answer(
            f"Для оплаты перейдите по ссылке: {confirmation_url}"
        )
        await session.execute(Cart.__table__.delete().where(Cart.user_id == user_id))
        await session.commit()
