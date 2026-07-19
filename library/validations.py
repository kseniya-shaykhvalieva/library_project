from rest_framework.serializers import ValidationError

from .models import Book


class ReturnDateValidator:
    """Проверяет, что дата возврата позже даты выдачи"""

    def __init__(self, field_borrowed, field_returned):
        self.field_borrowed = field_borrowed
        self.field_returned = field_returned

    def __call__(self, data):
        borrowed = data.get(self.field_borrowed)
        returned = data.get(self.field_returned)
        if returned and borrowed and returned < borrowed:
            raise ValidationError("Дата возврата не может быть раньше даты выдачи.")


class UniqueBookValidator:
    """Проверяет уникальность книги"""

    def __init__(self, title_field, author_field):
        self.title_field = title_field
        self.author_field = author_field

    def __call__(self, data, instance=None):
        title = data.get(self.title_field)
        author = data.get(self.author_field)
        if Book.objects.filter(title=title, author=author).exclude(pk=instance.pk if instance else None).exists():
            raise ValidationError("Книга с таким названием и автором уже существует.")


class AvailableCopiesValidator:
    """Проверяет доступные экземпляры книг для выдачи"""

    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        book = data.get("book")
        if book and book.available_copies <= 0:
            raise ValidationError("Нет доступных экземпляров книги.")
