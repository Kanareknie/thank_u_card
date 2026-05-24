from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import BasketItem


@login_required
def basket_view(request):
    basket_items = BasketItem.objects.filter(
        basket__user=request.user
    ).select_related(
        "card",
        "card__recipient_type",
        "card__theme",
        "card__colour",
        "card__element",
    ).order_by("-added_on")

    return render(
        request,
        "basket/basket.html",
        {
            "basket_items": basket_items,
        }
    )