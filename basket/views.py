from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

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
        messages.success(request, "The card has been removed from your basket.")

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