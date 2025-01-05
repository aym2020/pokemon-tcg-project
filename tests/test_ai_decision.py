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
1. AI decision for Misty card.
2. AI decision for Potion card.
3. AI decision for Brock card.
"""
class TestAIDecision(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger and test Pokémon.
        """
        self.logger = Logger(verbose=False)
        
    def test_ai_decision_misty(self):
        """
        Test AI decision for Misty card.
        """
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 2}, attacks=["10W"])
        magikarp = PokemonCard("Magikarp", "Water", 30, "Electric", energy={"W": 1}, attacks=["20W"])
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 1}, attacks=["30F"])
        gyarados = PokemonCard("Gyarados", "Water", 130, "Electric", evolves_from="Magikarp", attacks=["140WWWW"])

        # Add Pokémon to the field
        player = Player("Ash", [squirtle, magikarp, charmander, gyarados], energy_colors=["W"])
        player.active_pokemon = squirtle
        player.bench = [magikarp, charmander]

        # AI decision for Misty card
        misty = TrainerCard("Misty")
        ai = BasicAI(player, self.logger)
        target = ai.ai_decision(misty, [squirtle, magikarp, charmander])

        self.assertEqual(target, magikarp, "AI should choose Magikarp with less Water energy.")

    def test_ai_decision_potion(self):
        """
        Test AI decision for Potion card.
        """
        # Create Pokémon
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric")
        charmander = PokemonCard("Charmander", "Fire", 60, "Water")
        
        # Set HP for each Pokémon
        squirtle.current_hp = 30
        charmander.current_hp = 20

        # Add Pokémon to the field
        player = Player("Ash", [squirtle, charmander], energy_colors=["W"])
        player.active_pokemon = squirtle
        player.bench = [charmander]

        # AI decision for Potion card
        potion = TrainerCard("Potion")
        ai = BasicAI(player, self.logger)
        target = ai.ai_decision(potion, [squirtle, charmander])

        self.assertEqual(target, charmander, "AI should choose Charmander with the least HP.")

    def test_ai_decision_brock(self):
        """
        Test AI decision for Brock card.
        """
        golem = PokemonCard("Golem", "Rock", 120, "Grass")
        onix = PokemonCard("Onix", "Rock", 100, "Grass")
        charmander = PokemonCard("Charmander", "Fire", 60, "Water")

        # Add Pokémon to the field
        player = Player("Ash", [golem, onix, charmander], energy_colors=["F"])
        player.active_pokemon = golem
        player.bench = [onix, charmander]

        # AI decision for Brock card
        brock = TrainerCard("Brock")
        ai = BasicAI(player, self.logger)
        target = ai.ai_decision(brock, [golem, onix, charmander])

        self.assertEqual(target, golem, "AI should choose Golem or Onix for Brock's effect.")

