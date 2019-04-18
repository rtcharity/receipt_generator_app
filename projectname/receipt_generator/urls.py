from django.urls import path
from . import views

app_name = 'receipt_generator'
urlpatterns = [
    path("", views.receipt_generator_index, name="receipt_generator_index"),
    path("donor/add", views.add_donor, name="add_donor"),
    path("donor/<int:pk>/edit", views.edit_donor, name="edit_donor"),
    path("donation/add", views.add_donation, name="add_donation"),
    path("donation/<int:pk>/edit", views.edit_donation, name="edit_donation"),
    path("receipt/<int:pk>", views.view_receipt, name="view_receipt"),
    path("donor", views.list_donors, name="list_donors"),
    path("donor/<int:pk>", views.view_donor, name="view_donor"),
    path("donation/<int:pk>", views.view_donation, name="view_donation"),
    path("donation/<int:pk>/receipt/add", views.add_receipt, name="add_receipt")
    ]