import requests
import json
import os

def fetch_all_characters(base_url="https://gsi.fly.dev/characters", total_characters=52):
    all_characters = []

    for char_id in range(total_characters):
        url = f"{base_url}/{char_id}"
        response = requests.get(url)
        if response.status_code == 200:
            character_data = response.json()
            all_characters.append(character_data)
            print(f"✅ Fetched character ID {char_id}: {character_data.get('name', 'Unknown')}")
        else:
            print(f"⚠️ Failed to fetch character ID {char_id}: {response.status_code}")

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # Save to JSON file
    with open("data/characters.json", "w", encoding="utf-8") as f:
        json.dump(all_characters, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Saved {len(all_characters)} characters to data/characters.json")

if __name__ == "__main__":
    fetch_all_characters()
