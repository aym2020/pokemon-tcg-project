import unittest
from pokemon_card_game.card import PokemonCard, TrainerCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.player import Player
from pokemon_card_game.gameplay import perform_attack, attach_energy, evolve_pokemon
from pokemon_card_game.game import Game
from pokemon_card_game.ai import BasicAI
import random

"""
This test case tests the following features:
1. Check that the AI is able to evolve Pokémon during turn 0.
"""

class TestAI(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger and test Pokémon.
        """
        self.logger = Logger(verbose=False)
        
    def test_ai_prevent_evolution_during_turn_one(self):
        """
        Test that the AI does not attempt to evolve Pokémon during turn 1.
        """
        # Create Pokémon with attacks
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic", attacks=["30F"])
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1", attacks=["50FF"])
        bulbasaur = PokemonCard("Bulbasaur", "Grass", 60, "Fire", is_ex=False, subcategory="Basic", attacks=["20G"])
        
        # Create players and AI
        player1 = Player("Ash", [charmander, charmeleon], ["Fire"])
        player2 = Player("Gary", [bulbasaur], ["Grass"])
        player1.hand.append(charmeleon)  # Add Charmeleon to player1's hand
        player1.active_pokemon = charmander
        player2.active_pokemon = bulbasaur

        ai1 = BasicAI(player1, self.logger)
        ai2 = BasicAI(player2, self.logger)
        
        # Create game and set turn to 1
        game = Game(player1, player2, verbose=False, ai1=ai1, ai2=ai2)
        game.turn_count = 1  # Set to turn 1 to allow evolution

        # Simulate AI turn for player1
        ai1.play_turn(player2, game)
        
        # Check that Charmeleon is still in the hand and Charmander remains unevolved
        self.assertIn(charmeleon, player1.hand, "AI should not attempt to evolve Charmander during turn 1.")
        self.assertEqual(player1.active_pokemon, charmander, "Charmander should remain unevolved during turn 1.")
    
    def test_ai_prevent_attack_during_turn_one(self):
        """
        Test that the AI does not attempt to attack during turn 1.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"])
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"])
        
        # Create players and AI
        player = Player("Ash", [charmander], ["Fire"])
        opponent = Player("Gary", [squirtle], ["Water"])
        player.active_pokemon = charmander
        opponent.active_pokemon = squirtle

        ai = BasicAI(player, self.logger)
        
        # Create game and set turn to 1
        game = Game(player, opponent, verbose=False)
        game.turn_count = 1
        
        # Simulate AI turn
        ai.play_turn(opponent, game)
        
        # Validate no damage was dealt to the opponent
        self.assertEqual(opponent.active_pokemon.current_hp, squirtle.hp, "AI should not attempt to attack during turn 1.")
    
    def test_ai_allow_evolution_during_turn_two(self):
        """
        Test that the AI is able to evolve Pokémon during turn 2.
        """
        # Create Pokémon with attacks
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic", attacks=["30F"])
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1", attacks=["50FF"])
        bulbasaur = PokemonCard("Bulbasaur", "Grass", 60, "Fire", is_ex=False, subcategory="Basic", attacks=["20G"])
        
        # Create players and AI
        player1 = Player("Ash", [charmander, charmeleon], ["Fire"])
        player2 = Player("Gary", [bulbasaur], ["Grass"])
        player1.hand.append(charmeleon)  # Add Charmeleon to player1's hand
        player1.active_pokemon = charmander
        player2.active_pokemon = bulbasaur

        ai1 = BasicAI(player1, self.logger)
        ai2 = BasicAI(player2, self.logger)
        
        # Create game and set turn to 2
        game = Game(player1, player2, verbose=False, ai1=ai1, ai2=ai2)
        game.turn_count = 2  # Set to turn 2 to allow evolution

        # Simulate AI turn for player1
        ai1.play_turn(player2, game)
        
        # Check that Charmeleon is no longer in the hand and Charmander has evolved
        self.assertNotIn(charmeleon, player1.hand, "Charmeleon should no longer be in the hand after evolution.")
        self.assertEqual(player1.active_pokemon.name, "Charmeleon", "Charmander should have evolved into Charmeleon.")

    def test_ai_allow_attack_during_turn_two(self):
        """
        Test that the AI attempts to attack during turn 2 if possible.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"])
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"])
        
        # Create players and AI
        player = Player("Ash", [charmander], ["Fire"])
        opponent = Player("Gary", [squirtle], ["Water"])
        player.active_pokemon = charmander
        opponent.active_pokemon = squirtle

        ai = BasicAI(player, self.logger)
        
        # Create game and set turn to 2
        game = Game(player, opponent, verbose=False)
        game.turn_count = 2
        
        # Attach sufficient energy for Charmander's attack
        attach_energy(player.active_pokemon, "F", 1, self.logger)
        
        # Simulate AI turn
        ai.play_turn(opponent, game)
        
        # Validate damage was dealt to the opponent
        expected_hp = squirtle.hp - charmander.attacks[0].damage
        self.assertEqual(opponent.active_pokemon.current_hp, max(0, expected_hp), "AI should attempt to attack during turn 2.")
