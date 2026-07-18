from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.permissions import IsOwner
from .models import Author, Book, BookLoan
from .serializers import AuthorSerializer, BookSerializer, BookLoanSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели автора. Чтение доступно авторизованным, изменение — только админам."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated]
        elif self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser]
        return super().get_permissions()


class BookViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели книги. Чтение доступно авторизованным, изменение — только админам."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated]
        elif self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser]
        return super().get_permissions()


class BookLoanViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели выдачи книг.
    Чтение — авторизованным, изменение — админам, владелец проверяется при работе с объектом."""

    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated]
        elif self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser]
        return super().get_permissions()
