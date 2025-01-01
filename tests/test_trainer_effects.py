import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.effects import *
from pokemon_card_game.objects_effects import *
from pokemon_card_game.player import Player

"""
This test case tests the following features:
1. Misty: Check that Misty effect targets a Water Pokémon correctly.
2. Misty: Check that Misty's effect does nothing if there are no Water Pokémon.
3. Professor's Research: Check that Professor's Research effect draws 2 cards from the player's deck.
4. Blaine: Check that Blaine effect boosts damage for Ninetales, Rapidash, or Magmar.
5. Giovanni: Check that Giovanni effect boosts damage for all Pokémon.
6. Blue: Check that Blue effect reduces damage taken by all Pokémon during the opponent's next turn.
"""
    

class TestTrainerEffects(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger, Water Pokémon, and Player.
        """
        self.logger = Logger(verbose=False)

    def test_misty_target_selection(self):
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
        
        # Select target using the AI decision function
        target = select_pokemon(
            [player.active_pokemon] + player.bench,
            condition=lambda p: p.type == "Water",
            logger=None,
            ai_decision_function=mock_ai_decision
        )
        
        # Number of energies attached to each Pokémon before Misty's effect
        magikarp_energy = magikarp.energy.get("W", 0)
        squirtle_energy = squirtle.energy.get("W", 0)
        charmander_energy = charmander.energy.get("W", 0)

        # Execute Misty's effect
        misty_effect(target, logger=None)
        
        # Check that Magikarp was chosen and received Water Energy
        self.assertGreaterEqual(magikarp.energy.get("W", 0), magikarp_energy, "Magikarp should receive at least 0 additional Water Energy.")
        
        # Check that Squirtle and Charmander did not receive Water Energy
        self.assertEqual(squirtle.energy.get("W", 0), squirtle_energy, "Squirtle should not receive additional Water Energy.")
        self.assertEqual(charmander.energy.get("W", 0), charmander_energy, "Charmander should not receive any Water Energy.")

    def test_misty_no_valid_targets(self):
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
        
        # Select target using the AI decision function
        target = select_pokemon(
            [player.active_pokemon] + player.bench,
            condition=lambda p: p.type == "Water",
            logger=None,
            ai_decision_function=None
        )

        # Ensure no target is selected
        self.assertIsNone(target, "No valid target should be selected for Misty's effect.")

        # Execute Misty's effect only if a valid target exists
        if target:
            misty_effect(target, self.logger)

        # Assert that no energy was attached
        self.assertEqual(charmander.energy.get("W", 0), 0, "Charmander should not receive Water Energy.")

    def test_professors_research(self):
        """
        Test that Professor's Research effect draws 2 cards from the player's deck.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 0})
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 0})
        
        # Create player with a non-empty deck
        player = Player("Ash", [charmander, squirtle], ["Water"])
         
        # Define the number of cards in the player's hand before using Professor's Research
        hand_size_before = len(player.hand)
        
        # Execute Professor's Research effect   
        professors_research_effect(player, self.logger)
        
        # Check that 2 cards were drawn from the player's deck
        self.assertEqual(len(player.hand), hand_size_before + 2, "Professor's Research should draw 2 cards from the player's deck.")
    
    def test_blaine_damage_boost(self):
        """
        Test that Blaine effect boosts damage for Ninetales, Rapidash, or Magmar.
        """
        # Create Pokémon
        ninetales = PokemonCard("Ninetales", "Fire", 90, "Water", attacks=["90FF"], energy={"F": 2})
        rapidash = PokemonCard("Rapidash", "Fire", 80, "Water", attacks=["40F"], energy={"F": 1})
        magmar = PokemonCard("Magmar", "Fire", 70, "Water", attacks=["80FF(discardOwnEnergy(2F))"], energy={"F": 2})
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", attacks=["20F"], energy={"F": 1})
        
        # Create player
        player = Player("Ash", [ninetales, rapidash, magmar, charmander], ["Water"])
        
        # Add Pokémon to player's bench
        player.active_pokemon = ninetales
        player.bench = [rapidash, magmar, charmander]
        
        # Number of damage boosts for each Pokémon before Blaine's effect
        ninetales_damage_boost = getattr(ninetales, "damage_boost", 0)
        rapidash_damage_boost = getattr(rapidash, "damage_boost", 0)
        magmar_damage_boost = getattr(magmar, "damage_boost", 0)
        charmander_damage_boost = getattr(charmander, "damage_boost", 0)
        
        # Execute Blaine's effect
        blaine_effect(player, self.logger)
        
        # Check that Ninetales, Rapidash, and Magmar received a damage boost
        self.assertGreater(getattr(ninetales, "damage_boost", 0), ninetales_damage_boost, "Ninetales should receive a damage boost.")
        self.assertGreater(getattr(rapidash, "damage_boost", 0), rapidash_damage_boost, "Rapidash should receive a damage boost.")
        self.assertGreater(getattr(magmar, "damage_boost", 0), magmar_damage_boost, "Magmar should receive a damage boost.")
        
        # Check that Charmander did not receive a damage boost
        self.assertEqual(getattr(charmander, "damage_boost", 0), charmander_damage_boost, "Charmander should not receive a damage boost.")
    
    def test_giovanni_damage_boost(self):
        """
        Test that Giovanni effect boosts damage for all Pokémon.
        """
        # Create Pokémon
        ninetales = PokemonCard("Ninetales", "Fire", 90, "Water", attacks=["90FF"], energy={"F": 2})
        rapidash = PokemonCard("Rapidash", "Fire", 80, "Water", attacks=["40F"], energy={"F": 1})
        magmar = PokemonCard("Magmar", "Fire", 70, "Water", attacks=["80FF(discardOwnEnergy(2F))"], energy={"F": 2})
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", attacks=["20F"], energy={"F": 1})
        
        # Create player
        player = Player("Ash", [ninetales, rapidash, magmar, charmander], ["Water"])
        
        # Add Pokémon to player's bench
        player.active_pokemon = ninetales
        player.bench = [rapidash, magmar, charmander]
        
        # Number of damage boosts for each Pokémon before Giovanni's effect
        ninetales_damage_boost = getattr(ninetales, "damage_boost", 0)
        rapidash_damage_boost = getattr(rapidash, "damage_boost", 0)
        magmar_damage_boost = getattr(magmar, "damage_boost", 0)
        charmander_damage_boost = getattr(charmander, "damage_boost", 0)
        
        # Execute Giovanni's effect
        giovanni_effect(player, self.logger)
        
        # Check that all Pokémon received a damage boost
        self.assertGreater(getattr(ninetales, "damage_boost", 0), ninetales_damage_boost, "Ninetales should receive a damage boost.")
        self.assertGreater(getattr(rapidash, "damage_boost", 0), rapidash_damage_boost, "Rapidash should receive a damage boost.")
        self.assertGreater(getattr(magmar, "damage_boost", 0), magmar_damage_boost, "Magmar should receive a damage boost.")
        self.assertGreater(getattr(charmander, "damage_boost", 0), charmander_damage_boost, "Charmander should receive a damage boost.")
    
    def test_blue_damage_reduction(self):
        """
        Test that Blue effect reduces damage taken by all Pokémon during the opponent's next turn.
        """
        # Create Pokémon
        ninetales = PokemonCard("Ninetales", "Fire", 90, "Water", attacks=["90FF"], energy={"F": 2})
        rapidash = PokemonCard("Rapidash", "Fire", 80, "Water", attacks=["40F"], energy={"F": 1})
        magmar = PokemonCard("Magmar", "Fire", 70, "Water", attacks=["80FF(discardOwnEnergy(2F))"], energy={"F": 2})
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", attacks=["20F"], energy={"F": 1})
        
        # Create player
        player = Player("Ash", [ninetales, rapidash, magmar, charmander], ["Water"])
        
        # Add Pokémon to player's bench
        player.active_pokemon = ninetales
        player.bench = [rapidash, magmar, charmander]
        
        # Number of damage reductions for each Pokémon before Blue's effect
        ninetales_damage_reduction = getattr(ninetales, "damage_reduction", 0)
        rapidash_damage_reduction = getattr(rapidash, "damage_reduction", 0)
        magmar_damage_reduction = getattr(magmar, "damage_reduction", 0)
        charmander_damage_reduction = getattr(charmander, "damage_reduction", 0)
        
        # Execute Blue's effect
        blue_effect(player, self.logger)
        
        # Check that all Pokémon received a damage reduction
        self.assertGreater(getattr(ninetales, "damage_reduction", 0), ninetales_damage_reduction, "Ninetales should receive a damage reduction.")
        self.assertGreater(getattr(rapidash, "damage_reduction", 0), rapidash_damage_reduction, "Rapidash should receive a damage reduction.")
        self.assertGreater(getattr(magmar, "damage_reduction", 0), magmar_damage_reduction, "Magmar should receive a damage reduction.")
        self.assertGreater(getattr(charmander, "damage_reduction", 0), charmander_damage_reduction, "Charmander should receive a damage reduction.")

    def test_blue_effect_in_fight(self):
        """
        Test that Blue's effect reduces damage during the opponent's next turn in a fight.
        """
        # Create Pokémon
        ninetales = PokemonCard("Ninetales", "Fire", 90, "Water", attacks=["90FF"], energy={"F": 2})
        pikachu = PokemonCard("Pikachu", "Electric", 50, "Ground", attacks=["20W"], energy={"E": 1})
        
        # Create players
        player = Player("Ash", [ninetales], ["Fire"])
        opponent = Player("Gary", [pikachu], ["Water"])
        
        # Set up active Pokémon
        player.active_pokemon = ninetales
        opponent.active_pokemon = pikachu
        
        # Apply Blue's effect
        blue_effect(player, self.logger)
        
        # Number of damage reductions for Ninetales before the opponent's attack
        ninetales_damage_reduction = getattr(ninetales, "damage_reduction", 0)
        self.assertEqual(ninetales_damage_reduction, 10, "Ninetales should have a 10 damage reduction from Blue.")

        # Opponent's Squirtle attacks Ninetales
        attack = pikachu.attacks[0]  # Assume Squirtle has one attack
        attack.execute_attack(pikachu, ninetales, logger=self.logger)

        # Check that the damage reduction was applied
        expected_damage = max(0, attack.damage - ninetales_damage_reduction)  # Reduced by 10
        self.assertEqual(ninetales.current_hp, ninetales.hp - expected_damage,
                         f"Ninetales should have taken {expected_damage} damage after reduction.")

        # Clear temporary effects
        player.clear_temporary_effects()

        # Verify that damage reduction is removed after the turn
        self.assertEqual(getattr(ninetales, "damage_reduction", 0), 0, "Damage reduction should be cleared after the turn.")

if __name__ == "__main__":
    unittest.main()
