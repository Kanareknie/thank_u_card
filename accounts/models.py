from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#https://testdriven.io/blog/django-custom-user-model/

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # Ensure email is saved in lowercase
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email