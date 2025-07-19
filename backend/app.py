from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
from ocr import extract_text
import json

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
    for ingredient in all_blacklist:
        if ingredient['name'] not in seen_names:
            unique_blacklist.append(ingredient)
            seen_names.add(ingredient['name'])

    return unique_blacklist

# Перевірка інгредієнтів у тексті
def check_ingredients(text):
    blacklist = load_blacklist()  # Завантажуємо злитий чорний список
    found_ingredients = []
    for ingredient in blacklist:
        if any(alias.lower() in text.lower() for alias in ingredient["aliases"]) or ingredient["name"].lower() in text.lower():
            found_ingredients.append(ingredient)
    return found_ingredients

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
        return jsonify({"status": "error", "message": "Помилка під час аналізу. Спробуйте інше фото."}), 500

# Статичні файли (CSS, зображення тощо)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'frontend', 'static'), filename)

if __name__ == "__main__":
    app.run(debug=True)
