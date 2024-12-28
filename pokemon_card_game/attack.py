import re
from colorama import Fore
from attack_effects import deal_damage, discard_energy, apply_status_condition, heal_damage, flip_coins, modify_attack_damage

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

    def apply_effect(self, pokemon, logger=None):
        """
        Apply the special effect of the attack, if any.

        :param pokemon: The Pokémon on which the effect is applied.
        :param logger: Logger instance to log messages.
        """
        if self.effect_string:
            # Handle specific effects like discardEnergy or heal
            if "discardEnergy" in self.effect_string:
                match = re.match(r"discardEnergy\((\d+)([A-Z])\)", self.effect_string)
                if match:
                    amount = int(match.group(1))
                    energy_type = match.group(2)
                    discard_energy(pokemon, energy_type=energy_type, amount=amount, logger=logger)

            elif "heal" in self.effect_string:
                match = re.match(r"heal\((\d+)\)", self.effect_string)
                if match:
                    amount = int(match.group(1))
                    heal_damage(pokemon, amount=amount, logger=logger)

            elif "applyStatus" in self.effect_string:
                match = re.match(r"applyStatus\((\w+)\)", self.effect_string)
                if match:
                    status = match.group(1)
                    apply_status_condition(pokemon, condition=status, logger=logger)

            elif "flipCoins" in self.effect_string:
                match = re.match(r"flipCoins\((\d+),(\w+),(\d+)\)", self.effect_string)
                if match:
                    number_of_flips = int(match.group(1))
                    action_name = match.group(2)
                    amount = int(match.group(3))
                    if action_name == "dealDamage":
                        flip_coins(number_of_flips, deal_damage, target=pokemon, amount=amount, logger=logger)
                    elif action_name == "applyStatus":
                        flip_coins(number_of_flips, apply_status_condition, target=pokemon, condition="Paralyzed", logger=logger)

            elif "modifyDamage" in self.effect_string:
                match = re.match(r"modifyDamage\(([-\d+]+)\)", self.effect_string)
                if match:
                    modifier = int(match.group(1))
                    self.damage = modify_attack_damage(self.damage, modifier, logger=logger)

    def execute_attack(self, target, logger=None):
        """
        Execute the attack, dealing damage and applying effects.

        :param target: The target Pokémon to attack.
        :param logger: Logger instance to log messages.
        """
        # Deal damage
        deal_damage(target, self.damage, logger=logger)

        # Apply special effects
        self.apply_effect(target, logger=logger)

    def __repr__(self):
        return (f"Damage: {self.damage}, Energy: {self.energy_required}, "
                f"Effect: {self.effect_string or 'None'}")
