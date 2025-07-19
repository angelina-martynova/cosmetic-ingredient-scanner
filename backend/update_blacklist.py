import requests
import json
import os

BLACKLIST_FILE = "backend/blacklist.json"
FULL_FILE = "backend/full_blacklist.json"

SOURCES = [
    "https://raw.githubusercontent.com/openlists/ewg-cosmetics/main/blacklist.json",
    "https://raw.githubusercontent.com/kivvach/ingredients-data/main/data/ewg_extended.json"
]

def fetch_data():
    data = []
    for url in SOURCES:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                items = response.json()
                if isinstance(items, list):
                    data.extend(items)
                elif isinstance(items, dict) and "ingredients" in items:
                    data.extend(items["ingredients"])
        except Exception as e:
            print(f"⚠️ Не вдалося отримати {url}: {e}")
    return data

def normalize(entry):
    return {
        "name": entry.get("name", "Unknown"),
        "category": entry.get("category", "Невідомо"),
        "safety": entry.get("safety", "Unknown"),
        "description": entry.get("description", "")
    }

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("🔄 Завантаження списків...")
    raw = fetch_data()
    combined = [normalize(e) for e in raw if "name" in e]

    # Зберігаємо повний список
    save_json(FULL_FILE, combined)
    print(f"✅ Збережено повний список: {len(combined)} інгредієнтів")

    # Створюємо короткий блекліст лише з небезпечних (safety >= 4 або є ключові слова)
    danger = [e for e in combined if str(e.get("safety", "")).startswith("4") 
              or str(e.get("safety", "")).startswith("5")
              or str(e.get("safety", "")).startswith("6")
              or str(e.get("safety", "")).startswith("7")
              or str(e.get("safety", "")).startswith("8")]
    save_json(BLACKLIST_FILE, danger)
    print(f"⚠️ Збережено чорний список: {len(danger)} шкідливих інгредієнтів")

if __name__ == "__main__":
    main()