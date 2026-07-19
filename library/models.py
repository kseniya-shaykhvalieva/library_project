from django.db import models

from config.settings import AUTH_USER_MODEL


class Author(models.Model):
    """Автор"""

    name = models.CharField(max_length=255, unique=True, verbose_name="Имя автора")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class Book(models.Model):
    """Книга"""

    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    total_copies = models.PositiveIntegerField(default=1, verbose_name="Всего экземпляров")
    available_copies = models.PositiveIntegerField(default=1, verbose_name="Доступно экземпляров")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class BookLoan(models.Model):
    """Выдача книг"""

    ACTIVE = "active"
    RETURNED = "returned"

    STATUS_CHOICES = [
        (ACTIVE, "Активна"),
        (RETURNED, "Возвращена"),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    borrowed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    returned_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата возврата")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Статус")

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"

    def __str__(self):
        return f"{self.book.title} - {self.user.email}"
