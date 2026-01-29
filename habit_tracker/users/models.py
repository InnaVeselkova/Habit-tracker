from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    tg_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Telegram Chat", help_text="Укажите телеграмм chat_id"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
