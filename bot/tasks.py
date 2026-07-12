import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from habits.models import Habit


@shared_task
def send_telegram_message(chat_id, message):
    """Send message to Telegram"""
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@shared_task
def send_habit_reminders():
    """Send habit reminders"""
    now = timezone.now()
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
    )

    print(f"Ищем привычки на {current_time.hour}:{current_time.minute}")
    print(f"Найдено: {habits.count()} привычек")

    for habit in habits:
        user = habit.user
        chat_id = user.telegram_chat_id

        if chat_id:
            message = (
                f"Reminder!\n"
                f"Habit: {habit.action}\n"
                f"Place: {habit.place}\n"
                f"Time: {habit.time}\n"
            )
            send_telegram_message.delay(chat_id, message)
        else:
            print(f"У пользователя {user.username} нет Telegram ID")

    return f"Sent {habits.count()} reminders"
