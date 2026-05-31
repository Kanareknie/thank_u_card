from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from cards.models import Card
from .forms import CardForm
from basket.models import Basket, BasketItem
from .tasks import generate_background_task
from .openai_helpers import generate_card_message

from django.shortcuts import get_object_or_404



def home(request):
    generated_message = None
    preview_card = None
    # Check if the reset query parameter is set to "1" to determine if the form and preview should be reset
    reset_page = request.GET.get("reset") == "1"
    
    latest_card = None
    
    # Display on the preview only if the user is authenticated and has a card that has
    # a generated background image that is not paid for
    if request.user.is_authenticated:
        latest_card = Card.objects.filter(
            user=request.user, is_paid=False,
            background_status="completed",
            background_image__isnull=False,
        ).order_by("-created_on").first()

    # Handle form submissions for generating messages, 
    # updating preview, and saving cards
    if request.method == "POST":
        form = CardForm(request.POST)
        action = request.POST.get("action")

        # Determine which button was clicked and handle accordingly
        if action == "generate_message":
            if form.is_valid():
                generated_message = generate_card_message(
                    recipient_type=form.cleaned_data["recipient_type"],
                    theme=form.cleaned_data["theme"],
                    message=form.cleaned_data.get("message", ""),
                )
                
                # If a message was generated, update the form and preview card with the new message
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
                    
                    # Update the preview card with the generated message and other form data
                    preview_card = {
                        "recipient_name": form.initial.get("recipient_name"),
                        "message": generated_message,
                        "recipient_type": form.initial.get("recipient_type"),
                        "theme": form.initial.get("theme"),
                        "colour": form.initial.get("colour"),
                        "element": form.initial.get("element"),
                        "no_message": form.initial.get("no_message"),
                    }
                    
                    # Display a success message to the user
                    messages.success(request, "Message generated successfully.")
                else:
                    # If message generation failed, display an error message to the user
                    messages.error(request, "AI message generation is currently unavailable.")
         
        # Update the preview card with the current form data without generating a new message            
        elif action == "update_preview":
            if form.is_valid():
                preview_card = {
                    "recipient_name": form.cleaned_data.get("recipient_name"),
                    "message": form.cleaned_data.get("message"),
                    "recipient_type": form.cleaned_data.get("recipient_type"),
                    "theme": form.cleaned_data.get("theme"),
                    "colour": form.cleaned_data.get("colour"),
                    "element": form.cleaned_data.get("element"),
                    "no_message": form.cleaned_data.get("no_message"),
                }

                # Display a success message to the user indicating that the preview has been updated
                messages.success(request, "Preview updated.")
        # Save the card to the database with the current form data and generated message
        elif action == "save_card":
            if not request.user.is_authenticated:
                messages.error(
                    request,
                    "Please log in or create an account to save your card."
                )
                return redirect("login")

            if not latest_card or not latest_card.background_image:
                messages.error(
                    request,
                    "Please generate a background before saving your card."
                )
            elif form.is_valid():
                form_card = form.save(commit=False)

                latest_card.recipient_type = form_card.recipient_type
                latest_card.theme = form_card.theme
                latest_card.colour = form_card.colour
                latest_card.element = form_card.element
                latest_card.recipient_name = form_card.recipient_name
                latest_card.message = form_card.message
                latest_card.no_message = form_card.no_message
                latest_card.save()

                messages.success(request, "Your card has been saved successfully.")
                return redirect(f"{reverse('home')}?reset=1")
            
        # Add the card to the user's basket by creating a BasketItem linking the card to the user's Basket
        elif action == "add_to_basket":
            if not request.user.is_authenticated:
                messages.error(
                    request,
                    "Please log in or create an account to add your card to the basket."
                )
                return redirect("login")

            if not latest_card or not latest_card.background_image:
                messages.error(
                    request,
                    "Please generate a background before adding your card to the basket."
                )
            elif form.is_valid():
                form_card = form.save(commit=False)

                latest_card.recipient_type = form_card.recipient_type
                latest_card.theme = form_card.theme
                latest_card.colour = form_card.colour
                latest_card.element = form_card.element
                latest_card.recipient_name = form_card.recipient_name
                latest_card.message = form_card.message
                latest_card.no_message = form_card.no_message
                latest_card.save()

                basket, created = Basket.objects.get_or_create(
                    user=request.user
                )

                BasketItem.objects.get_or_create(
                    basket=basket,
                    card=latest_card
                )

                messages.success(request, "Your card has been added to the basket.")
                return redirect(f"{reverse('home')}?reset=1")
            
        # Generate a background image for the card using AI and save it to the card's background_image field
        # https://docs.djangoproject.com/en/6.0/ref/models/querysets/
        # https://stackoverflow.com/questions/32510123/django-datetime-timedelta-how-does-its-subtract-from-timezone-now-if-they-ar
        elif action == "generate_background":
            if not request.user.is_authenticated:
                messages.error(
                    request,
                "   Please log in or create an account to generate a card background."
                )
                return redirect("login")
            
            
            if form.is_valid():
                twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

                # Count the number of cards with background generation
                # requests made by the user in the last 24 hours
                generated_count = Card.objects.filter(
                    user=request.user,
                    created_on__gte=twenty_four_hours_ago,
                    background_status__in=["generating", "completed", "failed"],
                ).count()

                # If the user has already made 3 or more background generation requests in the last 24 hours, 
                # display an error message and do not allow them to generate 
                # another background until the 24-hour period has
                if generated_count >= 3:
                    messages.error(
                        request,
                        "You can generate only 3 card backgrounds per 24 hours."
                    )
                else:
                    card = form.save(commit=False)
                    card.background_status = "generating"
                    card.user = request.user
                    card.save()

                    # Call the Celery task to generate the background image asynchronously, 
                    # passing the card's ID as an argument
                    generate_background_task.delay(card.id)
                    
                    return redirect("home")
            else:
                messages.error(
                    request,
                    "Please choose the card options before generating a background."
                )
    # If the request method is GET, pre-fill the form with the latest card if it exists
    else:
        if reset_page:
            form = CardForm()
            latest_card = None
        elif latest_card:
            form = CardForm(instance=latest_card)
        else:
            form = CardForm()
            
    return render(
        request,
        "cards/home.html",
        {
            "form": form,
            "latest_card": latest_card,
            "generated_message": generated_message,
            "preview_card": preview_card,
        },
    )
    
