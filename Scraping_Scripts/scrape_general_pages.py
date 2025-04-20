import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Paste all the links from your file that are NOT character-specific
wiki_pages = [
    # Factions
    "https://genshin-impact.fandom.com/wiki/The_Seven",
    "https://genshin-impact.fandom.com/wiki/Adventurers%27_Guild",
    "https://genshin-impact.fandom.com/wiki/Knights_of_Favonius",
    "https://genshin-impact.fandom.com/wiki/Liyue_Qixing",
    "https://genshin-impact.fandom.com/wiki/Inazuma_Shogunate",
    "https://genshin-impact.fandom.com/wiki/Sumeru_Akademiya",
    "https://genshin-impact.fandom.com/wiki/Palais_Mermonia",
    "https://genshin-impact.fandom.com/wiki/Speaker%27s_Chamber",
    "https://genshin-impact.fandom.com/wiki/Fatui",

    # Regions
    "https://genshin-impact.fandom.com/wiki/Mondstadt",
    "https://genshin-impact.fandom.com/wiki/Liyue",
    "https://genshin-impact.fandom.com/wiki/Inazuma",
    "https://genshin-impact.fandom.com/wiki/Sumeru",
    "https://genshin-impact.fandom.com/wiki/Fontaine",
    "https://genshin-impact.fandom.com/wiki/Natlan",
    "https://genshin-impact.fandom.com/wiki/Snezhnaya",
    "https://genshin-impact.fandom.com/wiki/Khaenri%27ah",

    # Lore
    "https://genshin-impact.fandom.com/wiki/Timeline",
    "https://genshin-impact.fandom.com/wiki/Manga",
    "https://genshin-impact.fandom.com/wiki/Book",
    "https://genshin-impact.fandom.com/wiki/Comics",
    "https://genshin-impact.fandom.com/wiki/Archon_War",
    "https://genshin-impact.fandom.com/wiki/Cataclysm",
    "https://genshin-impact.fandom.com/wiki/Celestia",
    "https://genshin-impact.fandom.com/wiki/Khaenri%27ah"
    "https://genshin-impact.fandom.com/wiki/Delusion",
    "https://genshin-impact.fandom.com/wiki/Seven_Sovereigns",
    "https://genshin-impact.fandom.com/wiki/Heavenly_Principles",
    "https://genshin-impact.fandom.com/wiki/Dragon",
    "https://genshin-impact.fandom.com/wiki/Lore#World_History",


    # Quests
    "https://genshin-impact.fandom.com/wiki/Archon_Quest",
    "https://genshin-impact.fandom.com/wiki/Story_Quest",
    "https://genshin-impact.fandom.com/wiki/World_Quest",
    "https://genshin-impact.fandom.com/wiki/Event_Quest",

    # Enemies
    "https://genshin-impact.fandom.com/wiki/Common_Enemy",
    "https://genshin-impact.fandom.com/wiki/Elite_Enemy",
    "https://genshin-impact.fandom.com/wiki/Weekly_Boss",

    # Weapons
    "https://genshin-impact.fandom.com/wiki/Bow",
    "https://genshin-impact.fandom.com/wiki/Claymore",
    "https://genshin-impact.fandom.com/wiki/Catalyst",
    "https://genshin-impact.fandom.com/wiki/Polearm",
    "https://genshin-impact.fandom.com/wiki/Sword",

    # Artifacts
    "https://genshin-impact.fandom.com/wiki/Artifact/Sets",
    "https://genshin-impact.fandom.com/wiki/Artifact_EXP",

  
]

def extract_summary_from_url(url):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"⚠️ Failed: {url}")
            return ""

        soup = BeautifulSoup(res.content, "html.parser")
        content = soup.select_one("div.mw-parser-output")
        if not content:
            return ""

        paragraphs = content.find_all("p", recursive=False)
        summary = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        return summary
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return ""

def scrape_and_save():
    os.makedirs("data", exist_ok=True)
    wiki_data = {}

    for url in tqdm(wiki_pages, desc="Scraping Wiki Pages"):
        title = url.split("/")[-1].replace("_", " ")
        summary = extract_summary_from_url(url)
        wiki_data[title] = {
            "url": url,
            "summary": summary
        }

    with open("data/wiki_sections.json", "w", encoding="utf-8") as f:
        json.dump(wiki_data, f, indent=2, ensure_ascii=False)

    print("✅ General wiki data saved to data/wiki_sections.json")

if __name__ == "__main__":
    scrape_and_save()
