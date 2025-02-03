from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BroadcastForm
from aiogram import Bot
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


bot = Bot(token=os.getenv("BOT_TOKEN"))


def broadcast_message(request):
    if request.method == "POST":
        form = BroadcastForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            user_ids = [123456789, 987654321]
            for user_id in user_ids:
                asyncio.run(bot.send_message(chat_id=user_id, text=message))
            messages.success(request, "Сообщение успешно отправлено!")
            return redirect("broadcast")
        else:
            form = BroadcastForm()
    return render(request, "shop/broadcast.html", {"form": form})
