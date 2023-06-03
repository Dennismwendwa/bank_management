from django.urls import path
from . import views
from .views import PasswordResetCornfirmViewCustom #import for class bassed views

urlpatterns = [
	path("", views.register, name="register"),
    	path("login", views.login, name="login"),
	path("logout", views.logout, name="logout"),
	path("forgot-password", views.forgot_password, name="forgot_password"),
	path("reset/<uidb64>/<token>", PasswordResetCornfirmViewCustom.as_view(),
			name="password_reset_confirm"),
]
