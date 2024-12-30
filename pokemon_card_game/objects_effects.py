from colorama import Fore
from pokemon_card_game.effects import (
    heal_target,
    move_energy,
    switch_opponent_pokemon,
    flip_coins_until_tails,
    boost_attack_damage,
    play_as_pokemon,
    retrieve_to_hand,
    attach_energy_to_specific_pokemon,
    attach_energy_directly,
    select_pokemon,
)

# Mapping Trainer cards to their corresponding effects
object_effects = {
    "Misty": lambda player, logger: misty_effect(
        player,
        logger=logger
    ),
    "Potion": lambda player, logger: potion_effect(
        player,
        logger=logger
    ),
}

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
