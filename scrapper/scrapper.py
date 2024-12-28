import requests
from bs4 import BeautifulSoup
import json

def scrape_pokemon_cards(urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    all_card_data = []

    for url in urls:
        # Send GET request
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch the webpage {url}. Status code: {response.status_code}")
            continue
        else:
            print(f"Successfully fetched the webpage {url}")

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Initialize a list to store card data
        card_data = []

        # Find cards on the page
        cards = soup.find_all("div", class_="card")  # Adjust the class name based on the website's structure
        for card in cards:
            try:
                # Common fields
                card_id = card.find("div", class_="card-set-info").text.strip()
                category_and_stage_and_evolution = card.find("p", class_="card-text-type").text.strip().split("-")
                category = category_and_stage_and_evolution[0].strip()
                subcategory = category_and_stage_and_evolution[1].strip()
                name = card.find("span", class_="card-text-name").text.strip()

                # Pokémon Cards
                if category == "Pokémon":
                    flag_ex = True if "ex" in name else False
                    hp_and_type = card.find("p", class_="card-text-title").text.strip().split("-")
                    hp = hp_and_type[2].split()[0].strip()
                    pkmn_type = hp_and_type[1].strip()
                    evolve_from = category_and_stage_and_evolution[2].replace("Evolves from", "").strip() if len(category_and_stage_and_evolution) > 2 else "N/A"
                    
                    # Extract ability
                    ability_info = card.find("p", class_="card-text-ability-info")
                    ability_name = ability_info.text.strip() if ability_info else "N/A"
                    ability_effect = card.find("p", class_="card-text-ability-effect")
                    ability_effect = ability_effect.text.strip() if ability_effect else "N/A"
                    
                    # Extract weakness and retreat
                    weakness_and_retreat = card.find("p", class_="card-text-wrr")
                    if (weakness_and_retreat):
                        weakness_and_retreat = weakness_and_retreat.text.strip().split(":")
                        weakness = weakness_and_retreat[1].split()[0].strip() if len(weakness_and_retreat) > 1 else "N/A"
                        retreat = weakness_and_retreat[2].strip() if len(weakness_and_retreat) > 2 else "N/A"
                    else:
                        weakness = "N/A"
                        retreat = "N/A"

                    # Extract attacks
                    attack_sections = card.find_all("div", class_="card-text-attack")
                    attacks = []
                    for a in attack_sections:
                        attack_info = a.find("p", class_="card-text-attack-info").text.strip()
                        attack_parts = attack_info.split()
                        attack_name = " ".join(attack_parts[1:-1])
                        damage = attack_parts[-1]
                        energy_needed = a.find("span", class_="ptcg-symbol").text.strip()
                        attack_effect_section = a.find("p", class_="card-text-attack-effect")
                        
                        if attack_effect_section and attack_effect_section.text.strip():
                            effect_parts = []
                            for elem in attack_effect_section.children:
                                if elem.name == "span" and "data-tooltip" in elem.attrs:
                                    effect_parts.append(elem["data-tooltip"])
                                elif elem.name == "span" and "class" in elem.attrs and "copy-only" in elem["class"]:
                                    continue
                                elif elem.string:
                                    effect_parts.append(elem.string.strip())
                            attack_effect_text = " ".join(effect_parts).strip()
                        else:
                            attack_effect_text = "N/A"

                        attacks.append({
                            "name": attack_name,
                            "damage": damage,
                            "energy_needed": energy_needed,
                            "effect": attack_effect_text
                        })

                    card_data.append({
                        "card_id": card_id,
                        "category": category,
                        "subcategory": subcategory,
                        "name": name,
                        "is_ex": flag_ex,
                        "hp": hp,
                        "type": pkmn_type,
                        "evolve_from": evolve_from,
                        "ability_name": ability_name,
                        "ability_effect": ability_effect,
                        "weakness": weakness,
                        "retreat": retreat,
                        "attacks": attacks,
                        "effect": "N/A"  # Pokémon cards do not have a generic effect
                    })

                # Trainer Cards
                else:
                    trainer_effects = card.find_all("div", class_="card-text-section")
                    effect_parts = []
                    for elem in trainer_effects[1].children:
                        if elem.name == "span" and "data-tooltip" in elem.attrs:
                            effect_parts.append(elem["data-tooltip"])
                        elif elem.name == "span" and "class" in elem.attrs and "copy-only" in elem["class"]:
                            continue
                        elif elem.string:
                            effect_parts.append(elem.string.strip())
                    effect_text = " ".join(effect_parts).strip()

                    card_data.append({
                        "card_id": card_id,
                        "category": category,
                        "subcategory": subcategory,
                        "name": name,
                        "is_ex": "N/A",
                        "hp": "N/A",
                        "type": "N/A",
                        "evolve_from": "N/A",
                        "ability_name": "N/A",
                        "ability_effect": "N/A",
                        "weakness": "N/A",
                        "retreat": "N/A",
                        "attacks": [],
                        "effect": effect_text
                    })

            except Exception as e:
                print(f"Failed to parse card: {e}")

        all_card_data.extend(card_data)

    # Save to JSON file
    with open("pokemon_cards.json", "w", encoding="utf-8") as json_file:
        json.dump(all_card_data, json_file, ensure_ascii=False, indent=4)

    print(f"Saved {len(all_card_data)} Pokémon cards to 'pokemon_cards.json'")

if __name__ == "__main__":
    urls = [
        "https://pocket.limitlesstcg.com/cards/A1?display=text",
        "https://pocket.limitlesstcg.com/cards/A1a?display=text",
        "https://pocket.limitlesstcg.com/cards/P-A?display=text"
    ]
    scrape_pokemon_cards(urls)
