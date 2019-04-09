from django.urls import path
from . import views

urlpatterns = [
    path("", views.receipt_generator_index, name="receipt_generator_index"),
    path("donor/add", views.add_donor, name="add_donor")
    ]