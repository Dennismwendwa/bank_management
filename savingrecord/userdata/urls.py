from django.urls import path
from .import views

app_name = "userdata"

urlpatterns = [
        path("edit_user_data/<int:user_id>", views.edit_user_data, name="edit_user_data"),
        path("admin_deposit", views.admin_deposit_simba, name="admin_deposit_simba"),
        path("admin_withdraw", views.admin_widthdraw, name="admin_widthdraw"),
        ]

