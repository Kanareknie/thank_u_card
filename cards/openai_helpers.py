import base64
import os
from openai import OpenAI
from core import settings

# This function generates or improves a thank-you card message.


def generate_card_message(recipient_type, theme, message=""):

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
    - Maximum 120 characters
    - Suitable for a thank-you card
    - Do not include quotation marks
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=120,
    )

    return response.output_text.strip()

# Prompts for image generation INCLUDING main, colour, element, theme, recipient,
# and safety instructions.

MAIN_PROMPT = (
    "Create a square image featuring one large soft 3D rounded foam note panel "
    "as the main object. The note panel should be centered, smooth, plushy, "
    "slightly glossy, and have softly rounded corners. It should occupy about "
    "65% of the image width and 65% of the image height, leaving a clean blank "
    "surface for later text overlay. Use a white background with gentle "
    "studio lighting and a subtle floating shadow under the panel. Add only a "
    "few small decorative accents around the panel corners or outer edges. "
    "Keep the central surface completely blank and uncluttered. Style: cute "
    "modern soft 3D, plush foam, clay-like, premium pastel, rounded, minimal, "
    "polished. Do not create a flat border frame. Do not create a full "
    "decorative wreath. Do not fill the edges with many decorations. Do not "
    "include any text, words, letters, numbers, handwriting, typography, "
    "watermark, people, or logos."
)


