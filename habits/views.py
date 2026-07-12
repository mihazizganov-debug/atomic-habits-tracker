from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from .models import Habit
from .serializers import HabitSerializer


class HabitPagination(LimitOffsetPagination):
    """Пагинация для привычек"""
    default_limit = 5
    max_limit = 20


class HabitListCreateView(generics.ListCreateAPIView):
    """Список привычек пользователя и создание новой"""
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращаем только привычки текущего пользователя"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании привязываем привычку к текущему пользователю"""
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, редактирование и удаление привычки"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Пользователь может редактировать только свои привычки"""
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек (доступен всем)"""
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Только публичные привычки"""
        return Habit.objects.filter(is_public=True)