from pokemon_card_game.card import PokemonCard
import random
from colorama import Fore

def generate_energy(player, logger):
    """
    Generate energy for the player's active Pokémon based on their deck's energy colors.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    :return: The type of energy generated.
    """
    if not player.energy_colors:
        logger.log(f"{player.name} has no energy colors defined.", color=Fore.RED)
        return None
    
    if len(player.energy_colors) == 1:
        energy = player.energy_colors[0]  # Single energy type
    else:
        energy = random.choice(player.energy_colors)  # Random choice for multiple types
    
    player.energy_zone.append(energy[0])  # Add the first letter of the energy type to the energy zone
    logger.log(f"{player.name} generated {energy} energy.", color=Fore.YELLOW)
    return energy

def attach_energy(player, pokemon, logger, energy_type=None):
    """
    Attach energy from the player's energy zone to a Pokémon.
    :param player: The Player object.
    :param pokemon: The Pokémon to attach energy to.
    :param logger: Logger instance to log messages.
    :param energy_type: The specific type of energy to attach (optional).
    :return: True if energy was attached, False otherwise.
    """
    if not player.energy_zone:
        logger.log(f"{player.name} has no energy in the energy zone.", color=Fore.RED)
        return False

    # If energy_type is specified, check if it exists in the energy zone
    if energy_type:
        if energy_type not in player.energy_zone:
            logger.log(f"{player.name} does not have {energy_type} energy in the energy zone.", color=Fore.RED)
            return False
        player.energy_zone.remove(energy_type)
    else:
        # Use the first energy in the energy zone by default
        energy_type = player.energy_zone.pop(0)

    # Attach the energy to the Pokémon
    pokemon.energy[energy_type] = pokemon.energy.get(energy_type, 0) + 1
    logger.log(f"{player.name} attached 1 {energy_type} energy to {pokemon.name}.", color=Fore.GREEN)
    return True