# This function edits a saved card by allowing the user to update the card's attributes and message.

@login_required
def edit_card(request, card_id):
    card = get_object_or_404(
        Card,
        id=card_id,
        user=request.user,
        is_paid=False,
    )

    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        action = request.POST.get("action")

        if form.is_valid():
            updated_card = form.save(commit=False)
            updated_card.user = request.user

            if action == "generate_message":
                generated_message = generate_card_message(
                    recipient_type=form.cleaned_data["recipient_type"],
                    theme=form.cleaned_data["theme"],
                    message=form.cleaned_data.get("message", ""),
                )

                if generated_message:
                    updated_card.message = generated_message
                    updated_card.save()
                    messages.success(request, "Message updated successfully.")
                    return redirect("edit_card", card_id=updated_card.id)

                messages.error(request, "AI message generation is currently unavailable.")

            elif action == "generate_background":
                updated_card.background_status = "generating"
                updated_card.save()

                generate_background_task.delay(updated_card.id)

                messages.success(request, "New background generation has started.")
                return redirect("edit_card", card_id=updated_card.id)

            elif action == "save_changes":
                updated_card.save()
                messages.success(request, "Your card has been updated.")
                return redirect("account")

            elif action == "add_to_basket":
                updated_card.save()

                basket, created = Basket.objects.get_or_create(
                    user=request.user
                )

                BasketItem.objects.get_or_create(
                    basket=basket,
                    card=updated_card
                )

                messages.success(request, "Your card has been added to the basket.")
                return redirect("basket")

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CardForm(instance=card)

    return render(
        request,
        "cards/edit_card.html",
        {
            "form": form,
            "card": card,
        },
    )
    