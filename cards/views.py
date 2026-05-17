from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cards.models import Card
from .forms import CardForm

from .openai_helpers import generate_card_message

@login_required
def home(request):
    generated_message = None

    if request.method == "POST":
        form = CardForm(request.POST)
        action = request.POST.get("action")

        if action == "generate_message":
            if form.is_valid():
                generated_message = generate_card_message(
                    recipient_type=form.cleaned_data["recipient_type"],
                    theme=form.cleaned_data["theme"],
                    message=form.cleaned_data.get("message", ""),
                )

                if generated_message:
                    form = CardForm(
                        initial={
                            "recipient_type": form.cleaned_data["recipient_type"],
                            "theme": form.cleaned_data["theme"],
                            "colour": form.cleaned_data["colour"],
                            "element": form.cleaned_data["element"],
                            "recipient_name": form.cleaned_data.get("recipient_name", ""),
                            "message": generated_message,
                            "no_message": form.cleaned_data.get("no_message", False),
                        }
                    )
                    messages.success(request, "Message generated successfully.")
                else:
                    messages.error(request, "AI message generation is currently unavailable.")

        elif action == "save_card":
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
            "generated_message": generated_message,
        },
    )