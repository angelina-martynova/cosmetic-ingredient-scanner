from flask import Flask, request, jsonify, render_template, send_from_directory, make_response
from flask_cors import CORS
import json, os
from ocr import extract_text
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
import io

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')
CORS(app)

# Завантаження чорного списку інгредієнтів
def load_blacklist():
    with open('blacklist.json', 'r', encoding='utf-8') as f:
        blacklist = json.load(f)
    with open('blacklist_auto.json', 'r', encoding='utf-8') as f:
        blacklist_auto = json.load(f)
    with open('full_blacklist.json', 'r', encoding='utf-8') as f:
        full_blacklist = json.load(f)

    # Злиття чорних списків
    all_blacklist = blacklist + blacklist_auto + full_blacklist
    unique_blacklist = []
    seen_names = set()

    print("Завантажено інгредієнтів:", len(all_blacklist))  # Логування кількості інгредієнтів

    for ingredient in all_blacklist:
        if ingredient['name'] not in seen_names:
            unique_blacklist.append(ingredient)
            seen_names.add(ingredient['name'])

    return unique_blacklist

# Перевірка інгредієнтів у тексті
def check_ingredients(text):
    blacklist = load_blacklist()  # Завантажуємо злитий чорний список
    found_ingredients = []

    print("Текст для перевірки інгредієнтів:", text)  # Логування тексту перед пошуком

    # Шукаємо інгредієнти в очищеному тексті
    for ingredient in blacklist:
        if any(alias.lower() in text.lower() for alias in ingredient["aliases"]) or ingredient["name"].lower() in text.lower():
            found_ingredients.append(ingredient)
            print(f"Знайдено інгредієнт: {ingredient['name']}")  # Логування знайдених інгредієнтів

    if not found_ingredients:
        print("Інгредієнти не знайдено.")  # Якщо інгредієнти не знайдені

    return found_ingredients

# Генерація PDF з форматуванням
def generate_pdf(text, ingredients):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    # Отримуємо стилі для форматування
    styles = getSampleStyleSheet()

    # Заголовок
    header_style = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=16, spaceAfter=10)
    header = Paragraph("Результати аналізу складу косметичного засобу", header_style)
    story.append(header)

    # Розпізнаний текст
    text_style = ParagraphStyle('Text', parent=styles['Normal'], fontSize=12, spaceAfter=10)
    recognized_text = Paragraph(f"<b>Розпізнаний текст:</b><br/> {text}", text_style)
    story.append(recognized_text)

    # Виявлені інгредієнти
    if ingredients:
        ingredient_header = Paragraph("<b>Виявлені інгредієнти:</b>", header_style)
        story.append(ingredient_header)

        for ingredient in ingredients:
            risk = ingredient.get('risk', 'Невідомо')
            description = ingredient.get('description', 'Невідомо')

            # Форматуємо для кожного інгредієнта
            ingredient_text = f"<b>{ingredient['name']}</b> - Ризик: {risk}<br/> Опис: {description}"
            ingredient_paragraph = Paragraph(ingredient_text, text_style)
            story.append(ingredient_paragraph)

    # Створення PDF
    doc.build(story)

    buffer.seek(0)
    return buffer

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')  # Повертаємо HTML з папки frontend

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        image = request.files['image']
        text = extract_text(image)
        results = check_ingredients(text)
        return jsonify({
            "status": "success",
            "text": text,
            "ingredients": results
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Помилка під час аналізу: {e}"}), 500

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    try:
        data = request.get_json()  # Отримуємо JSON з запиту
        text = data['text']  # Отримуємо текст
        ingredients = data['ingredients']  # Отримуємо інгредієнти

        # Генерація PDF
        pdf_file = generate_pdf(text, ingredients)

        # Відправка PDF як відповіді
        response = make_response(pdf_file.read())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=results.pdf"

        return response
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Помилка при створенні PDF: {e}"}), 500

# Статичні файли (CSS, зображення тощо)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'frontend', 'static'), filename)

if __name__ == "__main__":
    app.run(debug=True)
