from django.urls import path
from app_auth.views import RegisterView, LoginView, UserAccountView, ChangePasswordView, PasswordResetConfirmView, PasswordResetRequestView, VerifyEmailView,cron_job
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns=[
    path("register/", RegisterView.as_view(),name="register"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("account/", UserAccountView.as_view(), name="account"),
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
    path("password/reset/request/", PasswordResetRequestView.as_view(), name="reset-password-request"),
    path("password/reset/confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("cron-job/",cron_job,name="cron-job"),
]