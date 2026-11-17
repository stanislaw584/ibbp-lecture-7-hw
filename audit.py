# Журнал аудита: каждое событие дописываем строкой в файл с временем
from datetime import datetime

LOG_FILE = "audit.log"


def log(event, message):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} | {event} | {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
