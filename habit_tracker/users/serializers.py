from django.contrib.auth import authenticate

from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Попытка аутентификации пользователя по email и паролю
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Некорректные учетные данные.")

        if not user.is_active:
            raise serializers.ValidationError("Пользователь заблокирован или не активен.")

        data["user"] = user
        return data
