import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

BASE_URL = "https://incidecoder.com/ingredients/"
output = []

# Список популярних інгредієнтів (можна розширити)
ingredients_to_fetch = [
    "sodium-laureth-sulfate",
    "methylparaben",
    "propylene-glycol",
    "triclosan",
    "formaldehyde",
    "benzyl-alcohol",
    "sodium-lauryl-sulfate",
    "diazolidinyl-urea",
    "parfum"
]

for slug in tqdm(ingredients_to_fetch):
    url = BASE_URL + slug
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        name = soup.find("h1").text.strip()
        risk_desc = soup.find("div", class_="card-body").text.strip().split("\n")[0]
        description = soup.find("meta", {"name": "description"})["content"]

        output.append({
            "name": name,
            "aliases": [],
            "risk": "High" if "irritant" in risk_desc.lower() or "cancer" in risk_desc.lower() else "Medium",
            "description": description
        })

    except Exception as e:
        print(f"[!] Error on {slug}: {e}")

# Зберігаємо
with open("blacklist_auto.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ Збережено {len(output)} інгредієнтів у blacklist_auto.json")
