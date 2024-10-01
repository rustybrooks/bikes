from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User  # type: ignore
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, serializers, status, viewsets  # type: ignore
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # type: ignore

from bikes import models  # type: ignore


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude: list[str] = [
            "password",
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
        ]


class SignupUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        password2 = data["password2"]

        if not username or not password:
            raise ValidationError("Username and password required")

        if password != password2:
            raise ValidationError({"password": "Passwords don't match"})

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        return data


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginUserSerializer, responses={200: UserSerializer}
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        user = authenticate(
            request,
            username=request.data["username"],
            password=request.data["password"],
        )
        if user is None:
            raise PermissionDenied()

        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=SignupUserSerializer, responses={200: UserSerializer}
    )
    @action(detail=False, methods=["post"])
    def signup(self, request):
        serializer = SignupUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            serializer2 = UserSerializer(user)
            return Response(serializer2.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
