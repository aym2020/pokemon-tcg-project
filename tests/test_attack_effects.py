import unittest
from pokemon_card_game.card import PokemonCard, TrainerCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.player import Player
from pokemon_card_game.gameplay import perform_attack, attach_energy, evolve_pokemon
from pokemon_card_game.game import Game
import random

"""
This test case tests the following features:
1. 200FFFF(discardOwnEnergy(2F)): 200 damage. Discard 2 Fire Energy attached to Charizard.
"""

class TestAttackEffects(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger and test Pokémon.
        """
        self.logger = Logger(verbose=False)
    
    def test_attack_effects_discard_energy(self):
        """
        Test that attack effects are correctly applied.
        """
        # Create Pokémon
        charizard = PokemonCard("Charizard", "Fire", 200, "Water", is_ex=False, attacks=["200FFFF(discardOwnEnergy(2F))"], energy={"F": 4})
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"], energy={"W": 2})
        pikachu = PokemonCard("Pikachu", "Electric", 40, "Fighting", is_ex=False, attacks=["20CC"])
                
        # Create players
        player1 = Player("Ash", [charizard], ["Fire"])
        player2 = Player("Gary", [squirtle], ["Water"])
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set the game to a random turn between 2 and 100
        game.turn_count = random.randint(2, 100)
            
        # Set active Pokémon for each player 
        player1.active_pokemon = charizard
        player2.active_pokemon = squirtle
        
        # Set bench Pokémon for player 2
        player2.bench = [pikachu]
              
        # Simulate fight
        perform_attack(player1, player2, self.logger, game)
        
        # Check if the attack was successful
        self.assertEqual(squirtle.current_hp, 0, "Squirtle should have 0 HP.")

        # Check the number of Fire Energy attached to Charizard
        self.assertEqual(charizard.energy["F"], 2, "Charizard should have 2 Fire Energy.")

if __name__ == '__main__':
    unittest.main()
