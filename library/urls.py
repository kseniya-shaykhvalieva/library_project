from rest_framework.routers import DefaultRouter

from library.apps import LibraryConfig
from library.views import AuthorViewSet, BookViewSet, BookLoanViewSet

app_name = LibraryConfig.name

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"books", BookViewSet, basename="books")
router.register(r"loans", BookLoanViewSet, basename="loans")

urlpatterns = []

urlpatterns += router.urls
