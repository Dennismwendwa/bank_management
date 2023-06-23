from django.urls import path
from . import views
from .views import reset_password_request_view, CustomPasswordResetConfirmView

urlpatterns = [
	path("register/", views.register, name="register"),
        path("login/", views.login, name="login"),
	path("logout", views.logout, name="logout"),
	path("reset-password/confirm/<str:uidb64>/<str:token>/", 
			CustomPasswordResetConfirmView.as_view(), 
			name="password_reset_confirm"),
	path("forgot-password", views.reset_password_request_view, name="forgot_password"),
	path("confirm_password_reset", views.password_confirm_request, name="password_confirm_request"),
	path("userprofile", views.userprofile, name="userprofile"),
	path("changepassword", views.changepassword, name="changepassword"),

	path("contact-us", views.contact_us, name="contact_us"),
]
