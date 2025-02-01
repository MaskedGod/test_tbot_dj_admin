from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import Category, Subcategory
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
