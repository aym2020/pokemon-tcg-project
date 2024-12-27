import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.player import Player
from pokemon_card_game.logger import Logger
from pokemon_card_game.effects import switch_opponent_pokemon

class TestEffects(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(verbose=False)
        self.active_pokemon = PokemonCard("Charmander", "Fire", 60, "Water")
        self.bench_pokemon_1 = PokemonCard("Squirtle", "Water", 50, "Electric")
        self.bench_pokemon_2 = PokemonCard("Bulbasaur", "Grass", 70, "Fire")

        self.opponent = Player("Gary", [], ["Fire", "Water"])
        self.opponent.active_pokemon = self.active_pokemon
        self.opponent.bench = [self.bench_pokemon_1, self.bench_pokemon_2]

    def test_switch_opponent_pokemon(self):
        """
        Test Sabrina's effect to switch the opponent's Active Pokémon.
        """
        switch_opponent_pokemon(self.opponent, self.logger)
        self.assertEqual(self.opponent.active_pokemon.name, "Squirtle", "The new Active Pokémon should be Squirtle.")
        self.assertIn(self.active_pokemon, self.opponent.bench, "Charmander should now be on the bench.")

    def test_no_switch_if_no_bench(self):
        """
        Test that no switch happens if the opponent has no Bench Pokémon.
        """
        self.opponent.bench = []  # Clear the bench
        switch_opponent_pokemon(self.opponent, self.logger)
        self.assertEqual(self.opponent.active_pokemon.name, "Charmander", "Active Pokémon should remain unchanged.")
