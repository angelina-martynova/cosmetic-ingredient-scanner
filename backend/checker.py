import json
from fuzzywuzzy import fuzz

# Завантажуємо blacklist
with open("blacklist.json", encoding='utf-8') as f:
    blacklist = json.load(f)

def check_ingredients(text):
    results = []
    found_names = []

    # 1. Розбиваємо OCR-текст на інгредієнти
    lines = text.split('\n')
    flat_text = ','.join(lines).replace(';', ',')  # прибираємо крапки з комою
    ingredients = [i.strip().lower() for i in flat_text.split(',') if i.strip()]

    # 2. Перевіряємо кожен інгредієнт проти blacklist
    for ing in ingredients:
        matched = False
        for entry in blacklist:
            all_names = [entry["name"].lower()] + [a.lower() for a in entry.get("aliases", [])]
            for name in all_names:
                similarity = fuzz.token_set_ratio(ing, name)
                if similarity > 75:
                    results.append({
                        "match": ing,
                        "name": entry["name"],
                        "risk": entry["risk"],
                        "description": entry["description"],
                        "score": similarity
                    })
                    found_names.append(ing)
                    matched = True
                    break
            if matched:
                break

    # 3. Додаємо інгредієнти, які не знайдено (для повного списку)
    for ing in ingredients:
        if ing not in found_names:
            results.append({
                "match": ing,
                "name": None,
                "risk": "Safe",
                "description": "Інгредієнт не знайдено у blacklist.",
                "score": None
            })

    return results
