from django.urls import path
from . import views
from .views import CustomPasswordResetConfirmView #import for class bassed views

urlpatterns = [
    #path("", views.home, name="home"),
#	path("", views.register, name="register"),
	path("register/", views.register, name="register"),
        path("login", views.login, name="login"),
	path("logout", views.logout, name="logout"),
	path("forgot-password", views.forgot_password, name="forgot_password"),
	path("reset/<uidb64>/<token>", CustomPasswordResetConfirmView.as_view(),
			name="password_reset_confirm"),
            
	path("userprofile", views.userprofile, name="userprofile"),
]
