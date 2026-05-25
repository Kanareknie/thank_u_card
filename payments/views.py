import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from basket.models import BasketItem
from cards.models import Card


CARD_PRICE_PENCE = 199


@login_required
def create_checkout_session(request):
    if request.method != "POST":
        return redirect("basket")

    basket_items = BasketItem.objects.filter(
        basket__user=request.user
    ).select_related("card")

    if not basket_items.exists():
        messages.error(request, "Your basket is empty.")
        return redirect("basket")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = []
    card_ids = []

    for item in basket_items:
        card_ids.append(str(item.card.id))

        line_items.append(
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": f"Thank U Card #{item.card.id}",
                    },
                    "unit_amount": CARD_PRICE_PENCE,
                },
                "quantity": 1,
            }
        )

    success_url = request.build_absolute_uri(
        reverse("payment_success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"

    cancel_url = request.build_absolute_uri(
        reverse("payment_cancel")
    )

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "user_id": str(request.user.id),
            "card_ids": ",".join(card_ids),
        },
    )

    return redirect(checkout_session.url, code=303)


@login_required
def payment_success(request):
    messages.success(
        request,
        "Payment received. Your card will be available in your account shortly."
    )
    return redirect("account")


@login_required
def payment_cancel(request):
    messages.info(request, "Payment cancelled. Your basket is still available.")
    return redirect("basket")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = session.get("metadata", {}).get("user_id")
        card_ids = session.get("metadata", {}).get("card_ids", "")

        if user_id and card_ids:
            card_id_list = [
                int(card_id)
                for card_id in card_ids.split(",")
                if card_id
            ]

            cards = Card.objects.filter(
                id__in=card_id_list,
                user_id=user_id,
                is_paid=False,
            )

            for card in cards:
                card.is_paid = True
                card.save()

            BasketItem.objects.filter(
                basket__user_id=user_id,
                card_id__in=card_id_list,
            ).delete()

    return HttpResponse(status=200)