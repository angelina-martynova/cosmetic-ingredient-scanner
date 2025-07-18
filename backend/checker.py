import json
from fuzzywuzzy import fuzz

# Завантаження злитого списку
with open("full_blacklist.json", encoding="utf-8") as f:
    blacklist = json.load(f)

def check_ingredients(text):
    results = []
    found_matches = set()

    # 1. Обробка тексту: поділяємо на інгредієнти
    lines = text.split("\n")
    flat = ",".join(lines).replace(";", ",")
    ingredients = [i.strip().lower() for i in flat.split(",") if i.strip()]

    # 2. Перевірка кожного інгредієнта проти blacklist
    for ing in ingredients:
        matched = False
        for entry in blacklist:
            all_names = [entry["name"].lower()] + [a.lower() for a in entry.get("aliases", [])]
            for name in all_names:
                similarity = fuzz.token_set_ratio(ing, name)
                if similarity >= 75:
                    results.append({
                        "match": ing,
                        "name": entry["name"],
                        "risk": entry["risk"],
                        "category": entry.get("category", "Невідомо"),
                        "description": entry.get("description", ""),
                        "score": similarity
                    })
                    found_matches.add(ing)
                    matched = True
                    break
            if matched:
                break

    # 3. Інші — виводимо як безпечні
    for ing in ingredients:
        if ing not in found_matches:
            results.append({
                "match": ing,
                "name": None,
                "risk": "Safe",
                "category": None,
                "description": "Інгредієнт не знайдено у базі.",
                "score": None
            })

    return results