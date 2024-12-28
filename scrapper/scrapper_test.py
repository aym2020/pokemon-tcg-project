import requests
from bs4 import BeautifulSoup

def scrape_pokemon_cards():
    url = "https://pocket.limitlesstcg.com/cards/P-A?display=text"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return
    else: 
        print("Successfully fetched the webpage")

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find cards on the page
    cards = soup.find_all("div", class_="card")  # Adjust the class name based on the website's structure
    for card in cards:
        if card.find("span", class_="card-text-name").text.strip() == "Potion":
            
            # Extract card details
            card_id = card.find("div", class_="card-set-info").text.strip()
            category_and_stage_and_evolution = card.find("p", class_="card-text-type").text.strip().split("-")
            category = category_and_stage_and_evolution[0].replace("Stage", "").strip()
            subcategory = category_and_stage_and_evolution[1].strip()
            name = card.find("span", class_="card-text-name").text.strip()
            
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
                if weakness_and_retreat:
                    weakness_and_retreat = weakness_and_retreat.text.strip().split(":")
                    weakness = weakness_and_retreat[1].split()[0].strip() if len(weakness_and_retreat) > 1 else "N/A"
                    retreat = weakness_and_retreat[2].strip() if len(weakness_and_retreat) > 2 else "N/A"
                else:
                    weakness = "N/A"
                    retreat = "N/A"
                
                # Extract attacks
                attack = card.find_all("div", class_="card-text-attack")
                attacks = []
                for a in attack:
                    attack_info = a.find("p", class_="card-text-attack-info").text.strip()
                    attack_parts = attack_info.split()
                    attack_name = " ".join(attack_parts[1:-1])
                    damage = attack_parts[-1]
                    energy_needed = a.find("span", class_="ptcg-symbol").text.strip()
                    attack_effect = a.find("p", class_="card-text-attack-effect")
                    
                    if attack_effect and attack_effect.text.strip():
                        attack_effect_parts = []
                        
                        for elem in attack_effect.children:
                            if elem.name == "span" and "data-tooltip" in elem.attrs:
                                # Replace the placeholder with the tooltip text (e.g., "G" -> "Grass")
                                attack_effect_parts.append(elem["data-tooltip"])
                            elif elem.name == "span" and "class" in elem.attrs and "copy-only" in elem["class"]:
                                continue  # Skip copy-only parts
                            elif elem.string:  # Add normal strings
                                attack_effect_parts.append(elem.string.strip())
                                
                        # Combine the effect text
                        attack_effect_text = " ".join(attack_effect_parts).strip()
                    else:
                        attack_effect_text = "N/A"
            
                    attacks.append({
                        "name": attack_name,
                        "damage": damage,
                        "energy_needed": energy_needed,
                        "effect": attack_effect_text
                    })
                
                # Set default values for Pokémon cards
                effect_text = "N/A"
                
            else:
                trainer_effects = card.find_all("div", class_="card-text-section")
                effect_parts = []
                for elem in trainer_effects[1].children:
                    if elem.name == "span" and "data-tooltip" in elem.attrs:
                        # Replace the placeholder with the tooltip text (e.g., "G" -> "Grass")
                        effect_parts.append(elem["data-tooltip"])
                    elif elem.name == "span" and "class" in elem.attrs and "copy-only" in elem["class"]:
                        continue  # Skip copy-only parts
                    elif elem.string:  # Add normal strings
                        effect_parts.append(elem.string.strip())
                        
                # Combine the effect text
                effect_text = " ".join(effect_parts).strip()
            
                # Set default values for non-Pokémon cards
                flag_ex = "N/A"
                hp = "N/A"
                pkmn_type = "N/A"
                evolve_from = "N/A"
                ability_name = "N/A"
                ability_effect = "N/A"
                weakness = "N/A"
                retreat = "N/A"
                attacks = []

            # Print the extracted data
            print(f"Card ID: {card_id}")
            print(f"Category: {category}")
            print(f"Subcategory: {subcategory}")
            print(f"Name: {name}")
            print(f"EX: {flag_ex}")
            print(f"HP: {hp}")
            print(f"Type: {pkmn_type}")
            print(f"Evolve From: {evolve_from}")
            print(f"Ability Name: {ability_name}")
            print(f"Ability Effect: {ability_effect}")
            print(f"Weakness: {weakness}")
            print(f"Retreat: {retreat}")
            for i, atk in enumerate(attacks, start=1):
                print(f"Attack {i}: {atk['name']}")
                print(f"Damage {i}: {atk['damage']}")
                print(f"Energy Needed {i}: {atk['energy_needed']}")
                print(f"Effect {i}: {atk['effect']}")
            print(f"Effect: {effect_text}")
            break
        else: continue
          
if __name__ == "__main__":
    scrape_pokemon_cards()
