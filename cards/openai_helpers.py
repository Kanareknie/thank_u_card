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
    - Maximum 200 characters
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
    - create a decorative frame or border design
    - keep the main decorative elements around the edges and corners
    - include the exact title text "Thank You" near the top, center as one line
    - the title must be readable, correctly spelled, fully visible, and not distorted
    - use only the words "Thank You"; do not add any other words or letters
    - leave a large empty central area below the title for the user's message
    - the message area should be clean, light, plain, and uncluttered
    - the message area should be about 80% of the card width
    - position the message area slightly below the center of the card, around 10% lower than center
    - keep enough clear space between the title and the message area
    - do not place decorations over the title or the message area
    - use the decorative elements only to frame the card, not to fill the middle
    - avoid overly complex patterns that may distract from the message
    - use a style correct to the theme
    - no watermark
    - the overall result should look like a printable greeting card template with room for text
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