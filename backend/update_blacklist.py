import json
import argparse
import os

MANUAL_FILE = "backend/blacklist.json"
AUTO_FILE = "backend/blacklist_auto.json"
FULL_FILE = "backend/full_blacklist.json"

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)  # <== Створює папку, якщо її нема
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def merge_lists(manual, auto):
    merged = {item["name"].lower(): item for item in manual}
    for item in auto:
        key = item["name"].lower()
        if key not in merged:
            merged[key] = item
    return list(merged.values())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Оновити full_blacklist.json з manual + auto")
    args = parser.parse_args()

    if args.update:
        manual = load_json(MANUAL_FILE)
        auto = load_json(AUTO_FILE)
        combined = merge_lists(manual, auto)
        save_json(FULL_FILE, combined)
        print(f"✅ Оновлено {len(combined)} інгредієнтів у {FULL_FILE}")

if __name__ == "__main__":
    main()
