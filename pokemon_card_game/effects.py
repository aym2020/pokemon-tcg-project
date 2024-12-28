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


def flip_coins_until_tails(action, energy_type, target, logger):
    heads_count = 0
    while random.choice([True, False]):  # Heads = True, Tails = False
        heads_count += 1
        if logger:
            logger.log(f"Flip result: Heads ({heads_count}).", color=Fore.MAGENTA)
    if logger:
        logger.log(f"Flip result: Tails. Total heads: {heads_count}.", color=Fore.MAGENTA)

    if action == "attach_energy":
        target.energy[energy_type] = target.energy.get(energy_type, 0) + heads_count
        if logger:
            logger.log(f"{target.name} attached {heads_count} {energy_type} energy.", color=Fore.YELLOW)


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


def attach_energy_to_specific_pokemon(energy_zone, pokemon, energy_type, logger):
    if energy_zone.get(energy_type, 0) > 0:
        amount = 1
        energy_zone[energy_type] -= amount
        pokemon.energy[energy_type] = pokemon.energy.get(energy_type, 0) + amount
        if logger:
            logger.log(f"Attached {amount} {energy_type} energy to {pokemon.name}.", color=Fore.YELLOW)

def counter_attack(attacker, damage, logger):
    if attacker.is_active and attacker.is_damaged:
        attacker.current_hp = max(0, attacker.current_hp - damage)
        if logger:
            logger.log(f"{attacker.name} took {damage} damage.", color=Fore.MAGENTA)