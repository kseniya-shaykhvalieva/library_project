from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Author, Book, BookLoan
from .paginations import CustomPagination
from .serializers import AuthorSerializer, BookLoanSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели автора. Чтение доступно авторизованным, изменение — только админам."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['name']  # фильтрует по имени автора
    search_fields = ['name']  # поиск по имени автора
    ordering_fields = ['name', 'birth_date']  # сортировка по имени и дате рождения

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()


class BookViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели книги. Чтение доступно авторизованным, изменение — только админам."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['genre', 'author']  # фильтрует по жанру и автору
    search_fields = ['title', 'author__name']  # поиск по названию книги и имени автора
    ordering_fields = ['title', 'author__name', 'genre']  # сортировка по названию, автору, жанру

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()


class BookLoanViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели выдачи книг.
    Чтение — авторизованным, изменение — админам, владелец проверяется при работе с объектом."""

    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['status', 'user']  # фильтрует по статусу выдачи и пользователю
    search_fields = ['book__title', 'user__email']  # поиск по названию книги и email пользователя
    ordering_fields = ['borrowed_at', 'returned_at', 'status']  # сортировка по дате выдачи, возврата, статусу

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        book.available_copies -= 1
        book.save()
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if serializer.validated_data.get('returned_at') and instance.status != 'returned':
            serializer.validated_data['status'] = 'returned'
            instance.book.available_copies += 1
            instance.book.save()
        serializer.save()
