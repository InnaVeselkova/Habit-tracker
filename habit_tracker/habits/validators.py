from django.core.exceptions import ValidationError

PERIOD_CHOICES = [
    (1, "Раз в неделю"),
    (2, "Два раза в неделю"),
    (3, "Три раза в неделю"),
    (7, "Ежедневно"),
]


def validate_max_two_minutes(value):
    if value > 120:
        raise ValidationError("Время не должно превышать 2 минут (120 секунд).")


def validate_linked_habit_is_pleasure(value):
    from .models import Habit

    if value:
        print(f"value={value}")
        try:
            habit = Habit.objects.get(pk=value)
        except Habit.DoesNotExist:
            raise ValidationError("Связанная привычка не найдена.")
        if not habit.is_pleasure:
            raise ValidationError("В связанной привычке должна быть признак 'приятной привычки'.")


def validate_periodicity(value):
    allowed_values = [choice[0] for choice in PERIOD_CHOICES]
    if value not in allowed_values:
        raise ValidationError("Недопустимое значение периодичности.")
