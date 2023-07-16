from django.urls import path
from .import views

app_name = "userdata"

urlpatterns = [
        path('forbidden/', views.forbidden_view, name='forbidden'),
        path("edit_user_data/<int:user_id>", views.edit_user_data, name="edit_user_data"),
        path("admin_deposit", views.admin_deposit_simba, name="admin_deposit_simba"),
        path("admin_withdraw", views.admin_widthdraw, name="admin_widthdraw"),
        path("approve_business_number", views.business_number_approval,
            name="business_number_approval"),
        path("approve_till_number", views.till_number_approval,
            name="till_number_approval"),

        ]

