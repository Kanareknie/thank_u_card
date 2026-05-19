from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cards.models import Card
from .forms import CardForm
from .tasks import generate_background_task
from .openai_helpers import generate_card_message

@login_required
def home(request):
    generated_message = None
    preview_card = None

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
            if form.is_valid():
                card = form.save(commit=False)
                card.user = request.user
                card.save()
                # Display a success message to the user indicating that the card has been saved successfully
                messages.success(request, "Your card has been saved successfully.")
                return redirect("home")
            
        # Generate a background image for the card using AI and save it to the card's background_image field
        elif action == "generate_background":
            if form.is_valid():
                card = form.save(commit=False)
                card.user = request.user
                card.save()

                # Call the Celery task to generate the background image asynchronously, 
                # passing the card's ID as an argument
                generate_background_task.delay(card.id)

                messages.success(
                    request,
                    "Background generation started. Please refresh the page in a moment."
                )
                return redirect("home")
            else:
                messages.error(
                    request,
                    "Please choose the card options before generating a background."
                )
        
    # If the request method is GET, initialize an empty form for the user to fill out
    else:
        form = CardForm()
    # Retrieve the latest card created by the user to display on the home page
    latest_card = Card.objects.filter(user=request.user).order_by("-created_on").first()
    # Render the home page template with the form, latest card, generated message, and preview card data
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