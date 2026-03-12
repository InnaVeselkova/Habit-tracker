import requests
from django.conf import settings


def send_tg_message(tg_chat_id, message):
    params = {"text": message, "chat_id": tg_chat_id}
    requests.get(f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params)
