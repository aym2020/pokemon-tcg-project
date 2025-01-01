from colorama import Fore
from pokemon_card_game.effects import *

def misty_effect(target, logger=None):
    """
    Flip coins until tails and attach Water Energy for each heads to the target Pokémon.
    :param target: The Pokémon to receive the energy.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"Applying Misty effect to {target.name}.", color=Fore.CYAN)

    # Flip coins and count heads
    heads_count = flip_coins_until_tails(logger)

    # Attach generated energy based on the number of heads
    attach_energy_directly(target, "W", heads_count, logger)

def potion_effect(target, logger=None):
    """
    Heal 20 HP from the target Pokémon.
    :param target: The Pokémon to heal.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"Applying Potion effect to {target.name}.", color=Fore.CYAN)

    # Heal the target Pokémon
    heal_target(target, amount=20, logger=logger)

    # Log the result
    if logger:
        logger.log(f"Healed {target.name} by 20 HP. Current HP: {target.current_hp}/{target.hp}", color=Fore.GREEN)

def pokeball_effect(player, logger=None):
    """
    Find a random Basic Pokémon from the deck, add it to the player's hand, and shuffle the deck.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"{player.name} plays Poké Ball.", color=Fore.CYAN)

    # Find a random Basic Pokémon
    selected_pokemon = find_random_basic_pokemon(player.deck, logger)

    if not selected_pokemon:
        if logger:
            logger.log("Poké Ball has no effect as no Basic Pokémon was found.", color=Fore.RED)
        return

    # Add the selected Pokémon to the player's hand
    player.hand.append(selected_pokemon)
    if logger:
        logger.log(f"{selected_pokemon.name} was added to {player.name}'s hand.", color=Fore.GREEN)

    # Shuffle the remaining deck
    shuffle_deck(player.deck, logger)

def professors_research_effect(player, logger=None):
    """
    Draw 2 cards from the player's deck using the draw_cards utility.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"{player.name} plays Professor's Research to draw 2 cards.", color=Fore.CYAN)

    draw_cards(player, 2, logger)

def blaine_effect(player, logger=None):
    """
    During this turn, attacks used by your Ninetales, Rapidash, or Magmar do +30 damage to the opponent's Active Pokémon.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"{player.name} plays Blaine to boost damage for Ninetales, Rapidash, or Magmar.", color=Fore.CYAN)

    # Find Ninetales, Rapidash, and Magmar on the active spot and the bench
    for pokemon in [player.active_pokemon] + player.bench:
        if pokemon.name in ["Ninetales", "Rapidash", "Magmar"]:
            boost_attack_damage([pokemon], 30, logger)

def giovanni_effect(player, logger=None):
    """
    During this turn, attacks used by all of the player's Pokémon do +10 damage to the opponent's Active Pokémon.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"{player.name} plays Giovanni to boost damage for all Pokémon by 10.", color=Fore.CYAN)

    # Apply damage boost to all player's Pokémon
    for pokemon in [player.active_pokemon] + player.bench:
        if hasattr(pokemon, "damage_boost"):
            pokemon.damage_boost += 10  # Add +10 damage boost
            if logger:
                logger.log(f"{pokemon.name}'s attacks will do +10 damage this turn.", color=Fore.GREEN)

def blue_effect(player, logger=None):
    """
    During your opponent's next turn, all of your Pokémon take −10 damage from attacks.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"{player.name} plays Blue, reducing damage taken by all Pokémon by 10 during the opponent's next turn.", color=Fore.CYAN)

    # Apply damage reduction to all Pokémon
    for pokemon in [player.active_pokemon] + player.bench:
        if hasattr(pokemon, "damage_reduction"):
            pokemon.damage_reduction += 10  # Add a temporary reduction of 10
                
# Mapping Trainer cards to their corresponding effects
object_effects = {
    "Misty": {
        "effect": misty_effect,
        "requires_target": True,
        "eligibility_check": True
    },
    "Potion": {
        "effect": potion_effect,
        "requires_target": True,
        "eligibility_check": True
    },
    "Poké Ball": {
        "effect": pokeball_effect,
        "requires_target": False,
        "eligibility_check": False
    },
    "Professor's Research": {
        "effect": professors_research_effect,
        "requires_target": False,
        "eligibility_check": False
    },
    "Blaine": {
        "effect": blaine_effect,
        "requires_target": False,
        "eligibility_check": True
    },
        "Giovanni": {
        "effect": giovanni_effect,
        "requires_target": False,
        "eligibility_check": False  # Always eligible
    },
        "Blue": {
        "effect": blue_effect,
        "requires_target": False,
        "eligibility_check": False  # Always eligible
    },
}
