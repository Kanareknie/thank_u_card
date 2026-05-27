# PDF generation helper functions for cards.
# Helper function inspired by ReportLab text measurement.
# ReportLab does not automatically wrap text when using drawCentredString,
# so the message is split into shorter lines that fit inside the card message box.
# https://docs.reportlab.com/reportlab/userguide/ch2_graphics/

# This implementation uses ReportLab to create the final downloadable card PDF.
# Uses canvas.Canvas(...), setFont(...), drawCentredString(...), showPage(), and save()
# https://docs.reportlab.com/reportlab/userguide/ch2_graphics/


# Django FileField / saving files to models - 
# How Django handles FileField and ImageField, which is what your card.pdf_file field uses.
# https://docs.djangoproject.com/en/6.0/topics/files/

# Python's io module for in-memory file handling, which is used to create 
# a file-like object for the PDF data before saving it to the model.
# https://docs.python.org/3/library/io.html

from io import BytesIO

import requests
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


# Draw text in wrapped lines, centred around x.
def draw_wrapped_text(pdf, text, x, y, max_width, line_height):
   
    if not text:
        return y

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()

        # Check if the test line fits within the max width using the current font 
        # settings - Helvetica is the safe default build-in font in ReportLab.
        if pdf.stringWidth(test_line, "Helvetica", 14) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    for line in lines:
        pdf.drawCentredString(x, y, line)
        y -= line_height

    return y


# Generate a square PDF for a paid card and save it to card.pdf_file. 
def generate_card_pdf(card):
   
    # Create an in-memory file-like object to hold the PDF data.
    buffer = BytesIO()

    page_size = (6 * inch, 6 * inch)
    
    pdf = canvas.Canvas(buffer, pagesize=page_size)
    width, height = page_size

     # 1. Draw generated background image full-page
    if card.background_image:
        image_url = card.background_image.url
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()

        image_file = BytesIO(response.content)
        background = ImageReader(image_file)

        pdf.drawImage(
            background,
            0,
            0,
            width=width,
            height=height,
            preserveAspectRatio=False,
            mask="auto",
        )

    # 2. Draw message only if user did not select "Card without message"
    if not card.no_message:
        box_width = width * 0.72
        box_height = height * 0.34
        box_x = (width - box_width) / 2
        box_y = height * 0.24

        # White transparent-style box. ReportLab does not always handle opacity
        # reliably across viewers, so this uses solid white for consistency.
        pdf.setFillColorRGB(1, 1, 1)
        pdf.roundRect(
            box_x,
            box_y,
            box_width,
            box_height,
            radius=14,
            fill=1,
            stroke=0,
        )

        text_center_x = width / 2
        text_y = box_y + box_height - 45

        if card.recipient_name:
            recipient_text = f"Dear {card.recipient_name}"

            pdf.setFont("Helvetica-Bold", 13)
            pdf.setFillColorRGB(0, 0, 0)

            text_y = draw_wrapped_text(
                pdf=pdf,
                text=recipient_text,
                x=text_center_x,
                y=text_y,
                max_width=box_width - 55,
                line_height=16,
                font_name="Helvetica-Bold",
                font_size=13,
            )

            text_y -= 8

        if card.message:
            pdf.setFont("Helvetica", 14)
            pdf.setFillColorRGB(0, 0, 0)

            draw_wrapped_text(
                pdf=pdf,
                text=card.message,
                x=text_center_x,
                y=text_y,
                max_width=box_width - 55,
                line_height=16,
            )

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    filename = f"thank_u_card_{card.id}.pdf"

    # Replace old PDF if one already exists
    if card.pdf_file:
        card.pdf_file.delete(save=False)

    card.pdf_file.save(
        filename,
        ContentFile(buffer.getvalue()),
        save=True,
    )

    buffer.close()

    return card.pdf_file