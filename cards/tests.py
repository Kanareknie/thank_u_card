from django.test import TestCase

# Create your tests here.

# This file contains tests for the card creation functionality.
# It tests that a logged-in user can create a card with valid data.
# Also that the card is saved correctly in the database.
# The test also checks that the user is redirected to
# the home page after creating a card.

# Imports

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model


from .models import Card, RecipientType, Theme, Colour, Element


# Test case for card creation
@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
    )
class CardCreationTests(TestCase):
    def setUp(self):
        # Create a test user and necessary related objects for card creation
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="Testpass123"
        )

        # Create related objects for card creation
        self.recipient_type = RecipientType.objects.create(name="Teacher")
        self.theme = Theme.objects.create(name="Cute")
        self.colour = Colour.objects.create(name="Pink")
        self.element = Element.objects.create(name="Hearts")

    # Test that a logged-in user can create a card with valid data
    def test_logged_in_user_can_create_card(self):
        self.client.login(
            username="test@example.com",
            password="Testpass123"
        )

        # Simulate a POST request to create a card with valid data
        response = self.client.post(
            reverse("home"),
            {
                "recipient_type": self.recipient_type.id,
                "theme": self.theme.id,
                "colour": self.colour.id,
                "element": self.element.id,
                "recipient_name": "Mrs Smith",
                "message": "Thank you for helping me.",
                "no_message": False,
                "action": "save_card",
            }
        )

        # Check that the card was created successfully and that
        # the user is redirected to the home page
        self.assertEqual(Card.objects.count(), 1)

        card = Card.objects.first()
        self.assertEqual(card.user, self.user)
        self.assertEqual(card.recipient_name, "Mrs Smith")
        self.assertEqual(card.message, "Thank you for helping me.")
        self.assertRedirects(response, reverse("home"))
