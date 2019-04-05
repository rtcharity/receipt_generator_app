from django.urls import path
from . import views

urlpatterns = [
    path("", views.receipt_generator_index, name="project_index"),
    ]