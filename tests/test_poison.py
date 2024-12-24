import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.gameplay import apply_poison

class TestPoisonMechanics(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment.
        """
        self.logger = Logger(verbose=False)  # Silent logger for tests
        self.charmander = PokemonCard("Charmander", "Fire", 60, "Water")

    def test_apply_poison(self):
        """
        Test applying poison to a Pokémon.
        """
        apply_poison(self.charmander, self.logger)
        self.assertEqual(self.charmander.status, "poisoned", "Charmander should be poisoned.")

    def test_poison_damage(self):
        """
        Test poison damage at the end of the turn.
        """
        self.charmander.status = "poisoned"
        self.charmander.apply_status_effects(self.logger)
        self.assertEqual(self.charmander.current_hp, 50, "Charmander should take 10 damage from poison.")

    def test_cure_poison(self):
        """
        Test curing poison by evolving or retreating.
        """
        self.charmander.status = "poisoned"
        self.charmander.cure_status()
        self.assertIsNone(self.charmander.status, "Charmander should no longer be poisoned.")
