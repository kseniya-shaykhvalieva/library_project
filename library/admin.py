from django.contrib import admin

from .models import Author, Book, BookLoan


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_filter = ("id",)
    search_fields = ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "total_copies",
        "available_copies",
    )
    list_filter = ("author",)
    search_fields = ("title", "author",)

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "user",
        "status",
        "borrowed_at",
        "returned_at"
    )
    list_filter = ("id",)
    search_fields = ("book", "user", "status")
