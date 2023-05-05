from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views
from .views import GoogleLogin

urlpatterns = [
    path("email-verify/", views.VerifyEmailView.as_view(), name="email-verify"),
    path("google/", GoogleLogin.as_view(), name="google"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("check-digits/", views.CheckDigitsView.as_view(), name="check-digits"),
    path(
        "request-reset-email/",
        views.RequestResetPasswordEmailView.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset-complete/",
        views.SetNewPasswordView.as_view(),
        name="password-reset-complete",
    ),
]
