from django.shortcuts import redirect, render
from accounts.forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from cards.models import Card
from basket.models import Basket, BasketItem


# This view is for the user registration page. 
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "Account created successfully. You are now logged in.")
            return redirect("home")
    else:
        form = SignUpForm()
        
    return render(request, 'accounts/register.html', {"form": form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Logged in successfully.")
        return super().form_valid(form)
    

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have logged out successfully.")
        return super().dispatch(request, *args, **kwargs)
    
    
# This view is for the user account page, 
# where they can see their cards that are ready to download and their saved cards.
@login_required
def account_view(request):
    ready_to_download = Card.objects.filter(
        user=request.user,
        is_paid=True,
        pdf_file__isnull=False,
    ).order_by("-created_on")

    saved_cards = Card.objects.filter(
        user=request.user,
        is_paid=False,
    ).order_by("-created_on")

    return render(
        request,
        "accounts/account.html",
        {
            "ready_to_download": ready_to_download,
            "saved_cards": saved_cards,
        },
    )
    
    
# This view allows the user to preview a saved card before downloading or adding it to the basket.
@login_required
def account_card_preview(request, card_id):
    card = get_object_or_404(
        Card,
        id=card_id,
        user=request.user,
    )

    return render(
        request,
        "accounts/account_preview.html",
        {
            "card": card,
        }
    )

# This view allows the user to add a saved card to their basket for checkout.
@login_required
def add_saved_card_to_basket(request, card_id):
    card = get_object_or_404(
        Card,
        id=card_id,
        user=request.user,
        is_paid=False,
    )

    if request.method == "POST":
        basket, created = Basket.objects.get_or_create(
            user=request.user
        )

        BasketItem.objects.get_or_create(
            basket=basket,
            card=card
        )

        messages.success(request, "Your saved card has been added to the basket.")

    return redirect("account")

# This view allows the user to delete a saved card that has not been paid for yet.
@login_required
def delete_saved_card(request, card_id):
    card = get_object_or_404(
        Card,
        id=card_id,
        user=request.user,
        is_paid=False,
    )

    if request.method == "POST":
        card.delete()
        messages.success(request, "Your saved card has been deleted.")

    return redirect("account")