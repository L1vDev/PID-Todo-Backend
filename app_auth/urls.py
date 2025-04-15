from django.urls import path
from app_auth.views import RegisterView, LoginView, UserAccountView, ChangePasswordView, PasswordResetConfirmView, PasswordResetRequestView, VerifyEmailView

urlpatterns=[
    path("register/", RegisterView.as_view(),name="register"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("account/", UserAccountView.as_view(), name="account"),
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
    path("password/reset/request/", PasswordResetRequestView.as_view(), name="reset-password-request"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
]