from PIL import Image
import pytesseract
import io

def extract_text(file):
    image = Image.open(io.BytesIO(file.read()))
    text = pytesseract.image_to_string(image)
    return text
