import re
from colorama import Fore

class Attack:
    def __init__(self, attack_string):
        """
        Parse an attack string and initialize attributes.

        :param attack_string: A string representing the attack (e.g., "60FCC", "200FFFF(discardEnergy(2F))").
        """
        # Initialize attributes
        self.damage = 0
        self.energy_required = {}
        self.effect_string = None

        # Parse damage
        match = re.match(r"(\d+)", attack_string)
        if match:
            self.damage = int(match.group(1))

        # Parse energy requirement (e.g., FCC or FFFF)
        energy_match = re.search(r"[A-Z]+", attack_string)
        if energy_match:
            for energy in energy_match.group(0):
                self.energy_required[energy] = self.energy_required.get(energy, 0) + 1

        # Parse special effect (e.g., discardEnergy(2F))
        effect_match = re.search(r"\((.*)\)", attack_string)
        if effect_match:
            self.effect_string = effect_match.group(1)


    def apply_effect(self, pokemon):
        """
        Apply the special effect of the attack, if any.

        :param pokemon: The Pokémon on which the effect is applied.
        """
        if self.effect_string:
            # Handle specific effects like discardEnergy
            if "discardEnergy" in self.effect_string:
                match = re.match(r"discardEnergy\((\d+)([A-Z])\)", self.effect_string)
                if match:
                    amount = int(match.group(1))
                    energy_type = match.group(2)
                    self.discard_energy(pokemon, energy_type, amount)


    def discard_energy(self, pokemon, energy_type, amount, logger=None):
        """
        Discard a specific amount of energy from the Pokémon.

        :param pokemon: The Pokémon card instance.
        :param energy_type: The type of energy to discard.
        :param amount: The amount of energy to discard.
        """
        if pokemon.energy.get(energy_type, 0) >= amount:
            pokemon.energy[energy_type] -= amount
            logger.log(f"{amount} {energy_type} energy discarded from {pokemon.name}.", color="magenta")
        else:
            logger.log(f"Not enough {energy_type} energy to discard from {pokemon.name}.", color="magenta")

    def __repr__(self):
        return (f"Damage: {self.damage}, Energy: {self.energy_required}, "
                f"Effect: {self.effect_string or 'None'}")
