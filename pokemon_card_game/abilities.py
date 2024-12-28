from colorama import Fore

class Ability:
    """
    Represents an ability of a Pokémon card.
    """
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def apply(self, pokemon, game_state, logger=None):
        """
        Apply the ability effect. Each ability is handled uniquely.

        :param pokemon: The Pokémon with the ability.
        :param game_state: The current game state for context.
        :param logger: Logger instance to log messages.
        """
        if logger:
            logger.log(f"Applying ability: {self.name} for {pokemon.name}", color=Fore.CYAN)

        # Handle abilities
        if self.name == "Rough Skin":
            self._rough_skin(pokemon, game_state, logger)
        elif self.name == "Primeval Law":
            self._primeval_law(game_state, logger)
        elif self.name == "Wash Out":
            self._wash_out(pokemon, game_state, logger)
        elif self.name == "Jungle Totem":
            self._jungle_totem(game_state, logger)
        elif self.name == "Data Scan":
            self._data_scan(game_state, logger)
        elif self.name == "Drive Off":
            self._drive_off(game_state, logger)
        elif self.name == "Hard Coat":
            self._hard_coat(pokemon, logger)
        elif self.name == "Gas Leak":
            self._gas_leak(pokemon, game_state, logger)
        elif self.name == "Psy Shadow":
            self._psy_shadow(game_state, logger)
        elif self.name == "Sleep Pendulum":
            self._sleep_pendulum(game_state, logger)
        elif self.name == "Shadowy Spellbind":
            self._shadowy_spellbind(game_state, logger)
        elif self.name == "Volt Charge":
            self._volt_charge(pokemon, game_state, logger)
        elif self.name == "Water Shuriken":
            self._water_shuriken(game_state, logger)
        elif self.name == "Shell Armor":
            self._shell_armor(pokemon, logger)
        elif self.name == "Counterattack":
            self._counterattack(pokemon, game_state, logger)
        elif self.name == "Fragrance Trap":
            self._fragrance_trap(game_state, logger)
        elif self.name == "Powder Heal":
            self._powder_heal(game_state, logger)

    def _rough_skin(self, pokemon, game_state, logger):
        if pokemon.is_active and pokemon.is_damaged:
            attacker = game_state.last_attacking_pokemon
            if attacker:
                attacker.current_hp = max(0, attacker.current_hp - 20)
                if logger:
                    logger.log(f"Rough Skin: {attacker.name} took 20 damage.", color=Fore.MAGENTA)

    def _primeval_law(self, game_state, logger):
        game_state.prevent_evolution = True
        if logger:
            logger.log("Primeval Law: Opponent can't evolve their Active Pokémon.", color=Fore.YELLOW)

    def _wash_out(self, pokemon, game_state, logger):
        if logger:
            logger.log("Wash Out: Move 1 Water Energy to Active Pokémon.", color=Fore.CYAN)
        # Implement logic to move energy

    def _jungle_totem(self, game_state, logger):
        game_state.energy_multiplier = 2
        if logger:
            logger.log("Jungle Totem: Grass Energy now provides 2 energy each.", color=Fore.GREEN)

    def _data_scan(self, game_state, logger):
        if logger:
            logger.log("Data Scan: Looked at the top card of the deck.", color=Fore.BLUE)
        # Implement deck peeking logic

    def _drive_off(self, game_state, logger):
        if game_state.opponent_bench:
            if logger:
                logger.log("Drive Off: Switch opponent's Active Pokémon.", color=Fore.YELLOW)
        # Implement opponent switch logic

    def _hard_coat(self, pokemon, logger):
        pokemon.damage_reduction += 20
        if logger:
            logger.log("Hard Coat: Pokémon takes -20 damage.", color=Fore.GREEN)

    def _gas_leak(self, pokemon, game_state, logger):
        if pokemon.is_active:
            game_state.opponent_active_pokemon.apply_status("Poisoned", logger=logger)

    def _psy_shadow(self, game_state, logger):
        if logger:
            logger.log("Psy Shadow: Attached Psychic Energy to Active Pokémon.", color=Fore.MAGENTA)
        # Implement energy attachment logic

    def _sleep_pendulum(self, game_state, logger):
        if logger:
            logger.log("Sleep Pendulum: Flip a coin for Sleep.", color=Fore.YELLOW)
        # Implement coin flip for sleep

    def _shadowy_spellbind(self, game_state, logger):
        game_state.prevent_supporter_cards = True
        if logger:
            logger.log("Shadowy Spellbind: Opponent can't use Supporter cards.", color=Fore.RED)

    def _volt_charge(self, pokemon, game_state, logger):
        if logger:
            logger.log("Volt Charge: Attached Lightning Energy to Pokémon.", color=Fore.YELLOW)
        # Implement energy attachment logic

    def _water_shuriken(self, game_state, logger):
        if logger:
            logger.log("Water Shuriken: Deal 20 damage to 1 opponent's Pokémon.", color=Fore.BLUE)
        # Implement targeted damage logic

    def _shell_armor(self, pokemon, logger):
        pokemon.damage_reduction += 10
        if logger:
            logger.log("Shell Armor: Pokémon takes -10 damage.", color=Fore.GREEN)

    def _counterattack(self, pokemon, game_state, logger):
        if pokemon.is_active and pokemon.is_damaged:
            attacker = game_state.last_attacking_pokemon
            if attacker:
                attacker.current_hp = max(0, attacker.current_hp - 20)
                if logger:
                    logger.log(f"Counterattack: {attacker.name} took 20 damage.", color=Fore.MAGENTA)

    def _fragrance_trap(self, game_state, logger):
        if logger:
            logger.log("Fragrance Trap: Switch in opponent's Benched Basic Pokémon.", color=Fore.YELLOW)
        # Implement switch logic

    def _powder_heal(self, game_state, logger):
        if logger:
            logger.log("Powder Heal: Healed 20 damage from each Pokémon.", color=Fore.GREEN)
        # Implement healing logic for all Pokémon
