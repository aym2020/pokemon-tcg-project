from colorama import Fore

def heal_target(target, amount=20, logger=None):
    """
    Heal a specified amount of HP for a target.

    :param target: The target object (e.g., a PokémonCard or Player).
    :param amount: The amount of HP or points to heal.
    :param logger: Logger instance to log the messages.
    """
    if hasattr(target, "current_hp") and hasattr(target, "hp"):
        previous_hp = target.current_hp
        target.current_hp = min(target.hp, target.current_hp + amount)
        healed_amount = target.current_hp - previous_hp
        logger.log(f"{target.name} was healed by {healed_amount} HP. Current HP: {target.current_hp}/{target.hp}", color=Fore.YELLOW)
    else:
        logger.log(f"{target.name} cannot be healed.", color=Fore.RED)

def shuffle_hand_and_draw(player, draw_count, logger):
    """
    Shuffle a player's hand into their deck and allow them to draw new cards.

    :param player: The Player object whose hand will be shuffled.
    :param draw_count: The number of cards the player will draw after shuffling.
    :param logger: Logger instance to log the messages.
    """
    logger.log(f"{player.name} shuffles their hand into their deck and draws {draw_count} cards.", color=Fore.YELLOW)
    player.deck.extend(player.hand)  # Add hand back to deck
    player.hand.clear()  # Clear the hand
    from random import shuffle
    shuffle(player.deck)  # Shuffle the deck
    logger.log(f"{player.name}'s hand has been shuffled back into their deck.", color=Fore.YELLOW)
    
    # Draw new cards
    for _ in range(draw_count):
        if player.deck:
            card = player.draw_card(logger)
            logger.log(f"{player.name} drew a card: {card.name}.", color=Fore.BLUE)
        else:
            logger.log(f"{player.name}'s deck is empty and cannot draw more cards.", color=Fore.RED)

def switch_opponent_pokemon(opponent, logger):
    """
    Force the opponent to switch their Active Pokémon with one from their Bench.
    The opponent chooses the new Active Pokémon.

    :param opponent: The Player object representing the opponent.
    :param logger: Logger instance to log messages.
    """
    if not opponent.bench:
        logger.log(f"{opponent.name} has no Pokémon on the bench to switch with.", color=Fore.RED)
        return

    # Log current state
    logger.log(f"{opponent.name} must switch their Active Pokémon.", color=Fore.YELLOW)
    logger.log(f"{opponent.name}'s Bench: {[pokemon.name for pokemon in opponent.bench]}", color=Fore.YELLOW)

    # Opponent chooses the new Active Pokémon (simulated here for simplicity)
    new_active_pokemon = opponent.bench[0]  # For now, always choose the first Pokémon

    # Switch the Pokémon
    opponent.bench.append(opponent.active_pokemon)  # Move active to the bench
    opponent.active_pokemon = new_active_pokemon
    opponent.bench.remove(new_active_pokemon)

    logger.log(f"{opponent.name} switched their Active Pokémon to {new_active_pokemon.name}.", color=Fore.GREEN)