from django.core.exceptions import ValidationError

def validate_max_two_minutes(value):
    if value > 120:
        raise ValidationError('Время не должно превышать 2 минут (120 секунд).')


def validate_linked_habit_is_pleasure(value):
    if value and not value.is_pleasure:
        raise ValidationError("В связанной привычке должна быть признак 'приятной привычки'.")


def validate_periodicity(value):
    if value and value < 7:
        raise ValidationError("Периодичность не должна быть менее 7 дней.")
