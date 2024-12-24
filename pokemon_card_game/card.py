from .attack import Attack
from colorama import Fore

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
    def __init__(self, name, type, hp, weakness, is_ex=False, attacks=None, evolves_from=None):
        """
        Initialize a Pokémon card.

        :param type: The type of the Pokémon (e.g., "Fire").
        :param hp: The health points of the Pokémon.
        :param weakness: The type this Pokémon is weak to.
        :param is_ex: Whether the Pokémon is an EX Pokémon.
        :param attacks: A list of attack strings (e.g., ["60FCC"]).
        :param evolves_from: The name of the Pokémon this card evolves from (if any).
        """
        super().__init__(name, "Pokemon")
        self.type = type
        self.hp = hp
        self.weakness = weakness
        self.is_ex = is_ex
        self.current_hp = hp
        self.attacks = [Attack(attack) for attack in attacks] if attacks else []
        self.energy = {}  # Energy attached to this Pokémon
        self.evolves_from = evolves_from
        self.status = None  # New attribute for status effects (e.g., "poisoned", "asleep")

    def apply_status_effects(self, logger):
        """
        Apply status effects to the Pokémon at the end of the turn.
        :param logger: Logger instance to log messages.
        """
        if self.status == "poisoned":
            self.current_hp = max(0, self.current_hp - 10)  # Apply poison damage
            logger.log(f"{self.name} is poisoned and took 10 damage. Current HP: {self.current_hp}/{self.hp}", color=Fore.MAGENTA)

    def cure_status(self):
        """
        Cure the Pokémon's status effects.
        """
        self.status = None

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