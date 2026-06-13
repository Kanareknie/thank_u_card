from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import BasketItem

# Price per card in pence (199p = £1.99)
CARD_PRICE_PENCE = 199


# View to display the user's basket
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

    basket_count = basket_items.count()
    basket_total_pence = basket_count * CARD_PRICE_PENCE
    basket_total = basket_total_pence / 100

    return render(
        request,
        "basket/basket.html",
        {
            "basket_items": basket_items,
            "basket_count": basket_count,
            "basket_total": basket_total,
        }
    )


# View to handle removing an item from the basket
@login_required
def remove_basket_item(request, item_id):
    basket_item = get_object_or_404(
        BasketItem,
        id=item_id,
        basket__user=request.user
    )

    if request.method == "POST":
        basket_item.delete()
        messages.success(
            request,
            "The card has been removed from your basket."
            )

    return redirect("basket")


# View to preview a card in the basket
@login_required
def basket_item_preview(request, item_id):
    basket_item = get_object_or_404(
        BasketItem,
        id=item_id,
        basket__user=request.user
    )

    return render(
        request,
        "basket/preview.html",
        {
            "basket_item": basket_item,
            "card": basket_item.card,
        }
    )
