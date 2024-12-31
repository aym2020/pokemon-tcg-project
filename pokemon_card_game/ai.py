from pokemon_card_game.card import PokemonCard, TrainerCard, ObjectCard
from pokemon_card_game.gameplay import perform_attack, attach_energy, generate_energy, evolve_pokemon
from pokemon_card_game.objects_effects import object_effects
from colorama import Fore

class BasicAI:
    def __init__(self, player, logger):
        self.player = player
        self.logger = logger

    def play_turn(self, opponent, game):
        """
        Execute the AI's turn logic, respecting game constraints.
        :param opponent: The opposing Player object.
        :param game: The Game instance for access to game state.
        """
        if game.turn_count == 0:
            self.logger.log(f"{self.player.name}'s first turn: No card draw, energy generation, or evolution allowed.", color=Fore.MAGENTA)
            
            # Play Pokémon if needed
            self.play_pokemon_if_needed()
            
            # Fill bench
            self.fill_bench()
            
            # Use Trainer or Object cards
            self.use_trainer_or_object(opponent)
            return

        # Play Pokémon if needed
        self.play_pokemon_if_needed()

        # Fill bench
        self.fill_bench()

        # Attempt evolution
        self.evolve_pokemon(game.turn_count)

        # Attach energy to the active Pokémon
        self.attach_energy_to_active()
        
        # Use Trainer or Object cards
        self.use_trainer_or_object(opponent)

        # Attack if possible
        self.attack(opponent, game)

    def play_pokemon_if_needed(self):
        """Set the active Pokémon if none exists."""
        if self.player.active_pokemon is None:
            for card in self.player.hand:
                if isinstance(card, PokemonCard) and not card.evolves_from:
                    self.player.play_pokemon(card, self.logger)
                    self.player.hand.remove(card)
                    break

    def fill_bench(self):
        """Fill the bench with available Pokémon."""
        for card in self.player.hand[:]:
            if isinstance(card, PokemonCard) and not card.evolves_from:
                if len(self.player.bench) < 3:
                    self.player.play_pokemon(card, self.logger)
                    self.player.hand.remove(card)

    def evolve_pokemon(self, turn_count):
        """Attempt to evolve Pokémon if possible."""
        for card in self.player.hand[:]:
            if isinstance(card, PokemonCard) and card.evolves_from:
                basic_pokemon = next(
                    (p for p in [self.player.active_pokemon] + self.player.bench if p and p.name == card.evolves_from),
                    None
                )
                if basic_pokemon:
                    evolve_pokemon(self.player, basic_pokemon, card, self.logger, turn_count)

    def attach_energy_to_active(self):
        """Attach energy to the active Pokémon if needed."""
        active = self.player.active_pokemon
        if active:
            for attack in active.attacks:
                missing_energy = {etype: attack.energy_required.get(etype, 0) - active.energy.get(etype, 0)
                                  for etype in attack.energy_required}
                for etype, amount in missing_energy.items():
                    if amount > 0 and etype in self.player.energy_colors:
                        attach_energy(active, etype, 1, self.logger)
                        break

    def attack(self, opponent, game):
        """
        Perform an attack if possible.
        :param opponent: The opposing Player object.
        :param game: The Game instance for access to turn count and rules.
        """
        if self.player.active_pokemon:
            perform_attack(self.player, opponent, self.logger, game)
    
    def use_trainer_or_object(self, opponent):
        """Play Trainer or Object cards if applicable."""
        for card in self.player.hand[:]:
            if isinstance(card, TrainerCard) or isinstance(card, ObjectCard):
                effect_info = object_effects.get(card.name)
                if effect_info:
                    effect = effect_info["effect"]
                    requires_target = effect_info["requires_target"]

                    if requires_target:
                        target = self.select_target_for_card(card)
                        if target:  # Only play the card if a valid target exists
                            effect(target, logger=self.logger)
                            self.player.hand.remove(card)
                    else:
                        # No target required, directly apply the effect
                        effect(self.player, logger=self.logger)
                        self.player.hand.remove(card)
                        
    def select_target_for_card(self, card):
        """
        Determine the appropriate target for a Trainer or Object card.
        :param card: The card being played.
        :return: The selected target Pokémon or None if no valid target exists.
        """
        if card.name == "Misty":
            # Ensure there is at least one Water Pokémon
            water_pokemon = [
                p for p in [self.player.active_pokemon] + self.player.bench
                if p and p.type == "Water"
            ]
            return self.ai_decision(water_pokemon) if water_pokemon else None

        elif card.name == "Potion":
            # Ensure there is at least one damaged Pokémon
            damaged_pokemon = [
                p for p in [self.player.active_pokemon] + self.player.bench
                if p and p.current_hp < p.hp
            ]
            return self.ai_decision(damaged_pokemon) if damaged_pokemon else None

        # Add other cards here as needed
        return None

    def ai_decision(self, pokemon_list):
        """
        AI logic to select a Pokémon from a list.
        Defaults to the first Pokémon if no complex logic is implemented.
        :param pokemon_list: List of Pokémon to choose from.
        :return: The selected Pokémon.
        """
        if not pokemon_list:
            return None
        # For now, simply pick the Pokémon with the lowest HP
        return min(pokemon_list, key=lambda p: p.current_hp)