COLOUR_PROMPTS = {
    "Blush Pink": (
        "Use a blush pink pastel colour palette with a soft rose gold metallic "
        "accent. Keep the background of the card light blush pink, and use subtle rose gold "
        "highlights in tiny decorative details. Behind the panel, use a white background with gentle studio lighting "
        "and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Dusty Rose": (
        "Use a dusty rose pastel colour palette with a soft rose gold metallic "
        "accent. Keep the background of the card muted rosy pink, and use subtle rose gold "
        "highlights in tiny decorative details. Behind the panel, use a white background with gentle studio lighting "
        "   and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Peach Apricot": (
        "Use a peach apricot pastel colour palette with a soft rose gold metallic "
        "accent. Keep the background of the card warm and peachy, and use subtle rose gold "
        "highlights in tiny decorative details. Behind the panel, use a white background with gentle studio lighting "
        "and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Dove Grey": (
        "Use a dove grey pastel colour palette with a soft silver metallic "
        "accent. Keep the background of the card light grey and airy, and use subtle silver "
        "highlights in tiny decorative details. Behind the panel, use a white background with gentle studio lighting "
        "and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Powder Blue": (
        "Use a powder blue pastel colour palette with a soft silver metallic "
        "accent. Keep the background of the card light powder blue, and use subtle silver "
        "highlights in tiny decorative details. Behind the panel, use a white background with gentle studio lighting "
        "and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Lavender": (
        "Use a lavender pastel colour palette with a soft silver metallic accent. "
        "Keep the background of the card soft lavender, and use subtle silver highlights in "
        "tiny decorative details. Behind the panel, use a white background with gentle studio lighting "
        "and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Butter Yellow": (
        "Use a butter yellow pastel colour palette with a soft yellow gold "
        "metallic accent. Keep the background of the card soft buttery yellow, and use subtle "
        "gold highlights in tiny decorative details. Behind the panel, use a white background with gentle studio lighting "
        "and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Cream Beige": (
        "Use a cream beige pastel colour palette with a soft champagne gold "
        "metallic accent. Keep the background of the card creamy beige, and use subtle "
        "champagne gold highlights in tiny decorative details. Behind the panel, use a white background with gentle "
        "studio lighting and a subtle floating shadow under the panel to create a soft 3D look."
    ),
    "Soft Mint": (
        "Use a soft mint pastel colour palette with a soft champagne gold "
        "metallic accent. Keep the background of the card fresh mint green, and use subtle "
        "champagne gold highlights in tiny decorative details. Behind the panel, use a white background with gentle "
        "studio lighting and a subtle floating shadow under the panel to create a soft 3D look."
    ),
}


ELEMENT_PROMPTS = {
    "Hearts": (
        "Use hearts as the main decorative accents. Place only a few soft 3D "
        "hearts around the corners or edges of the main note panel."
    ),
    "Flowers": (
        "Use flowers as the main decorative accents. Place only a few soft 3D "
        "flowers around the corners or edges of the main note panel."
    ),
    "Bows": (
        "Use bows as the main decorative accents. Place only a few soft 3D bows "
        "around the corners or edges of the main note panel."
    ),
    "Stars": (
        "Use stars as the main decorative accents. Place only a few soft 3D stars "
        "around the corners or edges of the main note panel."
    ),
    "Leaves": (
        "Use leaves as the main decorative accents. Place only a few soft 3D "
        "leaves around the corners or edges of the main note panel."
    ),
    "Bears": (
        "Use bears as the main decorative accents. Place only a few cute soft 3D "
        "bear details around the corners or edges of the main note panel, while "
        "keeping the center clear."
    ),
    "Clouds": (
        "Use clouds as the main decorative accents. Place only a few soft 3D "
        "clouds around the corners or edges of the main note panel."
    ),
    "Geometric": (
        "Use soft rounded geometric shapes as the main decorative accents. Place "
        "only a few minimal 3D geometric details around the corners or edges of "
        "the main note panel."
    ),
}


THEME_PROMPTS = {
    "Cute": (
        "Make the overall style cute, sweet, playful, and charming. Use rounded "
        "shapes, soft details, and a friendly whimsical look."
    ),
    "Elegant": (
        "Make the overall style elegant, graceful, and refined. Use a polished "
        "composition, delicate details, and a soft premium look."
    ),
    "Modern": (
        "Make the overall style modern, clean, and minimal. Use smooth shapes, "
        "balanced spacing, and a polished contemporary look."
    ),
    "Fun": (
        "Make the overall style fun, cheerful, and lively. Use playful decorative "
        "details, a joyful composition, and a bright soft 3D look."
    ),
}


RECIPIENT_PROMPTS = {
    "Teacher": (
        "Make the mood calm, respectful, and thoughtful. Keep the design neat, "
        "balanced, and polished with subtle refined decorative accents."
    ),
    "Friend": (
        "Make the mood warm, cheerful, and playful. Keep the design friendly, "
        "lively, and inviting with light joyful decorative accents."
    ),
    "Wedding guest": (
        "Make the mood elegant, soft, and romantic. Keep the design graceful and "
        "delicate with refined decorative accents."
    ),
    "Parent/family": (
        "Make the mood cozy, loving, and gentle. Keep the design warm, "
        "comforting, and soft with sweet decorative accents."
    ),
    "Colleague": (
        "Make the mood clean, polished, and modern. Keep the design professional, "
        "minimal, and balanced with subtle decorative accents."
    ),
}


SAFETY_PROMPT = (
    "Keep the composition simple and balanced. Do not overcrowd the design. "
    "Do not place decorations in the center of the note panel. Leave the main "
    "note panel fully blank for later text overlay."
)


# This function builds the final image generation prompt from the saved card options.

def build_background_prompt(card):
    """
    Build the final image generation prompt from the saved card options.
    """

    recipient_type_name = card.recipient_type.name if card.recipient_type else ""
    theme_name = card.theme.name if card.theme else ""
    colour_name = card.colour.name if card.colour else ""
    element_name = card.element.name if card.element else ""

    final_prompt = " ".join(
        [
            MAIN_PROMPT,
            COLOUR_PROMPTS.get(colour_name, ""),
            ELEMENT_PROMPTS.get(element_name, ""),
            THEME_PROMPTS.get(theme_name, ""),
            RECIPIENT_PROMPTS.get(recipient_type_name, ""),
            SAFETY_PROMPT,
        ]
    )

    return final_prompt



# This function generates a thank-you card background image based on the card's attributes.


def generate_card_background(card):
    if not settings.OPENAI_API_KEY:
        return None

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        timeout=120.0,
    )

    prompt = build_background_prompt(card)

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
    