from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Habit
from users.models import User


class HabitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        # Создаем связанную привычку
        linked_habit = Habit.objects.create(
            owner=self.user,
            place='Pool',
            time='08:00',
            action='Swim',
            is_pleasure=True,
            periodicity=7,
            reward='Healthy',
            time_spent_minutes=60,
            is_public=True,
        )
        # Создаем данные для новой привычки, которую будем тестировать
        self.habit_data = {
            'place': 'Gym',
            'time': '07:00',
            'action': 'Workout',
            'is_pleasure': False ,
            'linked_habit': linked_habit.id,
            'periodicity': 7,
            'reward': 'Good health',
            'time_spent_minutes': 30,
            'is_public': True,
        }

    def test_create_habit_success(self):
        print("Отправляемые данные:", self.habit_data)
        response = self.client.post('/habits/', self.habit_data, format='json')
        print("Статус ответа:", response.status_code)
        print("Ответные данные:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_create_habit_with_linked_non_pleasure(self):
        # Создаем другую привычку, чтобы связывать
        linked_habit_2 = Habit.objects.create(
            owner=self.user,
            place='Park',
            time='08:00',
            action='Jogging',
            is_pleasure=False,
            periodicity=7,
            reward='Enjoyment',
            time_spent_minutes=20,
            is_public=True,
        )
        data = self.habit_data.copy()
        data['linked_habit'] = linked_habit_2.id
        print("Отправляемые данные:", data)
        response = self.client.post('/habits/', data, format='json')
        print("Статус ответа:", response.status_code)
        print("Ответные данные:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "В связанной привычке должна быть признак 'приятной привычки'.",
            response.data['linked_habit'][0]
        )

    def test_create_habit_with_pleasure_and_reward(self):
        data = self.habit_data.copy()
        data['is_pleasure'] = True
        print("Отправляемые данные:", data)
        response = self.client.post('/habits/', data, format='json')
        print("Статус ответа:", response.status_code)
        print("Ответные данные:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_habits_list(self):
        data = self.habit_data.copy()
        response = self.client.get('/habits/',  data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)


    def test_filter_public_habits_only(self):
        # Создаем привычки с разными значениями is_public
        Habit.objects.create(
            owner=self.user,
            place='Public Place',
            time='10:00',
            action='Read',
            is_public=True,
            time_spent_minutes=3
        )
        Habit.objects.create(
            owner=self.user,
            place='Private Place',
            time='12:00',
            action='Meditate',
            is_public=False,
            time_spent_minutes=3
        )

        # Запрос с фильтром is_public=true
        response = self.client.get('/habits/', {'is_public': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Запрос для непубличных
        response = self.client.get('/habits/', {'is_public': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_custom_validators_time(self):
        data = self.habit_data.copy()
        data['time_spent_minutes'] = 200  # превышение
        response = self.client.post('/habits/', data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Время не должно превышать 2 минут', str(response.data))

    def test_periodicity_validator(self):
        data = self.habit_data.copy()
        data['periodicity'] = 8
        response = self.client.post('/habits/', data)
        errors = response.data['periodicity']
        self.assertIn('"8" is not a valid choice.', errors)


class HabitPermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='Петя', email='user1@example.com', password='pass1')
        self.user2 = User.objects.create_user(username='Анна', email='user2@example.com', password='pass2')

        # Создаем привычку для user1
        self.habit = Habit.objects.create(
            owner=self.user1,
            place='Place1',
            time='10:00',
            action='Action1',
            is_public=True,
            time_spent_minutes=30,
            periodicity=3,
            is_pleasure=False
        )

    def login_as_user(self, email):
        self.client.force_authenticate(user=User.objects.get(email=email))

    def test_owner_can_edit(self):
        self.login_as_user(self.user1)
        url = f'/habits/{self.habit.id}/'
        data = {
            'place': 'Новое место',
            'time': '11:00',
            'action': 'Обновленное действие',
            'is_public': False,
            'time_spent_minutes': 45,
            'periodicity': 3,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_edit(self):
        self.login_as_user(self.user2)
        url = f'/habits/{self.habit.id}/'
        data = {'place': 'Попытка редактировать'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete(self):
        self.login_as_user(self.user1)
        url = f'/habits/{self.habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_owner_cannot_delete(self):
        self.login_as_user(self.user2)
        url = f'/habits/{self.habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
