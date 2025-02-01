from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import Category, Subcategory, Product, Cart, FAQ
from sqlalchemy.ext.asyncio import AsyncSession


async def get_categories_keyboard(session: AsyncSession):
    categories = (await session.execute(Category.__table__.select())).scalars().all()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category.name, callback_data=f"category_{category.id}"
            )
        )
    return keyboard


async def get_subcategories_keyboard(category_id: int, session: AsyncSession):
    subcategories = (
        (
            await session.execute(
                Subcategory.__table__.select().where(
                    Subcategory.category_id == category_id
                )
            )
        )
        .scalars()
        .all()
    )
    keyboard = InlineKeyboardMarkup(row_width=2)
    for subcategory in subcategories:
        keyboard.add(
            InlineKeyboardButton(
                text=subcategory.name, callback_data=f"subcategory_{subcategory.id}"
            )
        )
    return keyboard


async def get_products_keyboard(subcategory_id: int, session: AsyncSession):
    products = (
        (
            await session.execute(
                Product.__table__.select().where(
                    Product.subcategory_id == subcategory_id
                )
            )
        )
        .scalars()
        .all()
    )
    keyboard = InlineKeyboardMarkup(row_width=2)
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=product.name, callback_data=f"product_{product.id}"
            )
        )
    return keyboard


async def get_cart_keyboard(user_id: int, session: AsyncSession):
    cart_items = (
        (await session.execute(Cart.__table__.select().where(Cart.user_id == user_id)))
        .scalars()
        .all()
    )
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in cart_items:
        product = item.product
        text = f"{product.name} ({item.quantity} шт.)"
        keyboard.add(
            InlineKeyboardButton(text=text, callback_data=f"cart_item_{item.id}")
        )
    keyboard.add(InlineKeyboardButton(text="Оформить заказ", callback_data="checkout"))
    return keyboard


async def get_faq_keyboard(session: AsyncSession):
    faqs = (await session.execute(FAQ.__table__.select())).scalars().all()
    keyboard = InlineKeyboardMarkup(row_width=1)
    for faq in faqs:
        keyboard.add(
            InlineKeyboardButton(text=faq.question, callback_data=f"faq_{faq.id}")
        )
    return keyboard
