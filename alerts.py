# Оповещения в Telegram и Slack. Ключи берём из переменных окружения,
# если их нет - просто печатаем сообщение (учебный режим)
import json
import os
import urllib.request


def _post(url, data):
    req = urllib.request.Request(url, json.dumps(data).encode("utf-8"),
                                 {"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)


def send_alert(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    slack_url = os.getenv("SLACK_WEBHOOK_URL")

    if token and chat_id:
        _post(f"https://api.telegram.org/bot{token}/sendMessage",
              {"chat_id": chat_id, "text": text})
    else:
        print("  [Telegram, учебный режим]", text)

    if slack_url:
        _post(slack_url, {"text": text})
    else:
        print("  [Slack, учебный режим]", text)
