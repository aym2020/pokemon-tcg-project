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

# Mapping Trainer cards to their corresponding effects
object_effects = {
    "Misty": {
        "effect": misty_effect,
        "requires_target": True
    },
    "Potion": {
        "effect": potion_effect,
        "requires_target": True
    },
    "Poké Ball": {
        "effect": pokeball_effect,
        "requires_target": False
    },
}