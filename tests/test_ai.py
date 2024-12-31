import unittest
from pokemon_card_game.card import PokemonCard, TrainerCard, ObjectCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.player import Player
from pokemon_card_game.gameplay import *
from pokemon_card_game.game import Game
from pokemon_card_game.ai import BasicAI
import random

"""
This test case tests the following features:
1. Check that the AI is able to evolve Pokémon during turn 1.
2. Check that the AI is able to attack during turn 1.
3. Check that the AI is able to evolve Pokémon during turn 2.
4. Check that the AI is able to attack during turn 2.
5. Check that the AI uses Potion effect to heal a Pokémon.
6. Check that the AI does not use Potion effect if there are no Pokémon to heal.
7. Check that the AI uses Poké Ball effect to add a Pokémon to the player's hand.

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
        
    def test_ai_use_potion_effect(self):
        """
        Test that the AI uses Potion effect to heal a Pokémon.
        """
        # Create Pokémon
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 3})
        squirtle.current_hp = 30
        
        # Create player
        player = Player("Ash", [squirtle], ["Water"])
        
        # Set up active Pokémon
        player.active_pokemon = squirtle
        
        # Define the amount of HP before using Potion
        hp_before = squirtle.current_hp
        
        # Create Potion card
        potion = ObjectCard("Potion", "Heal 20 HP from the target Pokémon.")
        
        # Add Potion to player's hand
        player.hand.append(potion)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Potion effect
        ai.use_trainer_or_object(None)
        
        # Check that the Pokémon was healed
        self.assertGreater(squirtle.current_hp, hp_before, "Pokémon should be healed by Potion effect.")
    
    def test_ai_use_potion_effect_no_pokemon(self):
        """
        Test that the AI does not use Potion effect if there are no Pokémon to heal.
        """
        # Create player
        player = Player("Ash", [], ["Water"])
        
        # Create Potion card
        potion = ObjectCard("Potion", "Heal 20 HP from the target Pokémon.")
        
        # Add Potion to player's hand
        player.hand.append(potion)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Potion effect
        ai.use_trainer_or_object(None)
        
        # Check that the Potion was not used
        self.assertIn(potion, player.hand, "Potion should not be used if there are no Pokémon to heal.")
    
    def test_ai_use_pokeball_effect(self):
        """
        Test that the AI uses Poké Ball effect to add a Pokémon to the player's hand.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 1})
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 1})
                
        # Create player
        player = Player("Ash", [charmander, squirtle], ["Fire", "Water"])
        
        # Define the number of cards in the player's hand before using Poké Ball
        hand_size_before = len(player.hand)
        
        # Create Poké Ball card
        pokeball = ObjectCard("Poké Ball", "Find a random Basic Pokémon from the deck, add it to the player's hand, and shuffle the deck.")
        
        # Add Poké Ball to player's hand
        player.hand.append(pokeball)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Poké Ball effect
        ai.use_trainer_or_object(None)
        
        # Check that a Pokémon was added to the player's hand
        self.assertEqual(len(player.hand), hand_size_before + 1, "Poké Ball should add a Pokémon to the player's hand.")
