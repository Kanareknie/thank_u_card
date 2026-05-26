# PDF generation helper functions for cards.

# This is a simple implementation using ReportLab to create a placeholder PDF.
# Uses canvas.Canvas(...), setFont(...), drawCentredString(...), showPage(), and save()
# https://docs.reportlab.com/reportlab/userguide/ch2_graphics/


# Django FileField / saving files to models - 
# How Django handles FileField and ImageField, which is what your card.pdf_file field uses.
# https://docs.djangoproject.com/en/6.0/topics/files/

# Python's io module for in-memory file handling, which is used to create 
# a file-like object for the PDF data before saving it to the model.
# https://docs.python.org/3/library/io.html

from io import BytesIO

from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas


def generate_card_pdf(card):
    """
    Generate a square PDF for a paid card and save it to card.pdf_file.
    First simple version: placeholder PDF only.
    """
    # Create an in-memory file-like object to hold the PDF data.
    buffer = BytesIO()

    page_size = (6 * inch, 6 * inch)

    # Create a PDF canvas and draw some placeholder content.
    pdf = canvas.Canvas(buffer, pagesize=page_size)
    width, height = page_size

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2, height - 80, "Thank You Card")

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, height / 2, f"Card ID: {card.id}")

    pdf.showPage()
    pdf.save()

    # Move the buffer's position to the beginning so we can read its content.
    buffer.seek(0)

    filename = f"thank_u_card_{card.id}.pdf"

    # Save the PDF data to the card's pdf_file field using Django's FileField handling.
    card.pdf_file.save(
        filename,
        ContentFile(buffer.getvalue()),
        save=True,
    )

    # Close the buffer to free up resources.
    buffer.close()

    return card.pdf_file