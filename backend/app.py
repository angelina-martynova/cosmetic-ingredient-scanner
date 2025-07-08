from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr import extract_text
from checker import check_ingredients

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    text = extract_text(image)
    results = check_ingredients(text)

    return jsonify({
        "raw_text": text,
        "risky_ingredients": results
    })

if __name__ == '__main__':
    app.run(debug=True)
