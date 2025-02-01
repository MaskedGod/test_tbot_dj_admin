import os
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import Message
from openpyxl import Workbook
from database.db import async_session
from tg_bot.database.models import Order

export_router = Router()


load_dotenv()

ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(",")))


@export_router.message(F.text == "Выгрузить заказы")
async def export_orders(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    async with async_session() as session:
        orders = (await session.execute(Order.__table__.select())).scalars().all()

    if not orders:
        await message.answer("Нет заказов для выгрузки.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Заказы"
    ws.append(
        ["ID заказа", "Пользователь ID", "Товары", "Общая стоимость", "Дата создания"]
    )

    for order in orders:
        ws.append(
            [order.id, order.user_id, order.items, order.total_price, order.created_at]
        )

    file_path = "orders.xlsx"
    wb.save(file_path)

    with open(file_path, "rb") as file:
        await message.answer_document(file)

    os.remove(file_path)
