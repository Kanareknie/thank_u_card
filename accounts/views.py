from django.shortcuts import redirect, render
from accounts.forms import SignUpForm
from django.contrib.auth import login

# Create your views here.
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = SignUpForm()
        
    return render(request, 'accounts/register.html', {"form": form})
