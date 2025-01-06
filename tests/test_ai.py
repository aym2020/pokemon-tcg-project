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
8. Check that the AI does not use Misty effect if there are no Water Pokémon.
9. Check that the AI uses Blaine effect to boost damage for Ninetales, Rapidash, or Magmar.
10. Check that the AI does not use Blaine effect if there are no Ninetales, Rapidash, or Magmar.
11. Check that the AI uses Professor's Research effect to draw 2 cards.
12. Check that the AI can use only one Trainer card per turn.
13. Check that the AI uses Blue effect to reduce damage for all Pokémon by 10.
14. Check that the AI uses Erik effect to heal a Grass Pokémon.
15. Check that the AI does not use Erik effect if there are no Grass Pokémon.
16. Check that the AI uses Pokédex card to look at the top 3 cards of its deck.
17. Check that the AI uses Mythical Slab effect to add a Psychic Pokémon to the player's hand.
18. Check that the AI uses Fossil card to add a random Basic Pokémon to the player's hand.
19. Check that the AI uses Budding expeditioner to bring Mew ex to the player's hand.
20. Check that the AI uses Koga to bring Muk or Weezing to the player's hand.
21. Check that the AI uses Red Card to shuffle the opponent's hand into their deck and draw 3 cards.
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
        player = Player("Ash", [charmander, charmeleon], ["Fire"])
        opponent = Player("Gary", [bulbasaur], ["Grass"])
        player.hand.append(charmeleon)  # Add Charmeleon to player's hand
        player.active_pokemon = charmander
        opponent.active_pokemon = bulbasaur

        ai1 = BasicAI(player, self.logger)
        ai2 = BasicAI(opponent, self.logger)
        
        # Create game and set turn to 1
        game = Game(player, opponent, verbose=False, ai1=ai1, ai2=ai2)
        game.turn_count = 1  # Set to turn 1 to allow evolution

        # Simulate AI turn for player
        ai1.play_turn(opponent, game)
        
        # Check that Charmeleon is still in the hand and Charmander remains unevolved
        self.assertIn(charmeleon, player.hand, "AI should not attempt to evolve Charmander during turn 1.")
        self.assertEqual(player.active_pokemon, charmander, "Charmander should remain unevolved during turn 1.")
    
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
        player = Player("Ash", [charmander, charmeleon], ["Fire"])
        opponent = Player("Gary", [bulbasaur], ["Grass"])
        player.hand.append(charmeleon)  # Add Charmeleon to player's hand
        player.active_pokemon = charmander
        opponent.active_pokemon = bulbasaur

        ai1 = BasicAI(player, self.logger)
        ai2 = BasicAI(opponent, self.logger)
        
        # Create game and set turn to 2
        game = Game(player, opponent, verbose=False, ai1=ai1, ai2=ai2)
        game.turn_count = 2  # Set to turn 2 to allow evolution

        # Simulate AI turn for player
        ai1.play_turn(opponent, game)
        
        # Check that Charmeleon is no longer in the hand and Charmander has evolved
        self.assertNotIn(charmeleon, player.hand, "Charmeleon should no longer be in the hand after evolution.")
        self.assertEqual(player.active_pokemon.name, "Charmeleon", "Charmander should have evolved into Charmeleon.")

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
        
        # Fill the player's energy zone for attack
        player.energy_zone = ["F"]  # Add Fire energy required for Charmander's attack
        
        # Simulate AI turn
        ai.play_turn(opponent, game)
        
        # Calculate expected HP after attack
        attack_damage = charmander.attacks[0].damage
        expected_hp = squirtle.hp - attack_damage
        
        # Validate that damage was dealt to the opponent's active Pokémon
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
        opponent = Player("Gary", [], [])
        
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
        ai.use_object_card(opponent)
        
        # Check that the Pokémon was healed
        self.assertGreater(squirtle.current_hp, hp_before, "Pokémon should be healed by Potion effect.")
    
    def test_ai_use_potion_effect_no_pokemon(self):
        """
        Test that the AI does not use Potion effect if there are no Pokémon to heal.
        """
        # Create pokémon
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 3})
        
        # Create player
        player = Player("Ash", [], ["Water"])
        opponent = Player("Gary", [], [])
        
        # Create Potion card
        potion = ObjectCard("Potion", "Heal 20 HP from the target Pokémon.")
        
        # Add Potion to player's hand
        player.hand.append(potion)
        
        # Set up active Pokémon
        player.active_pokemon = squirtle
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Potion effect
        ai.use_object_card(opponent)
        
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
        opponent = Player("Gary", [], [])
        
        # Define the number of cards in the player's hand before using Poké Ball
        hand_size_before = len(player.hand)
        
        # Create Poké Ball card
        pokeball = ObjectCard("Poké Ball", "Find a random Basic Pokémon from the deck, add it to the player's hand, and shuffle the deck.")
        
        # Add Poké Ball to player's hand
        player.hand.append(pokeball)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Poké Ball effect
        ai.use_object_card(opponent)
        
        # Check that a Pokémon was added to the player's hand
        self.assertEqual(len(player.hand), hand_size_before + 1, "Poké Ball should add a Pokémon to the player's hand.")
        
    def test_ai_no_water_pokemon_misty_effect(self):
        """
        Test that the AI does not use Misty effect if there are no Water Pokémon.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 0})
        
        # Create player
        player = Player("Ash", [charmander], ["Water"])
        opponent = Player("Gary", [], [])
        
        # Set Charmander as the active Pokémon
        player.active_pokemon = charmander  # Fire type
        player.bench = []
        
        # Create Misty card
        misty = TrainerCard("Misty", "Flip coins until tails and attach Water Energy for each heads to the target Pokémon.")
        
        # Add Misty to player's hand
        player.hand.append(misty)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Misty effect
        ai.use_trainer_card(opponent)
        
        # Check that no energy was attached
        self.assertEqual(charmander.energy.get("W", 0), 0, "Charmander should not receive Water Energy.")
    
    def test_ai_use_blaine_effect(self):
        """
        Test that the AI uses Blaine effect to boost damage for Ninetales, Rapidash, or Magmar.
        """
        # Create Pokémon
        ninetales = PokemonCard("Ninetales", "Fire", 90, "Water", attacks=["90FF"], energy={"F": 2})
        rapidash = PokemonCard("Rapidash", "Fire", 80, "Water", attacks=["40F"], energy={"F": 1})
        magmar = PokemonCard("Magmar", "Fire", 50, "Water", attacks=["80FF(discardOwnEnergy(2F))"], energy={"F": 2})
        
        # Create player
        player = Player("Ash", [ninetales, rapidash, magmar], ["Fire"])
        opponent = Player("Gary", [], [])
        
        # Set up active Pokémon
        player.active_pokemon = ninetales
        
        # Define the amount of damage before using Blaine
        damage_boost_before = ninetales.damage_boost
        
        # Create Blaine card
        blaine = TrainerCard("Blaine", "Boost damage by 20 for Ninetales, Rapidash, or Magmar.")
        
        # Add Blaine to player's hand
        player.hand.append(blaine)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Blaine effect
        ai.use_trainer_card(opponent)
        
        # Check that the damage was boosted
        self.assertEqual(ninetales.damage_boost, damage_boost_before + 30, "Blaine effect should boost damage for Ninetales.")
    
    def test_ai_no_ninetales_rapidash_magmar_blaine_effect(self):
        """
        Test that the AI does not use Blaine effect if there are no Ninetales, Rapidash, or Magmar.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 1})
        
        # Create player
        player = Player("Ash", [charmander], ["Fire"])
        opponent = Player("Gary", [], [])
        
        # Set Charmander as the active Pokémon
        player.active_pokemon = charmander  # Fire type
        player.bench = []
        
        # Create Blaine card
        blaine = TrainerCard("Blaine", "Boost damage by 20 for Ninetales, Rapidash, or Magmar.")
        
        # Add Blaine to player's hand
        player.hand.append(blaine)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Blaine effect
        ai.use_trainer_card(opponent)
        
        # Check that the Blaine card was not used
        self.assertIn(blaine, player.hand, "Blaine effect should not be used if there are no Ninetales, Rapidash, or Magmar.")
        
    def test_ai_use_professors_research_effect(self):
        """
        Test that the AI uses Professor's Research effect to draw 2 cards.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 0})
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", energy={"W": 0})
        
        # Create player with a non-empty deck
        player = Player("Ash", [charmander, squirtle], ["Water"])
        opponent = Player("Gary", [], [])
        
        # Define the number of cards in the player's hand before using Professor's Research
        hand_size_before = len(player.hand)
        
        # Create Professor's Research card
        professors_research = TrainerCard("Professor's Research", "Draw 2 cards from the player's deck.")
        
        # Add Professor's Research to player's hand
        player.hand.append(professors_research)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Professor's Research effect
        ai.use_trainer_card(opponent)
        
        # Check that 2 cards were drawn from the player's deck
        self.assertEqual(len(player.hand), hand_size_before + 2, "Professor's Research should draw 2 cards from the player's deck.")
        
    def test_ai_use_one_trainer_card_per_turn(self):
        """
        Test that the AI can use only one Trainer card per turn.
        """
        # Create Pokémon
        rapidash = PokemonCard("Rapidash", "Fire", 80, "Water", energy={"F": 1})
        
        # Create Trainer cards
        blaine = TrainerCard("Blaine", "Boost damage by 30 for Ninetales, Rapidash, or Magmar.")
        professors_research = TrainerCard("Professor's Research", "Draw 2 cards from the player's deck.")
        
        # Create player
        player = Player("Ash", [rapidash], ["Fire"])
        opponent = Player("Gary", [], [])
        
        # Set active Pokémon
        player.active_pokemon = rapidash
        
        # Add Trainer cards to player's hand
        player.hand.extend([blaine, professors_research])
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Trainer card
        ai.use_trainer_card(opponent)
        
        # Check that only one Trainer card was used
        self.assertTrue(player.trainer_card_played, "AI should have played one Trainer card.")
        self.assertEqual(len(player.hand), 1, "AI should have one Trainer card left in hand.")
    
    def test_ai_use_giovanni_effect(self):
        """
        Test that the AI uses Giovanni effect to boost damage for all Pokémon.
        """
        # Create Pokémon
        ninetales = PokemonCard("Ninetales", "Fire", 90, "Water", attacks=["90FF"], energy={"F": 2})
        magmar = PokemonCard("Magmar", "Fire", 70, "Water", attacks=["70F"], energy={"F": 1})
        
        # Create player
        player = Player("Ash", [ninetales, magmar], ["Fire"])
        player.active_pokemon = ninetales
        player.bench = [magmar]
        opponent = Player("Gary", [], [])
        
        # Create Giovanni card
        giovanni = TrainerCard("Giovanni", "Boost all Pokémon attacks by 10 damage.")
        player.hand.append(giovanni)
                
        # Damage boost before playing Giovanni
        ninetales_damage_boost_before = ninetales.damage_boost
        magmar_damage_boost_before = magmar.damage_boost
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Giovanni effect
        ai.use_trainer_card(opponent)

        # Check that the damage was boosted
        self.assertEqual(ninetales.damage_boost, ninetales_damage_boost_before + 10, "Ninetales should receive a +10 damage boost.")
        self.assertEqual(magmar.damage_boost, magmar_damage_boost_before + 10, "Magmar should receive a +10 damage boost.")

    def test_ai_use_blue_effect(self):
        """
        Test that the AI uses Blue effect to reduce damage for all Pokémon by 10.
        """
        # Create Pokémon
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric")
        bulbasaur = PokemonCard("Bulbasaur", "Grass", 60, "Fire")
        
        # Create player
        player = Player("Ash", [], ["Water"])
        opponent = Player("Gary", [], [])
        
        # Set active Pokémon and bench
        player.active_pokemon = squirtle
        player.bench = [bulbasaur]

        # Add Blue card
        blue = TrainerCard("Blue", "Reduce damage by 10 during opponent's turn.")
        player.hand.append(blue)

        ai = BasicAI(player, self.logger)
        ai.use_trainer_card(opponent)

        # Verify damage reduction
        self.assertEqual(squirtle.damage_reduction, 10)
        self.assertEqual(bulbasaur.damage_reduction, 10)
    
    def test_ai_use_erika_effect(self):
        """
        Test that the AI uses Erika effect to heal a Grass Pokémon.
        """
        # Create Pokémon
        bulbasaur = PokemonCard("Bulbasaur", "Grass", 60, "Fire", energy={"G": 1})
        bulbasaur.current_hp = 30
        
        # Create player
        player = Player("Ash", [bulbasaur], ["Grass"])
        opponent = Player("Gary", [], [])
        
        # Set active Pokémon
        player.active_pokemon = bulbasaur
        
        # Define the amount of HP before using Erika
        hp_before = bulbasaur.current_hp
        
        # Create Erika card
        erika = TrainerCard("Erika", "Heal 50 damage from the target Pokémon if it is of Grass type.")
        
        # Add Erika to player's hand
        player.hand.append(erika)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Erika effect
        ai.use_trainer_card(opponent)
        
        # Check that the Pokémon was healed
        self.assertGreater(bulbasaur.current_hp, hp_before, "Pokémon should be healed by Erika effect.")

    def test_ai_no_grass_pokemon_erika_effect(self):
        """
        Test that the AI does not use Erika effect if there are no Grass Pokémon.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", energy={"F": 1})
        
        # Create player
        player = Player("Ash", [charmander], ["Fire"])
        opponent = Player("Gary", [], [])
        
        # Set Charmander as the active Pokémon
        player.active_pokemon = charmander  # Fire type
        player.bench = []
        
        # Create Erika card
        erika = TrainerCard("Erika", "Heal 50 damage from the target Pokémon if it is of Grass type.")
        
        # Add Erika to player's hand
        player.hand.append(erika)
        
        # Create AI
        ai = BasicAI(player, self.logger)
        
        # Use Erika effect
        ai.use_trainer_card(opponent)
        
        # Check that the Erika card was not used
        self.assertIn(erika, player.hand, "Erika effect should not be used if there are no Grass Pokémon.")

    def test_ai_uses_pokedex(self):
        """Test that the AI uses the Pokédex card to look at the top 3 cards of its deck."""
        # Create Pokémon and object card
        card1 = PokemonCard("Card 1", "Fire", 60, "Water")
        card2 = PokemonCard("Card 2", "Fire", 70, "Water")
        card3 = PokemonCard("Card 3", "Fire", 80, "Water")
        pokedex = ObjectCard("Pokédex", "Look at the top 3 cards of your deck.")

        # Create a player and add cards to their deck and hand
        player = Player("Ash", [card1, card2, card3], energy_colors=["Fire"])
        player.hand.append(pokedex)
        opponent = Player("Gary", [], [])

        # Create AI
        ai = BasicAI(player, self.logger)

        # Use Pokédex
        ai.use_object_card(opponent)

        # Check that the Pokédex card was used and is no longer in the hand
        self.assertNotIn(pokedex, player.hand, "Pokédex should be removed from the hand after use.")

    def test_ai_uses_mythical_slab(self):
        """Test that the AI uses the Mythical Slab card correctly."""
        # Create Pokémon and object card
        psychic_card = PokemonCard("Psychic Pokémon", "Psychic", 60, "Dark")
        non_psychic_card = PokemonCard("Non-Psychic Pokémon", "Fire", 70, "Water")
        mythical_slab = ObjectCard("Mythical Slab", "Look at the top card of your deck and act based on its type.")

        # Create a player and add cards to their deck and hand
        player = Player("Ash", [psychic_card, non_psychic_card], energy_colors=["Psychic"])
        player.hand.append(mythical_slab)
        opponent = Player("Gary", [], [])

        # Create AI
        ai = BasicAI(player, self.logger)

        # Use Mythical Slab
        ai.use_object_card(opponent)

        # Check that the Mythical Slab card was used and is no longer in the hand
        self.assertNotIn(mythical_slab, player.hand, "Mythical Slab should be removed from the hand after use.")

        # Check that the psychic card was moved to the hand
        self.assertIn(psychic_card, player.hand, "Psychic Pokémon should be in the hand after using Mythical Slab.")

        # Use Mythical Slab again for the next card
        ai.use_object_card(opponent)

        # Check that the non-psychic card was placed at the bottom of the deck
        self.assertEqual(player.deck[-1], non_psychic_card, "Non-Psychic Pokémon should be placed at the bottom of the deck.")
    
    def test_ai_uses_fossil_as_basic_pokemon(self):
        """Test that the AI uses fossil object cards as basic Pokémon."""
        # Create a fossil card
        dome_fossil = ObjectCard("Dome Fossil", "Play as a 40-HP Basic Colorless Pokémon.")
        
        # Create a player with the fossil card in their hand
        player = Player("Ash", [], ["Colorless"])
        player.hand.append(dome_fossil)
        
        # Create AI instance
        ai = BasicAI(player, self.logger)
        
        # Ensure the active Pokémon slot is empty
        self.assertIsNone(player.active_pokemon, "Active Pokémon should be None before the AI plays a card.")

        # Simulate AI turn logic
        ai.play_pokemon_if_needed()

        # Check that the AI used the fossil card as a Pokémon
        self.assertIsNotNone(player.active_pokemon, "AI should have used the fossil card to set an active Pokémon.")
        self.assertEqual(player.active_pokemon.name, "Dome Fossil", "The active Pokémon should be the Dome Fossil.")
        self.assertEqual(player.active_pokemon.hp, 40, "Dome Fossil should have 40 HP.")
        self.assertEqual(player.active_pokemon.type, "Colorless", "Dome Fossil should be a Colorless Pokémon.")
    
    def test_ai_uses_budding_expeditioner(self):
        """Test that the AI uses Budding Expeditioner when the active Pokémon is Mew ex."""
        # Create a Mew ex Pokémon card
        mew_ex = PokemonCard("Mew ex", "Psychic", 90, "Dark")
        
        # Create player and set up the deck and hand
        player = Player("Ash", [], ["Psychic"])
        player.active_pokemon = mew_ex
        opponent = Player("Gary", [], [])

        # Create Budding Expeditioner card
        budding_expeditioner = TrainerCard("Budding Expeditioner", effect="Put your Mew ex in the Active Spot into your hand.")
        player.hand.append(budding_expeditioner)

        # Create AI instance
        ai = BasicAI(player, self.logger)

        # Ensure AI recognizes the card as eligible
        self.assertTrue(ai.is_card_eligible(budding_expeditioner), "Budding Expeditioner should be eligible if Mew ex is in the Active Spot.")

        # Execute AI logic for using trainer cards
        ai.use_trainer_card(opponent)

        # Check that the Mew ex card is now in the player's hand
        self.assertIn(mew_ex, player.hand, "Mew ex should be added to the player's hand after using Budding Expeditioner.")

        # Check that Budding Expeditioner card was removed from the hand
        self.assertNotIn(budding_expeditioner, player.hand, "Budding Expeditioner should be removed from the player's hand after being used.")

        # Ensure the active Pokémon spot is now empty
        self.assertIsNone(player.active_pokemon, "The Active Spot should be empty after using Budding Expeditioner.")

    def test_ai_uses_koga(self):
        """Test that the AI uses Koga when the active Pokémon is Muk or Weezing."""
        # Create Muk and Weezing Pokémon cards
        muk = PokemonCard("Muk", "Poison", 100, "Psychic")
        weezing = PokemonCard("Weezing", "Poison", 90, "Psychic")

        # Create player and set up the deck and hand
        player = Player("Ash", [], ["Poison"])
        player.active_pokemon = muk
        opponent = Player("Gary", [], [])
        
        # Create Koga card
        koga_card = TrainerCard("Koga", effect="Put your Muk or Weezing in the Active Spot into your hand.")
        player.hand.append(koga_card)

        # Create AI instance
        ai = BasicAI(player, self.logger)

        # Ensure AI recognizes the card as eligible
        self.assertTrue(ai.is_card_eligible(koga_card), "Koga should be eligible if Muk or Weezing is in the Active Spot.")

        # Execute AI logic for using trainer cards
        ai.use_trainer_card(opponent)

        # Check that the Muk card is now in the player's hand
        self.assertIn(muk, player.hand, "Muk should be added to the player's hand after using Koga.")

        # Check that Koga card was removed from the hand
        self.assertNotIn(koga_card, player.hand, "Koga should be removed from the player's hand after being used.")

        # Ensure the active Pokémon spot is now empty
        self.assertIsNone(player.active_pokemon, "The Active Spot should be empty after using Koga.")

    def test_ai_uses_red_card(self):
        """
        Test that the AI uses Red Card during its turn.
        """
        # Create players
        player = Player("Ash", [], [])
        opponent = Player("Gary", [], [])

        # Add Red Card to the player's hand
        red_card = ObjectCard("Red Card")
        player.hand = [red_card]

        # Add cards to the opponent's hand and deck
        opponent.hand = [
            TrainerCard("Potion"),
            TrainerCard("Blue"),
            TrainerCard("Professor's Research")
        ]
        opponent.deck = [
            TrainerCard("Giovanni"),
            TrainerCard("Misty")
        ]

        # Create AI
        ai1 = BasicAI(player, self.logger)

        # Create game
        game = Game(player, opponent, verbose=False)

        # AI turn logic
        ai1.use_object_card(opponent)

        # Verify Red Card was used
        self.assertNotIn(red_card, player.hand, "Red Card should be removed from the player's hand after being used.")
        self.assertEqual(len(opponent.hand), 3, "Opponent should have 3 cards in their hand after Red Card effect.")