def refill_energy_zone(player, logger):
    """
    Refill the player's energy zone at the start of their turn.

    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    while len(player.energy_zone) < 2:
        generate_energy(player, logger)

def calculate_damage(attack, attacker, defender, logger):
    """
    Calculate the damage dealt by an attack.

    :param attack: The Attack object used by the attacker.
    :param attacker: The attacking Pokémon.
    :param defender: The defending Pokémon.
    :param logger: Logger instance to log messages.
    :return: The calculated damage.
    """
    damage = attack.damage
    if defender.weakness == attacker.type:
        damage += 20  # Apply weakness bonus
        logger.log(f"{attacker.name}'s attack exploits {defender.name}'s weakness! +20 damage.")
    return damage

def handle_knockout(attacker, defender, attacking_player, defending_player, logger, game):
    """
    Handle a knockout event.

    :param attacker: The attacking Pokémon.
    :param defender: The defending Pokémon.
    :param attacking_player: The Player object whose Pokémon made the knockout.
    :param defending_player: The Player object whose Pokémon was knocked out.
    :param logger: Logger instance to log messages.
    :param game: The Game object to update the game state.
    """
    logger.log(f"{defender.name} was knocked out!")
    points = 2 if defender.is_ex else 1
    attacking_player.prizes += points
    logger.log(f"{attacking_player.name} earned {points} point(s)!")
    
    # Move the knocked-out Pokémon to the discard pile
    defending_player.discard_pile.append(defender)
    defending_player.active_pokemon = None
    
    # Check if defending player has bench Pokémon
    if defending_player.bench:
        new_active = defending_player.bench.pop(0)
        new_active.current_hp = new_active.hp  # Reset HP to max
        defending_player.active_pokemon = new_active
        logger.log(f"{defending_player.name} moved {new_active.name} from the bench to active.")
    else:
        # No bench Pokémon, defending player loses
        logger.critical(f"{defending_player.name} has no more Pokémon! {attacking_player.name} wins the game!")
        game.end_game(attacking_player.name)

def has_sufficient_energy(attacker, attack, logger):
    """
    Check if the attacking Pokémon has sufficient energy to perform the attack.

    :param attacker: The attacking Pokémon.
    :param attack: The Attack object.
    :param logger: Logger instance to log messages.
    :return: True if the attacker has sufficient energy, False otherwise.
    """
    for energy_type, required_amount in attack.energy_required.items():
        if attacker.energy.get(energy_type, 0) < required_amount:
            logger.log(f"{attacker.name} does not have enough {energy_type} energy to perform {attack.damage} damage.", color=Fore.RED)
            return False
    return True

def perform_attack(attacking_player, defending_player, logger, game):
    """
    Perform an attack during the current player's turn.

    :param attacking_player: The Player object whose Pokémon is attacking.
    :param defending_player: The Player object whose Pokémon is defending.
    :param logger: Logger instance to log messages.
    """
    attacker = attacking_player.active_pokemon
    defender = defending_player.active_pokemon

    if not attacker or not defender:
        logger.log("Both players must have active Pokémon to perform an attack!", color=Fore.RED)
        return

    # Select the first attack for simplicity
    attack = attacker.attacks[0]

    # Validate energy requirements
    if not has_sufficient_energy(attacker, attack, logger):
        return  # Skip the attack if energy is insufficient
        
    # Execute the attack
    attack.execute_attack(attacker, defender, logger)
    
    # Check for knockout
    if defender.current_hp == 0:
        handle_knockout(attacker, defender, attacking_player, defending_player, logger, game)

def evolve_pokemon(player, basic_pokemon, evolution_card, logger, turn_count):
    """
    Evolve a basic Pokémon into its evolution.

    :param player: The Player object performing the evolution.
    :param basic_pokemon: The basic Pokémon being evolved.
    :param evolution_card: The Evolution Pokémon card being played.
    :param logger: Logger instance to log messages.
    :param turn_count: The current turn count to enforce first-turn restrictions.
    """
    # Prevent evolution during the first turn
    if turn_count <= 1:
        logger.log(f"{basic_pokemon.name} cannot evolve during the first turn.", color=Fore.RED)
        return False

    # Check if the evolution hierarchy is correct
    if evolution_card.subcategory == "Stage 1" and basic_pokemon.subcategory != "Basic":
        logger.log(f"{evolution_card.name} can only evolve from a Basic Pokémon.", color=Fore.RED)
        return False
    if evolution_card.subcategory == "Stage 2" and basic_pokemon.subcategory != "Stage 1":
        logger.log(f"{evolution_card.name} can only evolve from a Stage 1 Pokémon.", color=Fore.RED)
        return False

    # Check if evolution_card lists the correct pre-evolution
    if not evolution_card.evolves_from or evolution_card.evolves_from != basic_pokemon.name:
        logger.log(f"{evolution_card.name} cannot evolve from {basic_pokemon.name}.", color=Fore.RED)
        return False

    # Prevent evolution for Pokémon that evolved this turn
    if basic_pokemon in player.newly_evolved_pokemons:
        logger.log(f"{basic_pokemon.name} has already evolved this turn and cannot evolve again.", color=Fore.RED)
        return False

    # Prevent evolution on the same turn a Pokémon is played
    if basic_pokemon in player.newly_played_pokemons:
        logger.log(f"{basic_pokemon.name} cannot evolve this turn; it was just played.", color=Fore.RED)
        return False

    # Transfer damage and energy
    evolution_card.current_hp = evolution_card.hp - (basic_pokemon.hp - basic_pokemon.current_hp)
    evolution_card.energy = basic_pokemon.energy.copy()

    # Replace the basic Pokémon
    if player.active_pokemon == basic_pokemon:
        player.active_pokemon = evolution_card
        logger.log(f"{player.name} evolved their Active Pokémon {basic_pokemon.name} into {evolution_card.name}.", color=Fore.GREEN)
    elif basic_pokemon in player.bench:
        index = player.bench.index(basic_pokemon)
        player.bench[index] = evolution_card
        logger.log(f"{player.name} evolved Bench Pokémon {basic_pokemon.name} into {evolution_card.name}.", color=Fore.GREEN)
    else:
        logger.log(f"{basic_pokemon.name} is not in play and cannot be evolved.", color=Fore.RED)
        return False

    # Remove status effects
    evolution_card.status = None
    logger.log(f"{basic_pokemon.name}'s status conditions have been healed by evolution.", color=Fore.CYAN)

    # Remove the evolution card from the player's hand
    player.hand.remove(evolution_card)

    # Track the newly evolved Pokémon
    player.newly_evolved_pokemons.append(evolution_card)
    return True

def apply_poison(pokemon, logger):
    """
    Apply poison status to a Pokémon.
    :param pokemon: The PokémonCard instance to poison.
    :param logger: Logger instance to log messages.
    """
    if pokemon.status != "poisoned":
        pokemon.status = "poisoned"
        logger.log(f"{pokemon.name} is now poisoned!", color=Fore.MAGENTA)

def apply_sleep(pokemon, logger):
    """
    Apply sleep status to a Pokémon.
    :param pokemon: The PokémonCard instance to put to sleep.
    :param logger: Logger instance to log messages.
    """
    if pokemon.status != "asleep":
        pokemon.status = "asleep"
        logger.log(f"{pokemon.name} is now asleep!", color=Fore.MAGENTA)
