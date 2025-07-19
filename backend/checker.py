import json
from fuzzywuzzy import fuzz

with open("full_blacklist.json", encoding="utf-8") as f:
    blacklist = json.load(f)

# Поширені помилки OCR (виправлення)
common_fixes = {
    "methytisctvazuivare": "Methylisothiazolinone",
    "tetrasodiurs edta": "Tetrasodium EDTA",
    "sotore": "Sorbitol",
    "cwarite": "Cocamide",
    "peg—~4": "PEG-4",
    "erccreuyl": "",
    "rezko foct": "",
    "‘bx protein": "Silk Protein",
    "seyreve": ""
}

def apply_fixes(text):
    for wrong, correct in common_fixes.items():
        text = text.replace(wrong, correct)
    return text

def check_ingredients(text):
    results = []
    found_matches = set()

    # Виправлення тексту
    text = apply_fixes(text)

    # Витягнення рядків, де ймовірно є інгредієнти
    lines = text.split("\n")
    candidate_lines = [l for l in lines if any(w in l.lower() for w in ["coctab", "ingredients", ",", "/"])]
    flat = ",".join(candidate_lines)

    ingredients = [i.strip().lower() for i in flat.split(",") if i.strip()]

    for ing in ingredients:
        matched = False
        for entry in blacklist:
            all_names = [entry["name"].lower()] + [a.lower() for a in entry.get("aliases", [])]
            for name in all_names:
                score1 = fuzz.token_sort_ratio(ing, name)
                score2 = fuzz.partial_ratio(ing, name)
                if score1 >= 70 or score2 >= 80:
                    results.append({
                        "match": ing,
                        "name": entry["name"],
                        "risk": entry["risk"],
                        "category": entry.get("category", "Невідомо"),
                        "description": entry.get("description", ""),
                        "score": max(score1, score2)
                    })
                    found_matches.add(ing)
                    matched = True
                    break
            if matched:
                break

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