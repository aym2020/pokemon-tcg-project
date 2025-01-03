from pokemon_card_game.card import PokemonCard, TrainerCard, ObjectCard
from pokemon_card_game.gameplay import *
from pokemon_card_game.objects_effects import *
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
        if game.turn_count == 1:
            self.logger.log(f"{self.player.name}'s first turn: No card draw, energy generation, or evolution allowed.", color=Fore.MAGENTA)
            
            # Use Object cards (no limit)
            self.use_object_card()
            
            # Use Trainer card (only one per turn)
            self.use_trainer_card()
            
            # Play Pokémon if needed
            self.play_pokemon_if_needed()
            
            # Fill bench
            self.fill_bench()
            return

        # Draw a card at the start of the turn (except Turn 1)
        if game.turn_count > 1:
            self.draw_card()

        # Attempt evolution
        self.evolve_pokemon(game.turn_count)

        # Attach energy to the active Pokémon
        self.manage_energy_attachment()
        
        # Use Object cards (no limit)
        self.use_object_card()
        
        # Use Trainer card (only one per turn)
        self.use_trainer_card()
            
        # Play Pokémon if needed
        self.play_pokemon_if_needed()

        # Fill bench
        self.fill_bench()

        # Attack if possible
        self.attack(opponent, game)
    
    def draw_card(self):
        """Draw a card at the start of the AI's turn."""
        card = self.player.draw_card(self.logger)
        if card:
            self.logger.log(f"{self.player.name} drew {card.name}.", color=Fore.GREEN)

    def play_pokemon_if_needed(self):
        """Set the active Pokémon if none exists."""
        if self.player.active_pokemon is None:
            for card in self.player.hand[:]:
                # Check for a regular Pokémon card
                if isinstance(card, PokemonCard) and not card.evolves_from:
                    self.player.play_pokemon(card, self.logger)
                    self.player.hand.remove(card)
                    return  # Exit after playing a card
                
                # Check for a fossil card and play it as a Pokémon
                if card.name in ["Dome Fossil", "Helix Fossil", "Old Amber"]:
                    fossil_effect(self.player, card, logger=self.logger)
                    return  # Exit after playing a card

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
                        
    def manage_energy_attachment(self):
        """Manage energy attachment for the active Pokémon, its potential evolution, or bench Pokémon."""
        if self.player.active_pokemon:
            # Prioritize the active Pokémon and its evolution
            if self.attach_energy_to_active_or_evolution():
                return

        # Feed the bench if the active Pokémon doesn't need energy
        self.attach_energy_to_bench()
    
    def attach_energy_to_active_or_evolution(self):
        """
        Attach energy to the active Pokémon if needed.
        If the active Pokémon doesn't need energy, check its potential evolution.
        :return: True if energy was attached; False otherwise.
        """
        active = self.player.active_pokemon
        if not active:
            return False

        # Check if the active Pokémon needs energy for its current attacks
        for attack in active.attacks:
            if self.attach_missing_energy(active, attack):
                return True

        # Check if the active Pokémon's evolutions in the deck require energy
        evolutions, max_energy_required = self.get_evolution_and_max_energy_from_deck(active)
        for energy_type, required_amount in max_energy_required.items():
            missing_energy = required_amount - active.energy.get(energy_type, 0)
            if missing_energy > 0 and energy_type in self.player.energy_colors:
                attach_energy(active, energy_type, 1, self.logger)
                return True
        return False

    def get_evolution_and_max_energy_from_deck(self, pokemon):
        """
        Get all potential evolution cards for a Pokémon from the player's deck 
        and calculate the maximum energy required across all attacks.
        :param pokemon: The Pokémon to check for potential evolution.
        :return: A tuple (evolutions, max_energy_required).
        """
        evolutions = []
        max_energy_required = {}

        def collect_evolutions_and_energy(base_pokemon, deck):
            """Recursively collect evolution cards and calculate max energy requirements."""
            nonlocal max_energy_required

            for card in deck:
                if isinstance(card, PokemonCard) and card.evolves_from == base_pokemon.name:
                    evolutions.append(card)

                    # Update max energy requirements for this evolution stage
                    for attack in card.attacks:
                        for energy_type, amount in attack.energy_required.items():
                            max_energy_required[energy_type] = max(
                                max_energy_required.get(energy_type, 0), amount
                            )

                    # Continue searching for the next stage of evolution
                    collect_evolutions_and_energy(card, deck)

        # Start collecting evolutions and energy requirements
        collect_evolutions_and_energy(pokemon, self.player.deck)
        return evolutions, max_energy_required

    def attach_energy_to_bench(self):
        """Attach energy to Pokémon on the bench, prioritizing those with missing energy."""
        for pokemon in self.player.bench:
            for attack in pokemon.attacks:
                if self.attach_missing_energy(pokemon, attack):
                    return
    
    def attach_missing_energy(self, pokemon, attack):
        """
        Attach missing energy to a Pokémon for a given attack.
        :param pokemon: The Pokémon to attach energy to.
        :param attack: The attack being checked.
        :return: True if energy was attached; False otherwise.
        """
        missing_energy = {
            etype: attack.energy_required.get(etype, 0) - pokemon.energy.get(etype, 0)
            for etype in attack.energy_required
        }
        for etype, amount in missing_energy.items():
            if amount > 0 and etype in self.player.energy_colors:
                attach_energy(pokemon, etype, 1, self.logger)
                return True
        return False

    def attack(self, opponent, game):
        """
        Perform an attack if possible.
        :param opponent: The opposing Player object.
        :param game: The Game instance for access to turn count and rules.
        """
        if self.player.active_pokemon:
            perform_attack(self.player, opponent, self.logger, game)
    
    def use_trainer_card(self):
        """Play a single Trainer card if applicable."""
        if self.player.trainer_card_played:
            self.logger.log(f"{self.player.name} has already played a Trainer card this turn.", color=Fore.RED)
            return

        for card in self.player.hand[:]:
            if isinstance(card, TrainerCard):
                effect_info = object_effects.get(card.name)
                if effect_info:
                    effect = effect_info["effect"]
                    requires_target = effect_info["requires_target"]
                    eligibility_check = effect_info["eligibility_check"]

                    # Check eligibility if required
                    if eligibility_check and not self.is_card_eligible(card):
                        continue  # Skip the card if eligibility fails

                    if requires_target:
                        target = self.select_target_for_card(card)
                        if target:
                            effect(target, logger=self.logger)
                            self.player.hand.remove(card)
                            self.player.trainer_card_played = True
                            return  # Only one Trainer card allowed per turn
                    else:
                        effect(self.player, logger=self.logger)
                        self.player.hand.remove(card)
                        self.player.trainer_card_played = True
                        return  # Only one Trainer card allowed per turn

    def use_object_card(self):
        """Play Object cards, which have no limit on usage."""
        for card in self.player.hand[:]:
            if isinstance(card, ObjectCard):
                effect_info = object_effects.get(card.name)
                if effect_info:
                    effect = effect_info["effect"]
                    requires_target = effect_info["requires_target"]
                    eligibility_check = effect_info["eligibility_check"]

                    # Check eligibility if required
                    if eligibility_check and not self.is_card_eligible(card):
                        continue  # Skip the card if eligibility fails

                    if requires_target:
                        target = self.select_target_for_card(card)
                        if target:
                            effect(target, logger=self.logger)
                            self.player.hand.remove(card)
                    else:
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

        elif card.name == "Blaine":
            # Ensure there is at least one Ninetales, Rapidash, or Magmar
            eligible_pokemon = [
                p for p in [self.player.active_pokemon] + self.player.bench
                if p and p.name in ["Ninetales", "Rapidash", "Magmar"]
            ]
            return self.ai_decision(eligible_pokemon) if eligible_pokemon else None
    
        elif card.name == "Erika":
            # Select damaged Grass Pokémon
            damaged_grass_pokemon = [
            p for p in [self.player.active_pokemon] + self.player.bench
            if p.type == "Grass" and p.current_hp < p.hp
        ]
        return self.ai_decision(damaged_grass_pokemon) if damaged_grass_pokemon else None

        # Add other cards here as needed
        return None
    
    def is_card_eligible(self, card):
        """Determine if a card is eligible to be played."""
        if card.name == "Blaine":
            return any(
                p.name in ["Ninetales", "Rapidash", "Magmar"] for p in [self.player.active_pokemon] + self.player.bench
            )
        if card.name == "Misty":
            return any(
                p.type == "Water" for p in [self.player.active_pokemon] + self.player.bench
            )
        if card.name == "Potion":
            return any(
                p.current_hp < p.hp for p in [self.player.active_pokemon] + self.player.bench
            )
        if card.name == "Erika":
            return any(
            p.type == "Grass" and p.current_hp < p.hp for p in [self.player.active_pokemon] + self.player.bench
        )
        if card.name == "Budding Expeditioner":
            return self.player.active_pokemon and self.player.active_pokemon.name == "Mew ex"
        return True  # Default to eligible for cards without specific conditions

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


