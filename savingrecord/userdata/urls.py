from django.urls import path
from .import views

app_name = "userdata"

urlpatterns = [
        path("edit_user_data/<int:user_id>", views.edit_user_data, name="edit_user_data"),
        ]

