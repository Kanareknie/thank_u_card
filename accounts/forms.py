from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    # Email validation
    # https://medium.com/@python-javascript-php-html-css/implementing-email-validation-in-django-projects-e210d4777fac
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email:
            email = email.lower()

        blocked_domains = [
            "tempmail.com",
            "mailinator.com",
            "10minutemail.com",
        ]

        domain = email.split("@")[-1]

        if domain in blocked_domains:
            raise forms.ValidationError(
                "Disposable email addresses are not allowed."
            )

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email
