from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth.hashers import check_password

from .models import User
from .serializers import SignUpSerializer, LogInSerializer, UserSerializer


from django.contrib.auth import logout


class AuthViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users perform authentications.
    """

    @swagger_auto_schema(
        operation_description="Sign Up User",
        operation_summary="Sign Up User",
        tags=["Auth"],
        request_body=SignUpSerializer,
    )
    @action(methods=["post"], detail=False)
    def sign_up(self, request):
        """
        Sign up a new user.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop("password")

        user = User.objects.create(**serializer.validated_data)
        user.set_password(password)
        user.save()

        return Response(
            UserSerializer(user).data, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_description="Log In User",
        operation_summary="Log In User",
        tags=["Auth"],
        request_body=LogInSerializer,
    )
    @action(methods=["post"], detail=False)
    def log_in(self, request):
        """
        Log in an existing user.
        """
        serializer = LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_password = check_password(password, user.password)

        if not user_password:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = RefreshToken.for_user(user)
        data = {
            "user": UserSerializer(instance=user).data,
            "token": {
                "refresh": str(token),
                "access": str(token.access_token),
            },
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Log Out User",
        operation_summary="Log Out User",
        tags=["Auth"],
    )
    @action(methods=["post"], detail=False)
    def log_out(self, request):
        logout(request)
        data = {"success": "Sucessfully logged out"}
        return Response(data=data, status=status.HTTP_200_OK)
