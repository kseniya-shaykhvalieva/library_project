from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserDestroyAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="refresh",
    ),
    path("user_list/", UserListAPIView.as_view(), name="user_list"),
    path("user_detail/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("user_update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("user_delete/", UserDestroyAPIView.as_view(), name="user_delete"),
]
