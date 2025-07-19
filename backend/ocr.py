import cv2
import numpy as np
from PIL import Image
import pytesseract
import io
import re

# Вказати шлях до tesseract, якщо не у PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Налаштування параметрів для Tesseract для покращення точності
custom_config = r'--oem 3 --psm 6'

def clean_text(text):
    # Відфільтровуємо непотрібні символи, пробіли на початку/в кінці
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    cleaned_text = re.sub(r'[^a-zA-Z0-9а-яА-ЯіІїЇєЄёЁ\s\.,;:!?-]', '', cleaned_text)
    return cleaned_text

def extract_text(file):
    # Завантажуємо зображення
    image = Image.open(io.BytesIO(file.read())).convert('RGB')
    image = np.array(image)

    # Перетворення в відтінки сірого для зменшення шуму
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Застосування бiлатерального фільтра для згладжування зображення
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Адаптивне порогування для виділення тексту
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Покращення контрасту
    contrast = cv2.convertScaleAbs(thresh, alpha=1.8, beta=0)

    # Розпізнавання тексту з використанням налаштувань Tesseract
    text = pytesseract.image_to_string(contrast, lang='eng+ukr+rus', config=custom_config)

    # Логування для відлагодження
    print("Розпізнаний текст:", text)

    # Очищаємо текст від зайвих символів
    cleaned_text = clean_text(text)

    # Логування для відлагодження
    print("Очищений текст:", cleaned_text)

    return cleaned_text
