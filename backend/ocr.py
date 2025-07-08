from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import io

def extract_text(file):
    image = Image.open(io.BytesIO(file.read()))
    image = image.convert("L")  # Grayscale
    image = image.filter(ImageFilter.SHARPEN)
    image = image.point(lambda x: 0 if x < 140 else 255)  # Бінаризація
    text = pytesseract.image_to_string(image)
    return text
