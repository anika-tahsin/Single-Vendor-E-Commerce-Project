from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("account/", views.user_account, name="account"),
    path("verify/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("reset-password/", views.reset_password, name="reset-password"),
    path("confirm-password-reset/<uidb64>/<token>/", views.confirm_password_reset, name="confirm-password-reset"),
    path("change-password/", views.change_password, name="change-password"),
]
    
