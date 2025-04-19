import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_HONEY = "https://genshin.honeyhunterworld.com"
BASE_WIKI = "https://genshin-impact.fandom.com/wiki"

def fetch_honey_characters():
    url = f"{BASE_HONEY}/db/char/"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).content, "html.parser")
    characters = []

    for link in soup.select("a.char_sea_cont"):
        name = link.text.strip()
        href = link["href"]
        full_link = BASE_HONEY + href
        characters.append({"name": name, "url": full_link})
    
    return characters

def scrape_character_details(character):
    res = requests.get(character['url'], headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")

    char_data = {"name": character["name"], "url": character["url"]}
    details = {}

    for row in soup.select("div.char_profile_stat_main div.sea_char_box"):
        for label in row.select("div"):
            k = label.get("title") or label.text.strip()
            v = label.find_next_sibling("div")
            if v:
                details[k] = v.text.strip()
    
    char_data["details"] = details
    return char_data

def fetch_and_save_characters():
    characters = fetch_honey_characters()
    result = []

    for char in tqdm(characters, desc="Scraping characters"):
        try:
            data = scrape_character_details(char)
            result.append(data)
        except Exception as e:
            print(f"Error with {char['name']}: {e}")

    with open("data/characters.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def fetch_fandom_summary(page):
    url = f"{BASE_WIKI}/{page.replace(' ', '_')}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")

    content = soup.select_one("div.mw-parser-output")
    paragraphs = content.find_all("p", recursive=False)
    lore = "\n".join([p.get_text().strip() for p in paragraphs if p.text.strip()])
    
    return {"title": page, "url": url, "summary": lore}

def fetch_example_lore_pages():
    lore_pages = ["Teyvat", "Archons", "Fatui", "Khaenri'ah", "Abyss_Order"]
    summaries = [fetch_fandom_summary(p) for p in tqdm(lore_pages, desc="Fetching lore pages")]
    
    with open("data/lore.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    fetch_and_save_characters()
    fetch_example_lore_pages()
