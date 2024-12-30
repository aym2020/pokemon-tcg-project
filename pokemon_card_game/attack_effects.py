from random import randint, choice
from colorama import Fore

# Attack effects
def deal_damage(target, amount, logger=None):
    """
    Deal damage to a target.

    :param target: The target Pokémon to receive damage.
    :param amount: The amount of damage to deal.
    :param logger: Logger instance to log the message.
    """
    if hasattr(target, "current_hp"):
        target.current_hp = max(0, target.current_hp - amount)
        if logger:
            logger.log(f"{target.name} took {amount} damage. Current HP: {target.current_hp}/{target.hp}", color=Fore.RED)

def heal_damage(target, amount, logger=None):
    """
    Heal damage from a target.

    :param target: The Pokémon to heal.
    :param amount: The amount of HP to restore.
    :param logger: Logger instance to log the message.
    """
    if hasattr(target, "current_hp") and hasattr(target, "hp"):
        previous_hp = target.current_hp
        target.current_hp = min(target.hp, target.current_hp + amount)
        healed_amount = target.current_hp - previous_hp
        if logger:
            logger.log(f"{target.name} was healed by {healed_amount} HP. Current HP: {target.current_hp}/{target.hp}", color=Fore.GREEN)

def discard_energy(source, energy_type=None, amount=1, logger=None):
    """
    Discard energy from a Pokémon.

    :param source: The Pokémon to discard energy from.
    :param energy_type: The type of energy to discard (or None for any).
    :param amount: The amount of energy to discard.
    :param logger: Logger instance to log the message.
    """
    if hasattr(source, "energy"):
        discarded = 0
        if energy_type:
            if energy_type in source.energy:
                discarded = min(amount, source.energy[energy_type])
                source.energy[energy_type] -= discarded
                if source.energy[energy_type] == 0:
                    del source.energy[energy_type]
        else:
            for etype in list(source.energy.keys()):
                if discarded >= amount:
                    break
                to_discard = min(amount - discarded, source.energy[etype])
                discarded += to_discard
                source.energy[etype] -= to_discard
                if source.energy[etype] == 0:
                    del source.energy[etype]
        if logger:
            logger.log(f"{source.name} discarded {discarded} {energy_type if energy_type else 'energy'}.", color=Fore.MAGENTA)

def flip_coins(number_of_flips, action, **kwargs):
    """
    Flip coins and perform an action based on heads count.

    :param number_of_flips: Number of coins to flip.
    :param action: The action to perform with heads count (e.g., deal_damage, heal_damage).
    :param kwargs: Additional arguments for the action.
    :return: Number of heads flipped.
    """
    heads_count = 0
    for _ in range(number_of_flips):
        if choice([True, False]):  # Heads = True
            heads_count += 1
    if "logger" in kwargs:
        kwargs["logger"].log(f"Flipped {heads_count}/{number_of_flips} heads.", color=Fore.YELLOW)
    if callable(action):
        action(heads_count, **kwargs)
    return heads_count

def modify_attack_damage(base_damage, modifier, condition=None, logger=None):
    """
    Modify attack damage based on a condition.

    :param base_damage: The base damage of the attack.
    :param modifier: The amount to modify the damage (positive or negative).
    :param condition: A callable to check if the condition is met (or None for unconditional).
    :param logger: Logger instance to log the message.
    :return: The modified damage.
    """
    if condition is None or condition():
        modified_damage = base_damage + modifier
        if logger:
            logger.log(f"Attack damage modified by {modifier}. New damage: {modified_damage}", color=Fore.BLUE)
        return modified_damage
    return base_damage

def apply_status_condition(target, condition, logger=None):
    """
    Apply a status condition to a target.

    :param target: The Pokémon to apply the condition to.
    :param condition: The status condition to apply (e.g., "Poisoned", "Asleep").
    :param logger: Logger instance to log the message.
    """
    if hasattr(target, "status"):
        target.status = condition
        if logger:
            logger.log(f"{target.name} is now {condition}.", color=Fore.MAGENTA)