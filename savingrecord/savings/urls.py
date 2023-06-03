from django.urls import path
from . import views

urlpatterns = [
	path("saving", views.savings, name="savings"),  
]
