from django.shortcuts import redirect, render
from accounts.forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
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