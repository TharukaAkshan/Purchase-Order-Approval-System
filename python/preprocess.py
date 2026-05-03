from pdf2image import convert_from_bytes
import base64
from io import BytesIO

async def pdf_to_base64_images(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    result = []

    for img in images:
        buf = BytesIO()
        img.save(buf, format="JPEG")
        result.append(base64.b64encode(buf.getvalue()).decode())

    return result