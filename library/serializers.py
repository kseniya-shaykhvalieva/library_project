from rest_framework import serializers

from .models import Author, Book, BookLoan
from .validations import AvailableCopiesValidator, ReturnDateValidator, UniqueBookValidator


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate(self, data):
        validator = UniqueBookValidator('title', 'author')
        validator(data, instance=self.instance)
        return data


class BookLoanSerializer(serializers.ModelSerializer):
    book_available_copies = serializers.IntegerField(source='book.available_copies', read_only=True)

    class Meta:
        model = BookLoan
        fields = "__all__"
        validators = [ReturnDateValidator("borrowed_at", "returned_at"), AvailableCopiesValidator("book")]
