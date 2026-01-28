from django.db import models
from rest_framework.exceptions import ValidationError
from users.models import User

from .validators import validate_max_two_minutes, validate_linked_habit_is_pleasure, validate_periodicity


class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasure = models.BooleanField(default=False)
    linked_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='linked_to', validators=[validate_linked_habit_is_pleasure])
    PERIOD_CHOICES = [
        (1, 'Раз в неделю'),
        (2, 'Два раза в неделю'),
        (3, 'Три раза в неделю'),
        (7, 'Ежедневно'),
    ]
    periodicity = models.IntegerField(choices=PERIOD_CHOICES, default=1, validators=[validate_periodicity])
    reward = models.CharField(max_length=255, blank=True, null=True)
    time_spent_minutes = models.PositiveSmallIntegerField(validators=[validate_max_two_minutes])
    is_public = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        # Проверка, что связанная привычка — приятная
        if self.linked_habit and not self.linked_habit.is_pleasure:
            raise ValidationError(
                "В связанной привычке должен быть признак 'приятной привычки'."
            )
        # Проверка, что у приятной привычки нет вознаграждения и связанной привычки
        if self.is_pleasure:
            if self.reward:
                raise ValidationError("Проблема: приятная привычка не должна иметь вознаграждение.")
            if self.linked_habit:
                raise ValidationError("Проблема: приятная привычка не должна иметь связанную привычку.")
        # Проверка, что одновременно не заполнены reward и linked_habit
        if self.linked_habit and self.reward:
            raise ValidationError(
                "Можно заполнить только либо 'Связанную привычку', либо 'Вознаграждение', но не оба одновременно."
            )

    def __str__(self):
        return f"{self.action} у {self.owner}"
