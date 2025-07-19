import json
from fuzzywuzzy import fuzz

# Завантаження блекліста
with open("backend/blacklist.json", encoding="utf-8") as f:
    BLACKLIST = json.load(f)

# Словник частих помилок OCR
common_fixes = {
    "methytisctvazuivare": "Methylisothiazolinone",
    "tetrasodiurs edta": "Tetrasodium EDTA",
    "sodim laureth sulfate": "Sodium Laureth Sulfate",
    "peg~4": "PEG-4",
    "peg—~4": "PEG-4",
    "fragranc": "Fragrance",
    "cwarite": "Cocamide",
    "sotore": "Sorbitol"
}

def clean_text(text):
    lines = text.lower().split("\n")
    ingredients_block = []
    trigger_words = ["ingredients", "coctab", ":"]

    for line in lines:
        if any(word in line for word in trigger_words):
            ingredients_block.append(line)

    all_text = " ".join(ingredients_block)
    all_text = all_text.replace(",", " ").replace(".", " ")
    tokens = all_text.split()
    return [common_fixes.get(t, t) for t in tokens]

def match_ingredient(token):
    for entry in BLACKLIST:
        if fuzz.token_sort_ratio(token.lower(), entry["name"].lower()) > 85:
            return entry
    return None

def check_ingredients(text):
    found = []
    tokens = clean_text(text)
    matched = set()

    for token in tokens:
        result = match_ingredient(token)
        if result and result["name"] not in matched:
            found.append(result)
            matched.add(result["name"])

    return found