import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0"
}

base_url = "https://genshin-impact.fandom.com/wiki"

# Replace with actual character list from Fandom
characters = [
    "Albedo", "Amber", "Arataki_Itto", "Baizhu", "Barbara", "Beidou", "Bennett", "Candace",
    "Charlotte", "Chevreuse", "Chongyun", "Collei", "Cyno", "Dehya", "Diluc", "Diona", "Dori",
    "Eula", "Faruzan", "Fischl", "Freminet", "Ganyu", "Gaming", "Gorou", "Hu_Tao", "Jean",
    "Kaedehara_Kazuha", "Kaeya", "Kamisato_Ayaka", "Kamisato_Ayato", "Kaveh", "Keqing", "Kirara",
    "Klee", "Kujou_Sara", "Kuki_Shinobu", "Layla", "Lisa", "Lynette", "Lyney", "Mika", "Mona",
    "Nahida", "Neuvillette", "Nilou", "Ningguang", "Noelle", "Qiqi", "Raiden_Shogun", "Razor",
    "Rosaria", "Sangonomiya_Kokomi", "Sayu", "Shenhe", "Shikanoin_Heizou", "Sucrose", "Tartaglia",
    "Thoma", "Tighnari", "Traveler", "Venti", "Wanderer", "Wriothesley", "Xiangling", "Xianyun",
    "Xiao", "Xingqiu", "Xinyan", "Yae_Miko", "Yanfei", "Yaoyao", "Yelan", "Yoimiya", "Yun_Jin",
    "Zhongli","Clorinde","Emilie","Furina","Navia","Sigewinne","Wriothesley","Arlecchino","Escoffier",
    "Chasca","Citlali","Iansan","Kachina","Kinich","Mavuika","Mualani","Ororon","Varesa","Xilonen","Ifa"
]

def get_wiki_content(url):
    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"⚠️ Failed: {url}")
            return ""
        soup = BeautifulSoup(r.content, "html.parser")
        content = soup.select_one("div.mw-parser-output")
        if not content:
            return ""
        paragraphs = content.find_all("p", recursive=False)
        text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def scrape_all_characters():
    os.makedirs("data", exist_ok=True)
    character_lore_data = {}

    for name in tqdm(characters, desc="Scraping Characters"):
        char_name = name.replace("_", " ")
        overview_url = f"{base_url}/{name}"
        lore_url = f"{base_url}/{name}/Lore"

        overview = get_wiki_content(overview_url)
        lore = get_wiki_content(lore_url)

        character_lore_data[char_name] = {
            "overview_url": overview_url,
            "lore_url": lore_url,
            "overview": overview,
            "lore": lore
        }

    with open("data/character_lore.json", "w", encoding="utf-8") as f:
        json.dump(character_lore_data, f, indent=2, ensure_ascii=False)

    print("✅ Character lore and overviews saved to data/character_lore.json")

if __name__ == "__main__":
    scrape_all_characters()
