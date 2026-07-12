from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, data):
        """Валидация при создании/обновлении"""
        # Проверяем, что нельзя одновременно указать reward и related_habit
        if data.get("reward") and data.get("related_habit"):
            raise serializers.ValidationError(
                "Нельзя указывать одновременно вознаграждение и связанную привычку"
            )

        # Проверяем время выполнения (не более 120 секунд)
        if data.get("duration", 0) > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд"
            )

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get("is_pleasant"):
            if data.get("reward") or data.get("related_habit"):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )

        # Периодичность не реже 1 раза в 7 дней
        if data.get("periodicity", 1) > 7:
            raise serializers.ValidationError(
                "Привычку необходимо выполнять хотя бы раз в 7 дней"
            )

        return data
