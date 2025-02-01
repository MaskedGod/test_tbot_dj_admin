import os
from dotenv import load_dotenv
from yookassa import Configuration, Payment


load_dotenv()


Configuration.account_id = os.getenv("PAYMENT_SHOP_ID")
Configuration.secret_key = os.getenv("PAYMENT_SECRET_KEY")


def create_payment(amount: float, description: str, user_id: int):
    payment = Payment.create(
        {
            "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://yourwebsite.com/success",  # URL для успешной оплаты
            },
            "description": description,
            "metadata": {"user_id": user_id},
        }
    )
    return payment.confirmation.confirmation_url, payment.id
