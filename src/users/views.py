import jwt
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.utils.encoding import smart_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    RegisterSerializer,
    EmailVerifySerializer,
    LoginSerializer,
    RequestResetPasswordEmailSerializer,
    SetNewPasswordSerializer,
    CheckDigitsSerializer,
)
from .services import UserService


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        UserService.send_mail_register(user=user, request=request)
        return Response(
            {
                "user": user_data,
                "message": "We have sent you link to activate your email",
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    serializer_class = EmailVerifySerializer
    template_name = "email.html"
    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return render(request, "email.html")
        except jwt.ExpiredSignatureError as error:
            return render(request, "linkexpired.html")
        except jwt.exceptions.DecodeError as error:
            return render(request, "invalidtoken.html")


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestResetPasswordEmailView(generics.GenericAPIView):
    serializer_class = RequestResetPasswordEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email", "")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            UserService.send_mail_reset_password(user=user, request=request)
            return Response(
                {
                    "success": "We have sent you message to reset your password",
                    "uidb64": uidb64,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Enter valid or existing email"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CheckDigitsView(generics.GenericAPIView):
    serializer_class = CheckDigitsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data.get("uidb64")
        check_digits = serializer.validated_data.get("digits")
        id = force_str(urlsafe_base64_decode(uidb64))
        send_digits = UserService.send_digits(id)
        if check_digits == send_digits:
            return Response({"message": "correct"}, status=status.HTTP_200_OK)
        return Response({"message": "incorrect"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password reset success"},
            status=status.HTTP_200_OK,
        )


class GoogleLogin(APIView):
    def post(self, request):
        data = UserService.get_user_info_from_google(request.data.get("token"))
        if "error" in data:
            return Response(
                data={"message": data.get("error").get("message")},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=data["email"],
                email=data["email"],
                is_verified=True,
                password=make_password(BaseUserManager().make_random_password()),
            )
            user.save()
        return Response(
            data=UserService.jwt_tokens_for_user(user), status=status.HTTP_201_CREATED
        )
