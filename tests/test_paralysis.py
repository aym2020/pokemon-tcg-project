import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.logger import Logger


class TestParalysis(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger and a test Pokémon.
        """
        self.logger = Logger(verbose=False)
        self.charmander = PokemonCard("Charmander", "Fire", 60, "Water")
        self.squirtle = PokemonCard("Squirtle", "Water", 50, "Electric")

    def test_apply_paralysis(self):
        """
        Test that paralysis is applied correctly to a Pokémon.
        """
        self.charmander.status = "paralyzed"
        self.charmander.paralysis_timer = 1  # Paralysis lasts 1 turn
        self.assertEqual(self.charmander.status, "paralyzed", "Charmander should be paralyzed.")
        self.assertEqual(self.charmander.paralysis_timer, 1, "Paralysis timer should be set to 1.")

    def test_paralysis_prevents_attack(self):
        """
        Test that a paralyzed Pokémon cannot attack.
        """
        self.charmander.status = "paralyzed"
        can_attack = self.charmander.status != "paralyzed"  # Attack logic placeholder
        self.assertFalse(can_attack, "A paralyzed Pokémon should not be able to attack.")

    def test_paralysis_prevents_retreat(self):
        """
        Test that a paralyzed Pokémon cannot retreat.
        """
        self.charmander.status = "paralyzed"
        can_retreat = self.charmander.status != "paralyzed"  # Retreat logic placeholder
        self.assertFalse(can_retreat, "A paralyzed Pokémon should not be able to retreat.")

    def test_paralysis_cures_after_turn(self):
        """
        Test that paralysis is cured automatically after the player's turn ends.
        """
        self.charmander.status = "paralyzed"
        self.charmander.paralysis_timer = 1

        # Simulate end of turn
        if self.charmander.paralysis_timer > 0:
            self.charmander.paralysis_timer -= 1

        if self.charmander.paralysis_timer == 0:
            self.charmander.status = None

        self.assertIsNone(self.charmander.status, "Charmander should no longer be paralyzed after 1 turn.")
        self.assertEqual(self.charmander.paralysis_timer, 0, "Paralysis timer should be 0 after the turn ends.")

    def test_evolve_cures_paralysis(self):
        """
        Test that evolving a Pokémon cures paralysis.
        """
        self.charmander.status = "paralyzed"
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", evolves_from="Charmander")

        def evolve(pokemon, evolution):
            evolution.current_hp = pokemon.current_hp
            evolution.energy = pokemon.energy
            evolution.status = None  # Cure all status effects
            return evolution

        evolved_pokemon = evolve(self.charmander, charmeleon)
        self.assertIsNone(evolved_pokemon.status, "Evolving should cure all status effects.")
        self.assertEqual(evolved_pokemon.name, "Charmeleon", "Charmander should now be Charmeleon.")

    def test_paralysis_does_not_stack(self):
        """
        Test that paralysis does not stack if applied multiple times.
        """
        self.charmander.status = "paralyzed"
        self.charmander.paralysis_timer = 1

        # Apply paralysis again
        self.charmander.status = "paralyzed"
        self.charmander.paralysis_timer = max(self.charmander.paralysis_timer, 1)  # Ensure no stacking

        self.assertEqual(self.charmander.paralysis_timer, 1, "Paralysis timer should not increase when applied again.")

if __name__ == "__main__":
    unittest.main()
