import random 
from pokemon_card_game.card import PokemonCard
from colorama import Fore

class Player:
    def __init__(self, name, deck, energy_colors):
        self.name = name
        self.deck = deck
        self.hand = []
        self.active_pokemon = None
        self.bench = []
        self.discard_pile = []
        self.prizes = 0
        self.energy_colors = energy_colors
        self.newly_played_pokemons = []  # Track Pokémon played this turn
        self.newly_evolved_pokemons = [] # Track Pokémon evolved this turn
        self.trainer_card_played = False  # Tracks Trainer card usage

    def draw_card(self, logger):
        """
        Draw a card from the deck into the hand.

        :param logger: Logger instance to log messages.
        """
        if not self.deck:
            logger.log(f"{self.name} cannot draw a card; the deck is empty.", color=Fore.RED)
            return None
        card = self.deck.pop(0)
        self.hand.append(card)
        logger.log(f"{self.name} drew a card: {card.name}.", color=Fore.CYAN)
        return card

    def play_pokemon(self, pokemon_card, logger):
        """
        Play a Pokémon card to the active spot or bench.

        :param pokemon_card: A PokémonCard object.
        :param logger: Logger instance to log messages.
        """
        if self.active_pokemon is None:
            self.active_pokemon = pokemon_card
            logger.log(f"{self.name} played {pokemon_card.name} as the active Pokémon.", color=Fore.GREEN)
        elif len(self.bench) < 3:
            self.bench.append(pokemon_card)
            logger.log(f"{self.name} placed {pokemon_card.name} on the bench.", color=Fore.GREEN)
        else:
            logger.log(f"{self.name}'s bench is full! Cannot play {pokemon_card.name}.", color=Fore.RED)
            return

        # Append the played Pokémon to newly_played_pokemons
        self.newly_played_pokemons.append(pokemon_card)

    def generate_energy(self, logger):
        """
        Generate energy for this player.

        :param logger: Logger instance to log messages.
        :return: The generated energy type.
        """
        if len(self.energy_colors) == 1:
            energy = self.energy_colors[0]  # 100% chance for single color
        else:
            energy = random.choice(self.energy_colors)  # Randomly choose one color for multiple options
        logger.log(f"{self.name} generated {energy} energy.", color=Fore.YELLOW)
        return energy

    def generate_first_hand(self, logger):
        """
        Generate the player's first hand, ensuring it contains at least one basic Pokémon.

        :param logger: Logger instance to log messages.
        """
        basic_pokemon = None
        remaining_deck = []
        
        # Search for a basic Pokémon in the deck
        for card in self.deck:
            if isinstance(card, PokemonCard) and card.evolves_from is None:
                basic_pokemon = card
                break
            remaining_deck.append(card)

        if basic_pokemon:
            # Add the basic Pokémon to the hand
            self.hand.append(basic_pokemon)
            self.deck.remove(basic_pokemon)
            logger.log(f"{self.name} starts with a basic Pokémon: {basic_pokemon.name}.", color=Fore.GREEN)
        else:
            logger.log(f"{self.name} has no basic Pokémon in the deck! This shouldn't happen in a valid game.", color=Fore.RED)
            return

        # Draw the remaining 4 cards to complete the 5-card hand
        for _ in range(4):
            if self.deck:
                self.draw_card(logger)
            else:
                logger.log(f"{self.name}'s deck is empty while drawing the initial hand.", color=Fore.RED)

        logger.log(f"{self.name}'s initial hand: {[card.name for card in self.hand]}", color=Fore.CYAN)

    def retreat(self, new_active_pokemon, logger):
        """
        Retreat the current active Pokémon and replace it with another.

        :param new_active_pokemon: The PokémonCard instance to become active.
        :param logger: Logger instance to log messages.
        :return: True if the retreat was successful, False otherwise.
        """
        if self.active_pokemon is None:
            logger.log(f"{self.name} has no active Pokémon to retreat.", color=Fore.RED)
            return False

        if self.active_pokemon.status in ["asleep", "paralyzed"]:
            logger.log(f"{self.active_pokemon.name} is {self.active_pokemon.status} and cannot retreat!", color=Fore.RED)
            return False

        if new_active_pokemon not in self.bench:
            logger.log(f"{new_active_pokemon.name} is not on the bench and cannot become the active Pokémon.", color=Fore.RED)
            return False

        # Move current active Pokémon to the bench
        self.bench.append(self.active_pokemon)
        self.active_pokemon = new_active_pokemon
        self.bench.remove(new_active_pokemon)

        # Log successful retreat
        logger.log(f"{self.name} retreated {self.bench[-1].name} to the bench and sent out {self.active_pokemon.name}.", color=Fore.YELLOW)
        return True

    def clear_newly_played_and_evolved_pokemons(self):
        """Clear the list of newly played Pokémon at the end of the turn."""
        self.newly_played_pokemons.clear()
        self.newly_evolved_pokemons.clear()
    
    def reset_turn_flags(self):
        """Reset flags at the end of the turn."""
        self.trainer_card_played = False
    
    def clear_temporary_effects(self):
        """
        Clear temporary effects like damage reductions at the end of the turn.
        """
        for pokemon in [self.active_pokemon] + self.bench:
            if hasattr(pokemon, "damage_reduction"):
                pokemon.damage_reduction = 0  # Reset damage reduction
            if hasattr(pokemon, "damage_boost"):
                pokemon.damage_boost = 0  # Reset damage boost
            
    def __repr__(self):
        return (f"{self.name} - Active: {self.active_pokemon}, "
                f"Bench: {[p.name for p in self.bench]}, Hand: {[c.name for c in self.hand]}, "
                f"Prizes: {self.prizes}")
    

