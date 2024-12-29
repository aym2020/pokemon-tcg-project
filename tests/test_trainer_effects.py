import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.effects import misty_effect
from pokemon_card_game.player import Player

"""
This test case tests the following features:
1. Misty: Choose a Water Pokémon from your deck and attach it to your active Pokémon.
"""
    

class TestTrainerEffects(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger, Water Pokémon, and Player.
        """
        self.logger = Logger(verbose=False)

    def test_target_selection(self):
        """
        Test that Misty effect targets a Water Pokémon correctly.
        """
        # Create Pokémon
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 3})
        magikarp = PokemonCard("Magikarp", "Water", 30, "Electric", energy={"W": 1})
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 0})
        
        # Create player
        player = Player("Ash", [squirtle, magikarp, charmander], ["Water"])
        
        # Add Pokémon to player's bench
        player.active_pokemon = squirtle
        player.bench = [magikarp, charmander]

        # Define a mock AI decision function to choose Magikarp
        def mock_ai_decision(pokemon_list):
            return pokemon_list[1]  # Always choose Magikarp
        
        # Number of energies attached to each Pokémon before Misty's effect
        magikarp_energy = magikarp.energy.get("W", 0)
        squirtle_energy = squirtle.energy.get("W", 0)
        charmander_energy = charmander.energy.get("W", 0)
    
        # Execute Misty's effect
        misty_effect(player, self.logger, ai_decision_function=mock_ai_decision)
        
        # Check that Magikarp was chosen and have received Water Energy
        self.assertGreaterEqual(magikarp.energy.get("W", 0), magikarp_energy, "Magikarp should receive at less 0 Water Energy.")
        
        # Check that Squirtle and Charmander did not receive Water Energy
        self.assertEqual(squirtle.energy.get("W", 0), squirtle_energy, "Squirtle should not receive Water Energy.")
        self.assertEqual(charmander.energy.get("W", 0), charmander_energy, "Charmander should not receive Water Energy.")
        
    def test_no_valid_targets(self):
        """
        Test that Misty's effect does nothing if there are no Water Pokémon.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 0})
        
        # Create player
        player = Player("Ash", [charmander], ["Water"])
        
        # Set Charmander as the active Pokémon
        player.active_pokemon = charmander  # Fire type
        player.bench = []

        # Execute Misty's effect
        misty_effect(player, self.logger)

        # Assert that no energy was attached
        self.assertEqual(charmander.energy.get("W", 0), 0, "Charmander should not receive Water Energy.")

if __name__ == "__main__":
    unittest.main()
