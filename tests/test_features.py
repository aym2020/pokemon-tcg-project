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
1. Pokemon initialization
2. Pokemon fight without weakness
3. Pokemon fight with weakness
4. Pokemon fight with damage boost
5. Pokemon knockout
6. Player gets point after knockout of a Pokemon
7. Player gets two points after knockout of an EX Pokemon
8. Player wins the game
9. Energy of each Pokemon
10. Attach energy to a Pokemon
11. Pokemon has correct energy to attack
12. Prevent evolution during first turn
13. Prevent evolution during second turn
14. Prevent evolution of newly played Pokemon
15. Prevent multiple evolutions in the same turn
16. Allow evolution after one turn
17. Validate evolution hierarchy
18. Evolution clears status conditions
19. Draw a card at the start of the turn
20. Prevent drawing a card on turn 1
21. Draw a card on turn 2
"""

class TestFeatures(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a Logger and test Pokémon.
        """
        self.logger = Logger(verbose=False)
        
    def test_pokemon_initialization(self):
        """
        Test that Pokémon are initialized correctly.
        """
        # Non-EX Pokemon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"])
        squirtle = PokemonCard("Squirtle", "Water", 40, "Electric", is_ex=False, attacks=["20W"])
        pikachu = PokemonCard("Pikachu", "Electric", 40, "Fighting", is_ex=False, attacks=["20CC"])
        # EX Pokemon
        charizard = PokemonCard("Charizard EX", "Fire", 200, "Water", is_ex=True, attacks=["200FFFF(discardEnergy(2F))"], energy={"F": 4})
                
        self.assertEqual(charmander.name, "Charmander")
        self.assertEqual(charmander.type, "Fire")
        self.assertEqual(charmander.hp, 60)
        self.assertEqual(charmander.weakness, "Water")

        self.assertEqual(squirtle.name, "Squirtle")
        self.assertEqual(squirtle.type, "Water")
        self.assertEqual(squirtle.hp, 40)
        self.assertEqual(squirtle.weakness, "Electric")
        
        self.assertEqual(pikachu.name, "Pikachu")
        self.assertEqual(pikachu.type, "Electric")
        self.assertEqual(pikachu.hp, 40)
        self.assertEqual(pikachu.weakness, "Fighting")
        
        self.assertEqual(charizard.name, "Charizard EX")
        self.assertEqual(charizard.type, "Fire")
        self.assertEqual(charizard.hp, 200)
        self.assertEqual(charizard.weakness, "Water")
        self.assertEqual(charizard.is_ex, True)
        
    def test_pokemon_fight_without_weakness(self):
        """
        Test that Pokémon fight correctly without weakness.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"])
        pikachu = PokemonCard("Pikachu", "Electric", 40, "Fighting", is_ex=False, attacks=["20CC"])
        
        # Initial HP
        initial_hp_charmander = charmander.hp
        initial_hp_pikachu = pikachu.hp
        
        # Attack damage
        attack_damage_charmander = charmander.attacks[0].damage
        attack_damage_pikachu = pikachu.attacks[0].damage
        
        # Create players
        player1 = Player("Ash", [charmander], ["Fire"])
        player2 = Player("Gary", [pikachu], ["Electric"])
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set active pokemon for each player
        player1.active_pokemon = charmander
        player2.active_pokemon = pikachu
        
        # Attach enough energy to perform the attack
        attach_energy(charmander, "F", 1, self.logger)
        attach_energy(pikachu, "C", 2, self.logger)
        
        # Simulate fight
        perform_attack(player1, player2, self.logger, game)
        perform_attack(player2, player1, self.logger, game)
          
        # Check if HP has decreased
        self.assertEqual(charmander.current_hp, initial_hp_charmander - attack_damage_pikachu) # Charmander HP = 60 - 20 = 40
        self.assertEqual(pikachu.current_hp, initial_hp_pikachu - attack_damage_charmander) # Pikachu HP = 40 - 30 = 10

    def test_pokemon_fight_with_weakness(self):
        """
        Test that Pokémon fight correctly with weakness.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"])
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"])
        
        # Initial HP
        initial_hp_charmander = charmander.hp
        
        # Attack damage
        attack_damage_squirtle = squirtle.attacks[0].damage
    
        # Create players
        player1 = Player("Gary", [squirtle], ["Water"])
        player2 = Player("Ash", [charmander], ["Fire"])
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set active pokemon for each player
        player1.active_pokemon = squirtle
        player2.active_pokemon = charmander
        
        # Attach enough energy to perform the attack
        attach_energy(squirtle, "W", 1, self.logger)

        # Simulate fight
        perform_attack(player1, player2, self.logger, game)

        # Check if HP has decreased
        self.assertEqual(charmander.current_hp, initial_hp_charmander - (attack_damage_squirtle + 20)) # Charmander HP = 60 - (20 + 20) = 20
    
    def test_pokemon_fight_with_damage_boost(self):
        """
        Test that Pokémon fight correctly with damage boost.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"])
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"])
        
        # Initial HP
        initial_hp_charmander = charmander.hp
        
        # Attack damage
        attack_damage_squirtle = squirtle.attacks[0].damage
        damage_boost = 10
        squirtle.damage_boost = damage_boost
    
        # Create players
        player1 = Player("Gary", [squirtle], ["Water"])
        player2 = Player("Ash", [charmander], ["Fire"])
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set active pokemon for each player
        player1.active_pokemon = squirtle
        player2.active_pokemon = charmander
        
        # Attach enough energy to perform the attack
        attach_energy(squirtle, "W", 1, self.logger)

        # Simulate fight
        perform_attack(player1, player2, self.logger, game)

        # Check if HP has decreased
        self.assertEqual(charmander.current_hp, initial_hp_charmander - (attack_damage_squirtle + 20 + damage_boost)) # Charmander HP = 60 - (20 + 20) = 20
      
    def test_pokemon_is_knocked_out(self):
        """
        Test that a Pokémon is knocked out when its HP reaches 0.
        """
        # Create Pokémon
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"])
        pikachu = PokemonCard("Pikachu", "Electric", 40, "Fighting", is_ex=False, attacks=["30CC"])
        
        # Initial HP
        initial_hp_squirtle = squirtle.hp
        
        # Attack damage
        attack_damage_pikachu = pikachu.attacks[0].damage
        
        # Create players
        player1 = Player("Ash", [pikachu], ["Electric"])
        player2 = Player("Gary", [squirtle], ["Water"])
                
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set active pokemon for each player
        player1.active_pokemon = pikachu
        player2.active_pokemon = squirtle
        
        # Attach enough energy to perform the attack
        attach_energy(pikachu, "C", 2, self.logger)
        
        # Simulate fight
        perform_attack(player1, player2, self.logger, game)

        # Verify Squirtle is in the discard pile
        self.assertIn(squirtle, player2.discard_pile)
            
        # Check if Squirtle is knocked out
        self.assertEqual(squirtle.current_hp, max(0, initial_hp_squirtle - (attack_damage_pikachu + 20))) # Squirtle HP = 50 - (30 + 20) = 0
        
        # Check if the game ended correctly
        self.assertTrue(game.game_state["ended"], "The game should have ended.")
        self.assertEqual(game.game_state["winner"], "Ash", "Ash should be the winner.")
    
    def test_player_gets_point_after_knockout(self):
        """
        Test that a player gets a point after knocking out an opponent's Pokémon.
        """
        # Create Pokémon
        pikachu = PokemonCard("Pikachu", "Electric", 40, "Fighting", is_ex=False, attacks=["30CC"])
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"])
        
        # Create players
        player1 = Player("Ash", [pikachu], ["Electric"])
        player2 = Player("Gary", [squirtle], ["Water"])
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set active pokemon for each player
        player1.active_pokemon = pikachu
        player2.active_pokemon = squirtle
        
        # Attach enough energy to perform the attack
        attach_energy(pikachu, "C", 2, self.logger)
        
        # Simulate fight: Pikachu attacks Squirtle
        perform_attack(player1, player2, self.logger, game)
       
        # Check if Ash has 1 point
        self.assertEqual(player1.prizes, 1, "Ash should have 1 point after knocking out Squirtle.")
    
    def test_player_gets_two_points_after_knockout(self):
        """
        Test that a player gets two points after knocking out an opponent's EX Pokémon.
        """
        # Create Pokémon
        pikachu = PokemonCard("Pikachu", "Electric", 40, "Fighting", is_ex=False, attacks=["30CC"])
        charizard = PokemonCard("Charizard EX", "Fire", 200, "Water", is_ex=True, attacks=["200FFFF(discardEnergy(2F))"], energy={"F": 4})
        
        # Create players
        player1 = Player("Ash", [pikachu], ["Electric"])
        player2 = Player("Gary", [charizard], ["Fire"])
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Reducing Charizard HP to 20
        charizard.current_hp = 20
        
        # Set active pokemon for each player
        player1.active_pokemon = pikachu
        player2.active_pokemon = charizard
        
        # Attach enough energy to perform the attack
        attach_energy(pikachu, "C", 2, self.logger)
        
        # Simulate fight: Pikachu attacks Charizard
        perform_attack(player1, player2, self.logger, game)
        
        # Check if Ash has 2 points after knocking out Charizard EX      
        self.assertEqual(player1.prizes, 2, "Ash should have 2 points after knocking out Charizard.")
        
    def test_player_wins_game(self):
        """
        Test that a player wins the game if the opponent has no more Pokémon.
        """
        # Create Pokémon
        pikachu = PokemonCard("Pikachu", "Electric", 40, "Fighting", is_ex=False, attacks=["30CC"])
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"])
        
        # Create players
        player1 = Player("Ash", [pikachu], ["Electric"])
        player2 = Player("Gary", [squirtle], ["Water"])
        
        # Create game
        game = Game(player1, player2, verbose=False)

        # Set active Pokémon for each player
        player1.active_pokemon = pikachu
        player2.active_pokemon = squirtle
        
        # Attach enough energy to perform the attack
        attach_energy(pikachu, "C", 2, self.logger)

        # Set Squirtle's HP low enough to be knocked out by Pikachu's attack
        squirtle.current_hp = 20

        # Simulate fight: Pikachu attacks Squirtle
        perform_attack(player1, player2, self.logger, game)
        
        # Check if the game ended correctly
        self.assertTrue(game.game_state["ended"], "The game should have ended.")
        self.assertEqual(game.game_state["winner"], "Ash", "Ash should be the winner.")
            
        # Validate game state
        self.assertEqual(player1.prizes, 1, "Ash should have 1 point after knocking out Squirtle.")
        self.assertIsNone(player2.active_pokemon, "Gary should have no active Pokémon.")
        self.assertEqual(player2.bench, [], "Gary should have no Bench Pokémon.")
        self.assertIn(squirtle, player2.discard_pile, "Squirtle should be in Gary's discard pile.")

    def test_energy_of_each_pokemon(self):
        """
        Test that energy of each pokemon is initialized correctly.
        """
        # Create Pokémon
        charizard = PokemonCard("Charizard", "Fire", 200, "Water", is_ex=False, attacks=["200FFFF(discardEnergy(2F))"], energy={"F": 4})
        
        # Assertions
        self.assertEqual(charizard.energy, {"F": 4})
        
    def test_attach_energy(self):
        """
        Test that energy is correctly attached to a Pokémon.
        """
        # Create Pokémon and Logger
        charizard = PokemonCard("Charizard", "Fire", 200, "Water", energy={"F": 2})
        logger = Logger(verbose=False)

        # Attach energy
        attach_energy(charizard, "F", 2, logger)  # Add 2 Fire Energy
        attach_energy(charizard, "C", 1, logger)  # Add 1 Colorless Energy

        # Assertions
        self.assertEqual(charizard.energy["F"], 4, "Charizard should have 4 Fire Energy.")
        self.assertEqual(charizard.energy["C"], 1, "Charizard should have 1 Colorless Energy.")

        # Test attaching energy to a card without energy support
        trainer_card = TrainerCard("Potion", "Trainer")
        attach_energy(trainer_card, "F", 1, logger)  # Should not allow energy attachment

        # Assertions
        self.assertNotIn("F", trainer_card.__dict__, "Trainer card should not have an energy attribute.")

    def test_pokemon_has_correct_energy_to_attack(self):
        """
        Test that a Pokémon has the correct energy to perform an attack.
        """
        # Create Pokémon
        charizard = PokemonCard("Charizard", "Fire", 200, "Water", is_ex=False, attacks=["200FFFF(discardEnergy(2F))"], energy={"F": 4})
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"], energy={"W": 2})
        
        # Initial HP
        initial_hp_squirtle = squirtle.hp
        
        # Attack damage
        attack_damage_charizard = charizard.attacks[0].damage
        
        # Create players
        player1 = Player("Ash", [charizard], ["Fire"])
        player2 = Player("Gary", [squirtle], ["Water"])
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set active Pokémon for each player
        player1.active_pokemon = charizard
        player2.active_pokemon = squirtle

        # Simulate fight
        perform_attack(player1, player2, self.logger, game)

        # Check if the attack was successful
        self.assertEqual(squirtle.current_hp, max(0, initial_hp_squirtle - attack_damage_charizard), "Squirtle should have 0 HP.")

        # Check if the game ended correctly
        self.assertTrue(game.game_state["ended"], "The game should have ended.")
        self.assertEqual(game.game_state["winner"], "Ash", "Ash should be the winner.")
        
    def test_prevent_evolution_during_turn_one(self):
        """
        Test that Pokémon cannot evolve during the turn 1.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1")
        
        # Create a player
        player = Player("Ash", [charmander, charmeleon], ["Fire"])
        player.hand.append(charmeleon)  # Add Charmeleon to the player's hand
        
        # Create game
        game = Game(player, None, verbose=False)
        game.turn_count = 1  # Set the game to the first turn
        
        # Manually set the active Pokémon
        player.active_pokemon = charmander

        # Attempt to evolve Charmander into Charmeleon
        self.logger.log("Simulating evolution on the first turn...")
        result = evolve_pokemon(player, charmander, charmeleon, self.logger, game.turn_count)
        self.assertFalse(result, "Charmander should not evolve during the first turn.")
    
    def test_allow_evolution_during_turn_two(self):
        """
        Test that Pokémon can evolve during the turn 2.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1")
        
        # Create a player
        player = Player("Ash", [charmander, charmeleon], ["Fire"])
        player.hand.append(charmeleon)  # Add Charmeleon to the player's hand
        
        # Create game
        game = Game(player, None, verbose=False)
        game.turn_count = 2  # Set the game to the second turn
        
        # Manually set the active Pokémon
        player.active_pokemon = charmander

        # Attempt to evolve Charmander into Charmeleon
        self.logger.log("Simulating evolution on the second turn...")
        result = evolve_pokemon(player, charmander, charmeleon, self.logger, game.turn_count)
        self.assertTrue(result, "Charmander should evolve during the second turn.")

    def test_prevent_evolution_of_newly_played_pokemon(self):
        """
        Test that newly played Pokémon cannot evolve during the same turn they are played.
        """
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1")
        
        # Create a player
        player = Player("Ash", [charmander, charmeleon], ["Fire"])
        player.hand.append(charmeleon)  # Add Charmeleon to the player's hand
        
        # Create game
        game = Game(player, None, verbose=False)
        game.turn_count = random.randint(2, 100)  # Set the game to a random turn between 2 and 100
        
        # Play Charmander as the active Pokémon
        player.play_pokemon(charmander, self.logger)

        # Attempt to evolve Charmander into Charmeleon
        result = evolve_pokemon(player, charmander, charmeleon, self.logger, game.turn_count)
        self.assertFalse(result, "Charmander should not evolve during the same turn it was played.")
        self.assertIn(charmander, player.newly_played_pokemons, "Charmander should be in the newly played Pokémon list.")

    def test_prevent_multiple_evolutions_in_same_turn(self):
        """
        Test that a Pokémon cannot evolve multiple times in the same turn.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1")
        charizard = PokemonCard("Charizard", "Fire", 150, "Water", is_ex=False, evolves_from="Charmeleon", subcategory="Stage 2")
        
        # Create a player
        player = Player("Ash", [charmander, charmeleon, charizard], ["Fire"])
        
        # Initialize the player's hand
        player.hand.append(charmeleon)
        player.hand.append(charizard)
        
        # Manually set the active Pokémon
        player.active_pokemon = charmander
        
        # Create game
        game = Game(player, None, verbose=False)

        # Set the game to a random turn between 2 and 100
        game.turn_count = random.randint(2, 100)
        
        # First evolution: Charmander -> Charmeleon
        result1 = evolve_pokemon(player, charmander, charmeleon, self.logger, game.turn_count)
        self.assertTrue(result1, "Charmander should evolve into Charmeleon.")

        # Attempt second evolution: Charmeleon -> Charizard
        result2 = evolve_pokemon(player, charmeleon, charizard, self.logger, game.turn_count)
        self.assertFalse(result2, "Charmeleon should not evolve into Charizard in the same turn.")

    def test_allow_evolution_after_one_turn(self):
        """
        Test that a Pokémon can evolve after being on the field for at least one turn.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1")
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, subcategory="Basic")
        
        # Create a player
        player1 = Player("Ash", [charmander, charmeleon], ["Fire"])
        player2 = Player("Gary", [squirtle, squirtle], ["Water"])
        
        # Initialize the players' hands
        player1.hand.append(charmeleon)
        player2.hand.append(squirtle)
        
        # Create game
        game = Game(player1, player2, verbose=False)
        
        # Set the game turn
        game.current_turn = 0
        game.turn_count = 2
        
        # Manually set the active Pokémon for player 2
        player2.active_pokemon = squirtle
        
        # Play Charmander as the active Pokémon for player 1
        player1.play_pokemon(charmander, self.logger)
        
        # Check if Charmander is in the newly played Pokémon list
        self.assertIn(charmander, player1.newly_played_pokemons, "Charmander should be in the newly played Pokémon list.")
        
        # End the turn
        game.end_turn()
               
        # Attempt to evolve Charmander into Charmeleon
        result = evolve_pokemon(player1, charmander, charmeleon, self.logger, game.turn_count)
        self.assertTrue(result, "Charmander should evolve into Charmeleon after one turn.")

    def test_validate_evolution_hierarchy(self):
        """
        Test that Pokémon evolve correctly based on hierarchy.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1")
        charizard = PokemonCard("Charizard", "Fire", 150, "Water", is_ex=False, evolves_from="Charmeleon", subcategory="Stage 2")
        
        # Create a player
        player = Player("Ash", [charmander, charmeleon, charizard], ["Fire"])
        
        # Initialize the player's hand
        player.hand.append(charmeleon)
        player.hand.append(charizard)
                
        # Manually set the active Pokémon
        player.active_pokemon = charmander
        
        # Create game
        game = Game(player, None, verbose=False)

        # Set the game to a random turn between 2 and 100
        game.turn_count = random.randint(2, 100)
        
        # Charmander -> Charmeleon
        result1 = evolve_pokemon(player, charmander, charmeleon, self.logger, game.turn_count)
        self.assertTrue(result1, "Charmander should evolve into Charmeleon.")
        
        # Check if the active Pokémon is now Charmeleon
        self.assertEqual(player.active_pokemon.name, "Charmeleon", "The active Pokémon should now be Charmeleon.")
        
        # Check if Charmeleon is in the newly evolved Pokémon list
        self.assertIn(charmeleon, player.newly_evolved_pokemons, "Charmeleon should be in the newly evolved Pokémon list.")

        # Attempt invalid evolution: Charmander -> Charizard
        result2 = evolve_pokemon(player, charmander, charizard, self.logger, game.turn_count)
        self.assertFalse(result2, "Charmander should not evolve directly into Charizard.")

    def test_evolution_clears_status_conditions(self):
        """
        Test that evolving a Pokémon clears its status conditions.
        """
        # Create Pokémon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, evolves_from="Charmander", subcategory="Stage 1")
        
        # Create a player
        player = Player("Ash", [charmander, charmeleon], ["Fire"])
        
        # Initialize the player's hand
        player.hand.append(charmeleon)
        
        # Set status condition
        charmander.status = "poisoned"
        
        # Manually set the active Pokémon
        player.active_pokemon = charmander
        
        # Create game
        game = Game(player, None, verbose=False)
        
        # Set the game to a random turn between 2 and 100
        game.turn_count = random.randint(2, 100)
        
        # Attempt to evolve Charmander into Charmeleon
        result = evolve_pokemon(player, charmander, charmeleon, self.logger, game.turn_count)
        self.assertTrue(result, "Charmander should evolve into Charmeleon.")
        self.assertEqual(player.active_pokemon.name, "Charmeleon", "The active Pokémon should now be Charmeleon.")
        self.assertIsNone(player.active_pokemon.status, "Evolving should clear status conditions.")
    
    def test_draw_card_at_start_of_turn(self):
        """
        Test that a player draws a card at the start of their turn.
        """
        # Create a pokemon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        
        # Create a player
        player = Player("Ash", [charmander, charmander], ["Fire"])
        
        # Draw a card
        player.draw_card(self.logger)
        
        # Assertions
        self.assertEqual(len(player.hand), 1, "Player should have 1 card in their hand.")
    
    def test_prevent_drawing_card_on_turn_one(self):
        """
        Test that a player cannot draw a card on the first turn.
        """
        # Create a player
        player = Player("Ash", [], ["Fire"])
        
        # Create game
        game = Game(player, None, verbose=False)
        
        # Set the game to a random turn between 2 and 100
        game.turn_count = 1
        
        # Attempt to draw a card
        player.draw_card(self.logger)
        
        # Assertions
        self.assertEqual(len(player.hand), 0, "Player should not draw a card on the first turn.")
    
    def test_draw_card_on_turn_two(self):
        """
        Test that a player draws a card on the second turn.
        """
        # Create a pokemon
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, subcategory="Basic")
        
        # Create a player
        player = Player("Ash", [charmander, charmander], ["Fire"])
        
         # Create game
        game = Game(player, None, verbose=False)
        
        # Set the game to a random turn between 2 and 100
        game.turn_count = 2
        
        # Attempt to draw a card
        player.draw_card(self.logger)
        
        # Assertions
        self.assertEqual(len(player.hand), 1, "Player should draw a card on the second turn.")
    
    def test_get_evolution_and_max_energy_from_deck(self):
        """
        Test the function to retrieve evolutions and calculate the maximum energy required.
        """
        # Create a sample deck
        charmander = PokemonCard("Charmander", "Fire", 60, "Water", attacks=["10F"])
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", evolves_from="Charmander", attacks=["50FF"])
        charizard = PokemonCard("Charizard", "Fire", 150, "Water", evolves_from="Charmeleon", attacks=["200FFFF(discardOwnEnergy(2F))", "100FFF"])
        squirtle = PokemonCard("Squirtle", "Water", 50, "Electric", attacks=["20W"])

        # Create player and add cards to deck
        deck = [charmander, charmeleon, charizard, squirtle]
        player = Player("Ash", deck, energy_colors=["Fire"])

        # Set Charmander as the active Pokémon
        player.active_pokemon = charmander

        # Create AI instance
        ai = BasicAI(player, self.logger)

        # Call the AI method
        evolutions, max_energy_required = ai.get_evolution_and_max_energy_from_deck(charmander)

        # Assertions
        self.assertEqual(len(evolutions), 2, "There should be 2 evolutions (Charmeleon, Charizard).")
        self.assertEqual(max_energy_required.get("F", 0), 4, "The maximum Fire energy required should be 4.")
              
if __name__ == '__main__':
    unittest.main()
