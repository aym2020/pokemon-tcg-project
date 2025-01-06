from colorama import Fore
from pokemon_card_game.effects import *
from pokemon_card_game.gameplay import *

def misty_effect(target, opponent, logger=None):
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

def potion_effect(target, opponent, logger=None):
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

def pokeball_effect(player, opponent, logger=None):
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

def professors_research_effect(player, opponent, logger=None):
    """
    Draw 2 cards from the player's deck using the draw_cards utility.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"{player.name} plays Professor's Research to draw 2 cards.", color=Fore.CYAN)

    draw_cards(player, 2, logger)

def blaine_effect(player, opponent, logger=None):
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

def giovanni_effect(player, opponent, logger=None):
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

def blue_effect(player, opponent, logger=None):
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
    
def erika_effect(target, opponent, logger=None):
    """
    Heal 50 damage from the target Pokémon if it is of Grass type.
    :param target: The Pokémon to heal.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"Applying Erika effect to {target.name}.", color=Fore.CYAN)

    # Heal the target Pokémon
    heal_target(target, amount=50, logger=logger)

    # Log the result
    if logger:
        logger.log(f"Healed {target.name} by 50 HP. Current HP: {target.current_hp}/{target.hp}", color=Fore.GREEN)

def pokedex_effect(player, opponent, logger=None):
    """
    Look at the top 3 cards of the player's deck.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if not player.deck:
        if logger:
            logger.log(f"{player.name}'s deck is empty. Pokédex has no effect.", color=Fore.RED)
        return

    if logger:
        logger.log(f"{player.name} plays Pokédex to look at the top 3 cards of the deck.", color=Fore.CYAN)

    # Look at the top 5 cards
    top_3_cards = look_at_top_cards(player.deck, 3, logger)
    if logger:
        logger.log(f"Top 3 cards of the deck: {[card.name for card in top_3_cards]}", color=Fore.CYAN)

def mythical_slab_effect(player, opponent, logger=None):
    """
    Look at the top card of the player's deck.
    If it is a Psychic Pokémon, add it to their hand.
    If not, place it at the bottom of the deck.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if not player.deck:
        if logger:
            logger.log(f"{player.name}'s deck is empty. Mythical Slab has no effect.", color=Fore.RED)
        return

    # Look at the top card
    top_card = player.deck.pop(0)
    if logger:
        logger.log(f"Top card of the deck is {top_card.name}.", color=Fore.CYAN)

    if isinstance(top_card, PokemonCard) and top_card.type == "Psychic":
        player.hand.append(top_card)
        
        if logger:
            logger.log(f"{top_card.name} is a Psychic Pokémon and was added to {player.name}'s hand.", color=Fore.GREEN)
    else:
        player.deck.append(top_card)  # Place the card at the bottom of the deck
        if logger:
            logger.log(f"{top_card.name} is not a Psychic Pokémon and was placed at the bottom of the deck.", color=Fore.YELLOW)

def fossil_effect(player, object_card, logger=None):
    """
    Play an object card as a 40-HP Basic Colorless Pokémon.
    :param player: The Player object.
    :param object_card: The object card being played.
    :param logger: Logger instance to log messages.
    """
    # Create a new PokémonCard instance based on the object card
    fossil_pokemon = PokemonCard(
        name=object_card.name,  # Use the name of the object card
        type="Colorless",       # Colorless Pokémon
        hp=40,                  # 40 HP
        weakness=None,          # No specific weakness
        subcategory="Basic"     # Acts as a Basic Pokémon
    )
    
    # Play the Pokémon card
    player.play_pokemon(fossil_pokemon, logger)

    # Remove the object card from the player's hand
    if object_card in player.hand:
        player.hand.remove(object_card)
        if logger:
            logger.log(f"{player.name} played {object_card.name} as a 40-HP Colorless Pokémon.", color=Fore.CYAN)

def budding_expeditioner_effect(player, opponent, logger=None):
    """
    Put your Mew ex in the Active Spot into your hand.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    active_pokemon = player.active_pokemon

    # Check if the active Pokémon is Mew ex
    if active_pokemon and active_pokemon.name == "Mew ex":
        player.hand.append(active_pokemon)
        player.active_pokemon = None
        if logger:
            logger.log(f"{player.name} used Budding Expeditioner and returned Mew ex to their hand.", color=Fore.CYAN)
    else:
        if logger:
            logger.log(f"{player.name} cannot use Budding Expeditioner as Mew ex is not in the Active Spot.", color=Fore.RED)

def koga_effect(player, opponent, logger=None):
    """
    Put your Muk or Weezing in the Active Spot into your hand.
    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if player.active_pokemon and player.active_pokemon.name in ["Muk", "Weezing"]:
        pokemon = player.active_pokemon
        player.active_pokemon = None
        player.hand.append(pokemon)
        if logger:
            logger.log(f"{player.name} used Koga and returned {pokemon.name} from the Active Spot to their hand.", color=Fore.CYAN)
    else:
        if logger:
            logger.log(f"Koga cannot be used; the Active Pokémon is not Muk or Weezing.", color=Fore.RED)

def brock_effect(target, opponent, logger):
    """
    Directly attach a Fighting Energy to Golem or Onix, bypassing the energy zone.

    :param player: The Player object.
    :param logger: Logger instance to log messages.
    """
    if logger:
        logger.log(f"Applying Brock effect to {target.name}.", color=Fore.CYAN)

    # Attach generated energy based on the number of heads
    attach_energy_directly(target, "W", 1, logger)

def red_card_effect(player, opponent, logger=None):
    """
    Your opponent shuffles their hand into their deck and draws 3 cards.
    """
    if logger:
        logger.log(f"{player.name} uses Red Card! {opponent.name} shuffles their hand into the deck and draws 3 cards.", color=Fore.CYAN)
    
    # Shuffle opponent's hand into their deck
    opponent.deck.extend(opponent.hand)
    shuffle_deck(opponent.deck, logger)
    opponent.hand.clear()

    # Opponent draws 3 cards
    draw_cards(opponent, 3, logger)

# Mapping Trainer cards to their corresponding effects
object_effects = {
    "Misty": {
        "effect": misty_effect,
        "requires_target": True,
        "eligibility_check": True,
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
    "Erika": {
        "effect": erika_effect,
        "requires_target": True,
        "eligibility_check": True
    },
    "Pokédex": {
        "effect": pokedex_effect,
        "requires_target": False,
        "eligibility_check": False
    },
    "Mythical Slab": {
        "effect": mythical_slab_effect,
        "requires_target": False,
        "eligibility_check": False
    },
    "Dome Fossil": {
        "effect": fossil_effect,
        "requires_target": False,
        "eligibility_check": False
    },
    "Helix Fossil": {
        "effect": fossil_effect,
        "requires_target": False,
        "eligibility_check": False
    },
    "Old Amber": {
        "effect": fossil_effect,
        "requires_target": False,
        "eligibility_check": False
    },
    "Budding Expeditioner": {
        "effect": budding_expeditioner_effect,
        "requires_target": False,
        "eligibility_check": True
    },
    "Koga": {
        "effect": koga_effect,
        "requires_target": False,
        "eligibility_check": True
    },
    "Broke": {
        "effect": brock_effect,
        "requires_target": True,
        "eligibility_check": True
    },
    "Red Card": {
        "effect": red_card_effect,
        "requires_target": False,
        "eligibility_check": False  # Always eligible
    },

}