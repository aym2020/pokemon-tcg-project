from .card import PokemonCard
import random
from colorama import Fore

def generate_energy(player, logger):
    """
    Generate energy for the player's active Pokémon based on their deck's energy colors.

    :param player: The Player object.
    :param logger: Logger instance to log messages.
    :return: The type of energy generated.
    """
    if len(player.energy_colors) == 1:
        energy = player.energy_colors[0]  # 100% chance for a single energy type
    else:
        energy = random.choice(player.energy_colors)  # Randomly choose one energy type
    logger.log(f"{player.name} generated {energy} energy.")
    return energy


def attach_energy(pokemon, energy_type, amount, logger):
    """
    Attach energy to a Pokémon.

    :param pokemon: The Pokémon card instance.
    :param energy_type: The type of energy to attach (e.g., 'F', 'C').
    :param amount: The number of energy units to attach.
    :param logger: Logger instance to log messages.
    """
    if hasattr(pokemon, "energy"):
        pokemon.energy[energy_type] = pokemon.energy.get(energy_type, 0) + amount
        logger.log(f"{amount} {energy_type} energy attached to {pokemon.name}.")
    else:
        logger.log(f"{pokemon.name} cannot have energy attached.", color="red")


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


def handle_knockout(attacker, defender, attacking_player, defending_player, logger):
    """
    Handle a knockout event.

    :param attacker: The attacking Pokémon.
    :param defender: The defending Pokémon.
    :param attacking_player: The Player object whose Pokémon made the knockout.
    :param defending_player: The Player object whose Pokémon was knocked out.
    :param logger: Logger instance to log messages.
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
        defending_player.active_pokemon = defending_player.bench.pop(0)
        logger.log(f"{defending_player.name} moved {defending_player.active_pokemon.name} from the bench to active.")
    else:
        # No bench Pokémon, defending player loses
        logger.critical(f"{defending_player.name} has no more Pokémon! {attacking_player.name} wins the game!")
        exit()  # End the game


def perform_attack(attacking_player, defending_player, logger):
    """
    Perform an attack during the current player's turn.

    :param attacking_player: The Player object whose Pokémon is attacking.
    :param defending_player: The Player object whose Pokémon is defending.
    :param logger: Logger instance to log messages.
    """
    attacker = attacking_player.active_pokemon
    defender = defending_player.active_pokemon

    if not attacker or not defender:
        logger.log("Both players must have active Pokémon to perform an attack!", color="red")
        return

    # Select the first attack for simplicity
    attack = attacker.attacks[0]

    # Calculate damage
    damage = calculate_damage(attack, attacker, defender, logger)

    # Apply damage
    defender.current_hp = max(0, defender.current_hp - damage)
    logger.log(f"{attacker.name} used {attack.damage}! {defender.name} took {damage} damage. Current HP: {defender.current_hp}/{defender.hp}")

    # Check for knockout
    if defender.current_hp == 0:
        handle_knockout(attacker, defender, attacking_player, defending_player, logger)


def evolve_pokemon(player, basic_pokemon, evolution_card, logger):
    """
    Evolve a basic Pokémon into its evolution.

    :param player: The Player object performing the evolution.
    :param basic_pokemon: The basic Pokémon being evolved.
    :param evolution_card: The Evolution Pokémon card being played.
    :param logger: Logger instance to log messages.
    """
    if not evolution_card.evolves_from or evolution_card.evolves_from != basic_pokemon.name:
        logger.log(f"{evolution_card.name} cannot evolve from {basic_pokemon.name}.", color="red")
        return False

    # Transfer damage and energy
    evolution_card.current_hp = evolution_card.hp - (basic_pokemon.hp - basic_pokemon.current_hp)
    evolution_card.energy = basic_pokemon.energy.copy()

    # Replace the basic Pokémon
    if player.active_pokemon == basic_pokemon:
        player.active_pokemon = evolution_card
        logger.log(f"{player.name} evolved their Active Pokémon {basic_pokemon.name} into {evolution_card.name}.")
    elif basic_pokemon in player.bench:
        index = player.bench.index(basic_pokemon)
        player.bench[index] = evolution_card
        logger.log(f"{player.name} evolved Bench Pokémon {basic_pokemon.name} into {evolution_card.name}.")
    else:
        logger.log(f"{basic_pokemon.name} is not in play and cannot be evolved.", color="red")
        return False

    # Remove the evolution card from the player's hand
    player.hand.remove(evolution_card)
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

