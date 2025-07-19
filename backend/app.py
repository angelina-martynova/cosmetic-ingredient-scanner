from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr import extract_text
from checker import check_ingredients

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze_image():
    try:
        image = request.files["image"]
        text = extract_text(image)
        print("🔍 Розпізнаний текст:\n", text)
        results = check_ingredients(text)
        return jsonify({
            "status": "success",
            "text": text,
            "ingredients": results
        })
    except Exception as e:
        print("❌ Помилка:", e)
        return jsonify({"status": "error", "message": "Помилка під час аналізу. Спробуйте інше фото."}), 500

if __name__ == "__main__":
    app.run(debug=True)