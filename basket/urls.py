from django.urls import path
from . import views

urlpatterns = [
    path("", views.basket_view, name="basket"),
    path("remove/<int:item_id>/",
         views.remove_basket_item,
         name="remove_basket_item"),
    path("preview/<int:item_id>/",
         views.basket_item_preview,
         name="basket_item_preview"),
]
