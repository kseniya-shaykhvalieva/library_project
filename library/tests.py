from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Author, Book, BookLoan
from django.utils import timezone


class AuthorTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email='admin@test.ru', password='testpass')
        self.client.force_authenticate(user=self.admin)
        self.author = Author.objects.create(name='Толстой', birth_date='1828-09-09')

    def test_create_author(self):
        url = reverse('library:authors-list')
        data = {'name': 'Достоевский', 'birth_date': '1821-11-11'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_author_update(self):
        url = reverse('library:authors-detail', args=[self.author.pk])
        data = {'name': 'Лев Толстой'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Лев Толстой')

    def test_author_delete(self):
        url = reverse('library:authors-detail', args=[self.author.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_author_list(self):
        url = reverse('library:authors-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.author.pk,
                    "name": self.author.name,
                    "birth_date": self.author.birth_date,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class BookTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email='admin@test.ru', password='testpass')
        self.client.force_authenticate(user=self.admin)
        self.author = Author.objects.create(name='Достоевский')
        self.book = Book.objects.create(
            title='Идиот',
            author=self.author,
            genre='Роман',
            total_copies=5,
            available_copies=5
        )

    def test_create_book(self):
        url = reverse('library:books-list')
        data = {'title': 'Братья Карамазовы', 'author': self.author.pk, 'genre': 'Роман', 'total_copies': 3, 'available_copies': 3}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_update(self):
        url = reverse('library:books-detail', args=[self.book.pk])
        data = {'title': 'Преступление и наказание'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Преступление и наказание')

    def test_book_delete(self):
        url = reverse('library:books-detail', args=[self.book.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_book_list(self):
        url = reverse('library:books-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.book.pk,
                    "title": self.book.title,
                    "author": self.author.pk,
                    "genre": self.book.genre,
                    "description": None,
                    "total_copies": self.book.total_copies,
                    "available_copies": self.book.available_copies,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class BookLoanTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.ru', password='testpass')
        self.admin = User.objects.create_superuser(email='admin@test.ru', password='testpass')
        self.client.force_authenticate(user=self.admin)
        self.author = Author.objects.create(name='Пушкин')
        self.book = Book.objects.create(title='Евгений Онегин', author=self.author, genre='Роман', total_copies=3, available_copies=3)

    def test_create_loan(self):
        url = reverse('library:loans-list')
        data = {'book': self.book.pk, 'user': self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookLoan.objects.count(), 1)
        self.assertEqual(response.json().get('book_available_copies'), 2)

    def test_return_book(self):
        loan = BookLoan.objects.create(book=self.book, user=self.user)
        url = reverse('library:loans-detail', args=[loan.pk])
        data = {'returned_at': '2026-07-19T12:00:00Z'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'returned')

    def test_loan_update(self):
        loan = BookLoan.objects.create(book=self.book, user=self.user)
        url = reverse('library:loans-detail', args=[loan.pk])
        data = {'returned_at': '2026-07-20T12:00:00Z'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['returned_at'], '2026-07-20T15:00:00+03:00')

    def test_loan_delete(self):
        loan = BookLoan.objects.create(book=self.book, user=self.user)
        url = reverse('library:loans-detail', args=[loan.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookLoan.objects.count(), 0)

    def test_loan_list(self):
        loan = BookLoan.objects.create(book=self.book, user=self.user)
        url = reverse('library:loans-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": loan.pk,
                    "book": self.book.pk,
                    "user": self.user.pk,
                    "borrowed_at": loan.borrowed_at.astimezone(timezone.get_fixed_timezone(180)).strftime("%Y-%m-%dT%H:%M:%S.%f+03:00"),
                    "returned_at": loan.returned_at,
                    "status": loan.status,
                    "book_available_copies": 3,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
