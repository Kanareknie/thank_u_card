from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.utils.text import slugify

from cards.models import Card
from .forms import CardForm
from .openai_helpers import generate_card_message, generate_card_background

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
            # Retrieve the card ID from the POST data and get the corresponding card object for the current user
            card_id = request.POST.get("card_id")
            # Use get_object_or_404 to retrieve the card object, ensuring that it belongs to the current user
            # and handling the case where the card does not exist
            card = get_object_or_404(Card, id=card_id, user=request.user)

            # Generate the background image using the generate_card_background function,
            # passing in the card object as an argument
            image_bytes = generate_card_background(card)

            # If the image was generated successfully, save it to the card's background_image field
            # using Django's ContentFile and slugify utilities to create a unique filename based on
            # the card's ID and theme name. Display a success message to the user 
            # if the image was saved successfully, 
            # or an error message if AI image generation is currently unavailable.
            if image_bytes:
                filename = f"card_{card.id}_{slugify(card.theme.name)}.png"
                card.background_image.save(
                    filename,
                    ContentFile(image_bytes),
                    save=True,
                )
                messages.success(request, "Background image generated successfully.")
            else:
                messages.error(request, "AI image generation is currently unavailable.")

            return redirect("home")
        
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