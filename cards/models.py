from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s profile"


class RecipientType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Theme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Colour(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Element(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class Card(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_cards',
        null = False,
        blank = False
    )
    recipient_type = models.ForeignKey(
        RecipientType,
        on_delete=models.CASCADE,
        related_name='recipient_type_cards',
        null = False,
        blank = False
    )
    theme = models.ForeignKey(
        Theme, 
        on_delete=models.CASCADE,
        related_name='theme_cards',
        null = False,
        blank = False
    )
    colour = models.ForeignKey(
        Colour, 
        on_delete=models.CASCADE, 
        related_name='colour_cards',
        null = False,
        blank = False
    )
    element = models.ForeignKey(
        Element, 
        on_delete=models.CASCADE, 
        related_name='element_cards',
        null = False,
        blank = False
        )
    recipient_name = models.CharField(
        max_length=50, 
        null=True, 
        blank=True
        )
    message = models.TextField(
        max_length=300, 
        null=True, 
        blank=True
        )
    no_message = models.BooleanField(default=False)
    background_image = models.ImageField(
        upload_to='card_backgrounds/', 
        null=True, 
        blank=True
        )
    pdf_file = models.FileField(
        upload_to='card_pdfs/', 
        null=True, 
        blank=True
        )
    is_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Card '{self.recipient_name}' by {self.user.email}"
