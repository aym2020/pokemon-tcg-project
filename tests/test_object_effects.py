import unittest
from pokemon_card_game.card import *
from pokemon_card_game.logger import Logger
from pokemon_card_game.objects_effects import *
from pokemon_card_game.player import Player

"""
This test case tests the following features:
1. Potion: Heal 20 HP from the target Pokémon.
2. Poké Ball: Add a Pokémon to the player's hand.
3. Poké Ball: Do nothing if there are no Basic Pokémon.
4. Pokédex: Look at the top 3 cards of the deck.
5. Mythical Slab: Add a Psychic Pokémon to the player's hand.
6. Red Card: Make the opponent shuffle their hand into the deck.
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
    
    def test_pokedex_effect(self):
        """Test the Pokédex effect to look at the top 3 cards of the deck."""
        # Create a sample deck
        card1 = PokemonCard("Card 1", "Fire", 60, "Water")
        card2 = PokemonCard("Card 2", "Water", 50, "Electric")
        card3 = TrainerCard("Card 3", "Trainer")
        card4 = PokemonCard("Card 4", "Grass", 70, "Fire")
        deck = [card1, card2, card3, card4]

        player = Player("Ash", deck, energy_colors=["Fire"])
        self.logger = Logger(verbose=True)

        # Apply Pokédex effect
        top_cards = look_at_top_cards(player.deck, 3, self.logger)
        self.assertEqual(len(top_cards), 3)
        self.assertEqual([card.name for card in top_cards], ["Card 1", "Card 2", "Card 3"])

    def test_mythical_slab_effect(self):
        """Test the Mythical Slab effect."""
        # Create a sample deck
        psychic_card = PokemonCard("Psychic Pokémon", "Psychic", 60, "Dark")
        non_psychic_card = PokemonCard("Non-Psychic Pokémon", "Fire", 70, "Water")
        deck = [psychic_card, non_psychic_card]
        player = Player("Ash", deck, energy_colors=["Psychic"])
        self.logger = Logger(verbose=True)

        # Apply Mythical Slab effect
        mythical_slab_effect(player, self.logger)
        self.assertIn(psychic_card, player.hand)
        self.assertNotIn(psychic_card, player.deck)
        self.assertEqual(player.deck, [non_psychic_card])  # Ensure the non-psychic card remains in the deck
       
        # Reapply for a non-psychic card
        mythical_slab_effect(player, self.logger)
        self.assertNotIn(non_psychic_card, player.hand)
        self.assertEqual(player.deck, [non_psychic_card])  # Should be placed at the bottom

    def test_red_card_effect(self):
        """
        Test that the opponent shuffles their hand into their deck and draws 3 cards.
        """
        # Create players
        player = Player("Ash", [], [])
        opponent = Player("Gary", [], [])
        
        # Add cards to player's hand and deck
        player.hand = [
            ObjectCard("Red Card")
        ]

        # Add cards to opponent's hand and deck
        opponent.hand = [
            TrainerCard("Potion"),
            TrainerCard("Blue"),
            TrainerCard("Professor's Research")
        ]
        opponent.deck = [
            TrainerCard("Giovanni"),
            TrainerCard("Misty")
        ]

        # Define expected deck after shuffling
        expected_deck_size = len(opponent.hand) + len(opponent.deck)
        expected_hand_size = 3

        # Execute Red Card effect
        red_card_effect(player, opponent, self.logger)

        # Verify the opponent's deck size and contents
        self.assertEqual(len(opponent.deck), expected_deck_size - expected_hand_size, "Opponent's deck size should be updated.")
        self.assertEqual(len(opponent.hand), expected_hand_size, "Opponent should have exactly 3 cards in their hand.")

        