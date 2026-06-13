from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['recipient_type',
                  'theme', 
                  'colour',
                  'element', 
                  'recipient_name',
                  'message',
                  'no_message',
                  ]
