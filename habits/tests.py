from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import time
from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(8, 0),
            action='Morning exercise',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=True
        )

    def test_habit_creation(self):
        """Тест создания привычки"""
        self.assertEqual(self.habit.action, 'Morning exercise')
        self.assertEqual(self.habit.place, 'Home')
        self.assertEqual(self.habit.duration, 60)
        self.assertTrue(self.habit.is_public)

    def test_habit_str(self):
        """Тест строкового представления"""
        expected = f"Morning exercise - testuser"
        self.assertEqual(str(self.habit), expected)

    def test_habit_validators(self):
        """Тест валидаторов"""
        # Проверка duration > 120
        habit = Habit(
            user=self.user,
            place='Home',
            time=time(8, 0),
            action='Test',
            duration=130,
            periodicity=1
        )
        with self.assertRaises(Exception):
            habit.full_clean()

        # Проверка periodicity > 7
        habit = Habit(
            user=self.user,
            place='Home',
            time=time(8, 0),
            action='Test',
            duration=60,
            periodicity=10
        )
        with self.assertRaises(Exception):
            habit.full_clean()


class HabitAPITest(TestCase):
    """Тесты для API Habit"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(8, 0),
            action='Morning exercise',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=True
        )

    def test_get_habits_without_token(self):
        """Тест доступа без токена"""
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_with_token(self):
        """Тест создания привычки с токеном"""
        # Получаем токен
        response = self.client.post('/api/users/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        token = response.data['access']

        # Создаём привычку
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/habits/', {
            'place': 'Office',
            'time': '09:00:00',
            'action': 'Workout',
            'is_pleasant': False,
            'periodicity': 1,
            'duration': 45,
            'is_public': False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Workout')

    def test_get_public_habits(self):
        """Тест получения публичных привычек"""
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)