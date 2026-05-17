from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cards.models import Card
from .forms import CardForm


@login_required
def home(request):
    if request.method == "POST":
        form = CardForm(request.POST)

        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()

            messages.success(request, "Your card has been saved successfully.")
            return redirect("home")
    else:
        form = CardForm()

    latest_card = Card.objects.filter(user=request.user).order_by("-created_on").first()

    return render(
        request,
        "cards/home.html",
        {
            "form": form,
            "latest_card": latest_card,
        },
    )
