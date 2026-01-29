from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    linked_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("owner",)

    def validate_linked_habit(self, value):
        if value is not None:
            if not value.is_pleasure:
                raise serializers.ValidationError("В связанной привычке должна быть признак 'приятной привычки'.")
        return value

    def validate(self, data):
        is_pleasure = data.get("is_pleasure")
        linked_habit = data.get("linked_habit")

        if is_pleasure:
            if data.get("reward"):
                raise serializers.ValidationError({"reward": "Приятная привычка не должна иметь вознаграждение."})
            if linked_habit:
                raise serializers.ValidationError(
                    {"linked_habit": "Приятная привычка не должна иметь связанную привычку."}
                )

        return data
