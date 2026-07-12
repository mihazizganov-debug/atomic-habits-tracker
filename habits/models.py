from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )
    time = models.TimeField(
        verbose_name='Время выполнения'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        help_text='Может быть только приятная привычка'
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность (в днях)',
        help_text='Не реже 1 раза в 7 дней'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name='Время на выполнение (в секундах)',
        help_text='Не более 120 секунд'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} - {self.user.username}"

    def clean(self):
        """Валидация модели"""
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя указывать одновременно вознаграждение и связанную привычку"
            )

        if self.duration > 120:
            raise ValidationError(
                "Время выполнения не должно превышать 120 секунд"
            )

        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )

        if self.periodicity > 7:
            raise ValidationError(
                "Привычку необходимо выполнять хотя бы раз в 7 дней"
            )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                "Связанная привычка должна быть приятной"
            )