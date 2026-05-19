import base64
import os
from openai import OpenAI
from core import settings

# This function generates or improves a thank-you card message.


def generate_card_message(recipient_type, theme, message=""):
    """
    Generate or improve a short thank-you card message.
    """

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return None

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Write a short thank-you card message.

    Recipient type: {recipient_type}
    Theme: {theme}
    Existing message: {message}

    Requirements:
    - Warm and friendly
    - Maximum 300 characters
    - Suitable for a thank-you card
    - Do not include quotation marks
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=120,
    )

    return response.output_text.strip()

# This function generates a thank-you card background image based on the card's attributes.


def generate_card_background(card):
    if not settings.OPENAI_API_KEY:
        return None

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        timeout=120.0,
    )

    prompt = f"""
    Create a beautiful thank-you card background.

    Recipient type: {card.recipient_type.name}
    Theme: {card.theme.name}
    Main colour: {card.colour.name}
    Decorative element: {card.element.name}

    Requirements:
    - visually appealing
    - suitable for a thank-you card
    - leave clear empty space in the center for message text containing 300 characters
    - no words
    - no letters
    - no watermark
    - white background with a soft border in the main colour is preferred,
    - Add title text to the image that says "Thank You" in a stylish font that complements the card's theme and colour scheme. The title should be prominently displayed but not overpower the top message area.
    - avoid overly complex patterns that may distract from the message
    - pictures should be in a style that complements the card's theme and colour scheme
    - avoid using the same decorative element as the main focus of the image to prevent visual clutter
    - the elements should be arranged in a way that frames the central message area without overwhelming it
    - watercolour style of elements is preferred, as it adds a soft and elegant touch to the card's design
    """

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )

        image_base64 = result.data[0].b64_json
        return base64.b64decode(image_base64)

    except Exception as error:
        print(f"OpenAI image generation failed: {error}")
        return None