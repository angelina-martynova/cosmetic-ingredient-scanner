import cv2
import numpy as np
from PIL import Image
import pytesseract
import io

def extract_text(file):
    # Відкриваємо зображення
    image = Image.open(io.BytesIO(file.read()))
    image = np.array(image)

    # Перетворюємо в градації сірого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Видаляємо шум
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Адаптивна бінаризація
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Підвищення контрасту (опціонально)
    enhanced = cv2.convertScaleAbs(thresh, alpha=1.8, beta=0)

    # OCR
    text = pytesseract.image_to_string(enhanced, lang='eng')
    return text