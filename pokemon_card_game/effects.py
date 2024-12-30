from colorama import Fore
import random

def heal_target(target, amount=20, logger=None):
    if hasattr(target, "current_hp") and hasattr(target, "hp"):
        previous_hp = target.current_hp
        target.current_hp = min(target.hp, target.current_hp + amount)
        healed_amount = target.current_hp - previous_hp
        if logger:
            logger.log(f"{target.name} was healed by {healed_amount} HP. Current HP: {target.current_hp}/{target.hp}", color=Fore.YELLOW)


def move_energy(source, target, energy_type, logger):
    if source.energy.get(energy_type, 0) > 0:
        amount = source.energy.pop(energy_type)
        target.energy[energy_type] = target.energy.get(energy_type, 0) + amount
        if logger:
            logger.log(f"Moved {amount} {energy_type} energy from {source.name} to {target.name}.", color=Fore.CYAN)


def switch_opponent_pokemon(opponent, logger):
    if not opponent.bench:
        if logger:
            logger.log(f"{opponent.name} has no Pokémon on the bench to switch with.", color=Fore.RED)
        return

    new_active_pokemon = opponent.bench[0]  # For simplicity, always choose the first Pokémon
    opponent.bench.append(opponent.active_pokemon)
    opponent.active_pokemon = new_active_pokemon
    opponent.bench.remove(new_active_pokemon)

    if logger:
        logger.log(f"{opponent.name} switched their Active Pokémon to {new_active_pokemon.name}.", color=Fore.GREEN)

def flip_coins_until_tails(logger=None):
    """
    Flip coins until tails and count the number of heads.
    :param logger: Logger instance to log messages.
    :return: Number of heads flipped.
    """
    heads_count = 0
    while random.choice([True, False]):  # Heads = True, Tails = False
        heads_count += 1
        if logger:
            logger.log(f"Flip result: Heads ({heads_count}).", color=Fore.MAGENTA)
    if logger:
        logger.log("Flip result: Tails.", color=Fore.MAGENTA)
    return heads_count

def attach_energy_directly(target, energy_type, amount, logger=None):
    """
    Attach a specified amount of energy directly to a Pokémon.
    :param target: The Pokémon to attach energy to.
    :param energy_type: The type of energy to attach.
    :param amount: The number of energy units to attach.
    :param logger: Logger instance to log messages.
    """
    for _ in range(amount):
        target.energy[energy_type] = target.energy.get(energy_type, 0) + 1
        if logger:
            logger.log(f"Attached 1 {energy_type} energy to {target.name}.", color=Fore.YELLOW)
        
def select_pokemon(pokemon_list, condition, active_pokemon=None, logger=None, ai_decision_function=None):
    """
    Select a Pokémon from the list based on a condition or AI decision.
    Prioritize the active Pokémon by default.
    :param pokemon_list: List of Pokémon to select from.
    :param condition: A callable to filter Pokémon.
    :param active_pokemon: The currently active Pokémon to prioritize.
    :param logger: Logger instance to log messages.
    :param ai_decision_function: Optional function for AI to choose a Pokémon.
    :return: The selected Pokémon or None if no valid Pokémon found.
    """
    # Check if the active Pokémon satisfies the condition
    if active_pokemon and condition(active_pokemon):
        if logger:
            logger.log(f"Selected Active Pokémon: {active_pokemon.name}.", color=Fore.CYAN)
        return active_pokemon

    # Otherwise, filter the bench Pokémon
    valid_pokemon = [p for p in pokemon_list if condition(p)]

    if not valid_pokemon:
        if logger:
            logger.log("No valid Pokémon found for selection.", color=Fore.RED)
        return None

    # Use AI decision function if provided, otherwise default to the first valid Pokémon
    selected_pokemon = ai_decision_function(valid_pokemon) if ai_decision_function else valid_pokemon[0]

    if logger:
        logger.log(f"Selected Pokémon: {selected_pokemon.name}.", color=Fore.CYAN)
    return selected_pokemon
 
def attach_energy_to_specific_pokemon(energy_zone, pokemon, energy_type, logger):
    if energy_zone.get(energy_type, 0) > 0:
        amount = 1
        energy_zone[energy_type] -= amount
        pokemon.energy[energy_type] = pokemon.energy.get(energy_type, 0) + amount
        if logger:
            logger.log(f"Attached {amount} {energy_type} energy to {pokemon.name}.", color=Fore.YELLOW)
            
def boost_attack_damage(targets, boost_amount, logger):
    for target in targets:
        if hasattr(target, "damage_boost"):
            target.damage_boost = target.damage_boost + boost_amount
            if logger:
                logger.log(f"{target.name}'s attacks will do +{boost_amount} damage this turn.", color=Fore.GREEN)

def play_as_pokemon(card, logger):
    card.is_played_as_pokemon = True
    if logger:
        logger.log(f"{card.name} is now played as a 40-HP Basic Colorless Pokémon.", color=Fore.CYAN)

def retrieve_to_hand(player, card_name, logger):
    for pokemon in [player.active_pokemon] + player.bench:
        if pokemon.name == card_name:
            player.hand.append(pokemon)
            if pokemon in player.bench:
                player.bench.remove(pokemon)
            else:
                player.active_pokemon = None
            if logger:
                logger.log(f"{pokemon.name} was retrieved to {player.name}'s hand.", color=Fore.CYAN)
            break

def counter_attack(attacker, damage, logger):
    if attacker.is_active and attacker.is_damaged:
        attacker.current_hp = max(0, attacker.current_hp - damage)
        if logger:
            logger.log(f"{attacker.name} took {damage} damage.", color=Fore.MAGENTA)