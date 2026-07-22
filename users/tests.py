from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from users.models import User


class UserTest(APITestCase):
    def setUp(self):
        """Заготовка для тестов пользователя"""
        self.user = User.objects.create_user(email='user@test.ru', password='testpass')
        self.admin = User.objects.create_superuser(email='admin@test.ru', password='testpass')

    def test_user_registration(self):
        """Регистрация пользователя"""
        url = reverse('users:register')
        data = {'email': 'newuser@test.ru', 'password': 'newpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_user_list_admin(self):
        """Список пользователей доступен только админу"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('users:user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_unauthorized(self):
        """Неавторизованный не видит список пользователей"""
        url = reverse('users:user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
