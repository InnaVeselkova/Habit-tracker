from celery import shared_task
from users.models import User
from .services import send_tg_message


@shared_task
def send_habits_reminder(user_id, chat_id, remind_time):
    user = User.objects.get(id=user_id)

    def generate_habits_reminder(user, date_time):
        habits = user.habits.filter(
            time__hour=date_time.hour,
            time__minute=date_time.minute
        )
        if not habits.exists():
            return "Нет запланированных привычек на это время."
        message_lines = ["Напоминание о ваших привычках:\n"]
        for habit in habits:
            line = f"- {habit.action} в {habit.place} в {habit.time.strftime('%H:%M')}"
            if habit.reward:
                line += f" (награда: {habit.reward})"
            message_lines.append(line)
        return "\n".join(message_lines)

    message = generate_habits_reminder(user, remind_time)
    send_tg_message(chat_id, message)

