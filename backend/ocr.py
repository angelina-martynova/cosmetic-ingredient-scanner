import cv2
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import io

def extract_text(file):
    image = Image.open(io.BytesIO(file.read()))
    image = np.array(image)

    # Попередня обробка зображення
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    contrast = cv2.convertScaleAbs(thresh, alpha=1.8, beta=0)

    # Розпізнавання тексту
    text = pytesseract.image_to_string(contrast, lang='eng')
    return text