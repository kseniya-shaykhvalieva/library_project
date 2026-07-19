from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.serializers import ValidationError

from library.paginations import CustomPagination
from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    pagination_class = CustomPagination


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | IsAdminUser)

    def perform_destroy(self, instance):
        if instance.bookloan_set.filter(status="active").exists():
            raise ValidationError("Нельзя удалить пользователя с активными выдачами.")
        instance.delete()
