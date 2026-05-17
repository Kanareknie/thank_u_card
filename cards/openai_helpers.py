import os

from openai import OpenAI


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