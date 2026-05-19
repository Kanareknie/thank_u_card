from celery import shared_task
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Card
from .openai_helpers import generate_card_background

# This is a Celery task that generates a thank-you card background image 
# based on the card's attributes and saves it to the card instance.
@shared_task
def generate_background_task(card_id):
    try:
        card = Card.objects.get(id=card_id)

        image_bytes = generate_card_background(card)

        if image_bytes:
            filename = f"card_{card.id}_{slugify(card.theme.name)}.png"
            card.background_image.save(
                filename,
                ContentFile(image_bytes),
                save=True,
            )
            return f"Background generated for card {card.id}"

        return f"No image generated for card {card.id}"

    except Card.DoesNotExist:
        return f"Card with id {card_id} does not exist"

    except Exception as error:
        print(f"Celery task failed: {error}")
        return f"Task failed for card {card_id}"
    