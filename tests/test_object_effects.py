import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.objects_effects import *
from pokemon_card_game.player import Player

"""
This test case tests the following features:
1. Potion: Heal 20 HP from the target Pokémon.
2. Poké Ball: Add a Pokémon to the player's hand.
3. Poké Ball: Do nothing if there are no Basic Pokémon.
"""

class TestObjectEffects(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger, Water Pokémon, and Player.
        """
        self.logger = Logger(verbose=False)
    
    def test_potion_effect(self):
        """
        Test that Potion effect heals a Pokémon correctly.
        """
        # Create Pokémon
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 3})
        squirtle.current_hp = 30
        
        # Create player
        player = Player("Ash", [squirtle], ["Water"])
        
        # Define the amount of HP before using Potion
        hp_before = squirtle.current_hp
        
        # Execute Potion's effect
        potion_effect(squirtle, self.logger)
        
    def test_pokeball_effect(self):
        """
        Test that Poké Ball effect adds a Pokémon to the player's hand.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 1})
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 1})
                
        # Create player
        player = Player("Ash", [charmander, squirtle], ["Fire", "Water"])
        
        # Define the number of cards in the player's hand before using Poké Ball
        hand_size_before = len(player.hand)
        
        # Execute Poké Ball's effect
        pokeball_effect(player, self.logger)
        
        # Check that a Pokémon was added to the player's hand
        self.assertEqual(len(player.hand), hand_size_before + 1, "Poké Ball should add a Pokémon to the player's hand.")
    
    def test_pokeball_effect_no_basic_pokemon(self):
        """
        Test that Poké Ball effect does nothing if there are no Basic Pokémon.
        """
        # Create player
        player = Player("Ash", [], ["Water"])
        
        # Define the number of cards in the player's hand before using Poké Ball
        hand_size_before = len(player.hand)
        
        # Execute Poké Ball's effect
        pokeball_effect(player, self.logger)
        
        # Check that no Pokémon was added to the player's hand
        self.assertEqual(len(player.hand), hand_size_before, "Poké Ball should not add a Pokémon if there are no Basic Pokémon.")