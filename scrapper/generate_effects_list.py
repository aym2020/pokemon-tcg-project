import json

def generate_effects_txt(json_file, output_txt):
    # Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        cards = json.load(f)

    # Separate effects into Pokémon and Trainer categories with card names
    pokemon_effects = {}  # Dictionary to map effects to Pokémon card names
    trainer_effects = {}  # Dictionary to map effects to Trainer card names

    for card in cards:
        if card["category"] == "Pokémon":
            # Add Pokémon effects (e.g., abilities or attack effects)
            if card["ability_effect"] != "N/A":
                pokemon_effects.setdefault(card["ability_effect"], []).append(card["name"])
            for attack in card["attacks"]:
                if attack["effect"] != "N/A":
                    pokemon_effects.setdefault(attack["effect"], []).append(card["name"])
        else:
            # Add Trainer card effects
            if card["effect"] != "N/A":
                trainer_effects.setdefault(card["effect"], []).append(card["name"])

    # Write to the output TXT file
    with open(output_txt, "w", encoding="utf-8") as f:
        # Write Pokémon effects
        f.write("Pokemon Effects:\n")
        if pokemon_effects:
            for effect, card_names in sorted(pokemon_effects.items()):  # Sort for readability
                f.write(f"- {effect} [Used by: {', '.join(sorted(card_names))}]\n")
        else:
            f.write("- No Pokémon effects found.\n")
        f.write("\n")

        # Write Trainer effects
        f.write("Trainer Effects:\n")
        if trainer_effects:
            for effect, card_names in sorted(trainer_effects.items()):  # Sort for readability
                f.write(f"- {effect} [Used by: {', '.join(sorted(card_names))}]\n")
        else:
            f.write("- No Trainer effects found.\n")

    print(f"Effects have been saved to '{output_txt}'")

# Example usage
generate_effects_txt("pokemon_cards.json", "effects_with_cards.txt")
