import json
from fuzzywuzzy import fuzz

with open("backend/blacklist.json", encoding='utf-8') as f:
    blacklist = json.load(f)

def check_ingredients(text):
    found = []
    ingredients = [i.strip().lower() for i in text.split(',')]
    for ing in ingredients:
        for entry in blacklist:
            names = [entry["name"].lower()] + [a.lower() for a in entry.get("aliases", [])]
            for name in names:
                if fuzz.partial_ratio(ing, name) > 80:
                    found.append({
                        "match": ing,
                        "name": entry["name"],
                        "risk": entry["risk"],
                        "description": entry["description"]
                    })
                    break
    return found
