import cv2
import numpy as np
from PIL import Image
import pytesseract
import io

# Вказати шлях до tesseract, якщо не у PATH.
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text(file):
    image = Image.open(io.BytesIO(file.read())).convert('RGB')
    image = np.array(image)

    # Обробка зображення для покращення OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    contrast = cv2.convertScaleAbs(thresh, alpha=1.8, beta=0)

    # Розпізнавання тексту (англійська + українська)
    text = pytesseract.image_to_string(contrast, lang='eng+ukr')
    return text