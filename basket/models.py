from django.db import models
from django.conf import settings
from cards.models import Card

# Create your models here.
# The Basket model represents a user's shopping basket, which can contain multiple items (cards).
class Basket(models.Model):
    user = models.OneToOneField(
        # Use the custom user model defined in settings.AUTH_USER_MODEL
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="basket"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s basket"


class BasketItem(models.Model):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name="items"
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="basket_items"
    )
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card {self.card.id} in basket"
    