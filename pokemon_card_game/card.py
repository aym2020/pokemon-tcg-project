from pokemon_card_game.attack import Attack
from colorama import Fore
import random

class Card:
    def __init__(self, name, card_category):
        """
        Base class for all cards.

        :param name: The name of the card.
        :param card_category: The category of the card (e.g., "Pokemon", "Trainer", "Object").
        """
        self.name = name
        self.card_category = card_category

    def __repr__(self):
        return f"{self.name} ({self.card_category})"

class PokemonCard(Card):
    def __init__(self, name, type, hp, weakness, is_ex=False, attacks=None, evolves_from=None, 
                 subcategory="Basic", energy=None, retreat=None, resistance=None, status=None, paralysis_timer=0):
        """
        Initialize a Pokémon card.

        :param subcategory: Indicates the Pokémon's stage (e.g., "Basic", "Stage 1", "Stage 2").
        """
        super().__init__(name, "Pokemon")
        self.type = type
        self.hp = hp
        self.current_hp = hp
        self.weakness = weakness
        self.is_ex = is_ex
        self.attacks = [Attack(attack) for attack in attacks] if attacks else []
        self.evolves_from = evolves_from
        self.subcategory = subcategory  # Basic, Stage 1, Stage 2
        self.energy = energy if energy else {}
        self.retreat = retreat
        self.resistance = resistance
        self.status = status
        self.paralysis_timer = paralysis_timer

    def apply_status_effects(self, logger):
        """
        Apply status effects in the correct order during the Control Phase.
        :param logger: Logger instance to log messages.
        """
        # Poison
        if self.status == "poisoned":
            self.current_hp = max(0, self.current_hp - 10)  # Apply poison damage
            logger.log(f"{self.name} is poisoned and took 10 damage. Current HP: {self.current_hp}/{self.hp}", color=Fore.MAGENTA)

        # Burn (not implemented yet)

        # Sleep
        elif self.status == "asleep":
            coin_toss = random.choice(["Heads", "Tails"])
            logger.log(f"{self.name} is asleep. Coin toss: {coin_toss}", color=Fore.CYAN)
            if coin_toss == "Heads":
                self.status = None
                logger.log(f"{self.name} woke up!", color=Fore.GREEN)

        # Paralysis
        elif self.status == "paralyzed":
            if self.paralysis_timer > 0:
                self.paralysis_timer -= 1
            if self.paralysis_timer == 0:
                self.status = None
                logger.log(f"{self.name} is no longer paralyzed.", color=Fore.GREEN)

    def cure_status(self):
        """
        Cure the Pokémon's status effects.
        """
        self.status = None
        self.paralysis_timer = 0

    def __repr__(self):
        return (f"{self.name} (Pokemon) - Type: {self.type}, HP: {self.current_hp}/{self.hp}, "
                f"Energy: {self.energy}, Weakness: {self.weakness}, EX: {self.is_ex}, "
                f"Evolves From: {self.evolves_from}, "
                f"Attacks: {[str(attack) for attack in self.attacks]}")

class TrainerCard(Card):
    def __init__(self, name, effect=None):
        """
        Initialize a Trainer card.

        :param name: The name of the Trainer card.
        :param effect: The effect of the Trainer card.
        """
        super().__init__(name, "Trainer")
        self.effect = effect

    def __repr__(self):
        return f"{self.name} (Trainer) - Effect: {self.effect}"

class ObjectCard(Card):
    def __init__(self, name, effect=None):
        """
        Initialize an Object card.

        :param name: The name of the Object card.
        :param effect: The effect of the Object card.
        """
        super().__init__(name, "Object")
        self.effect = effect

    def __repr__(self):
        return f"{self.name} (Object) - Effect: {self.effect}"

