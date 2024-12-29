from pokemon_card_game.card import PokemonCard, TrainerCard, ObjectCard
from pokemon_card_game.gameplay import perform_attack, attach_energy, generate_energy
from pokemon_card_game.objects_effects import object_effects

class BasicAI:
    def __init__(self, player, logger):
        self.player = player
        self.logger = logger

    def play_turn(self, opponent, game):
        """
        Execute the AI's turn logic.
        :param opponent: The opposing Player object.
        """
        # Play Pokémon if needed
        if self.player.active_pokemon is None:
            self.play_active_pokemon()

        self.fill_bench()

        # Attach energy to the active Pokémon
        self.attach_energy_to_active()

        # Use Trainer or Object cards
        self.use_trainer_or_object(opponent)

        # Attack if possible
        self.attack(opponent, game)


    def play_active_pokemon(self):
        """Set the active Pokémon if none exists."""
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

    def use_trainer_or_object(self, opponent):
        """Play Trainer or Object cards if applicable."""
        for card in self.player.hand[:]:
            if isinstance(card, TrainerCard) or isinstance(card, ObjectCard):
                effect_function = object_effects.get(card.name)
                if effect_function:
                    effect_function(self.player, opponent, self.logger)
                    self.player.hand.remove(card)

    def attack(self, opponent, game):
        """Perform an attack if possible."""
        if self.player.active_pokemon:
            perform_attack(self.player, opponent, self.logger, game)  # Pass the game instance
