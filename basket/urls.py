from django.urls import path
from . import views

urlpatterns = [
    path("", views.basket_view, name="basket"),
]
