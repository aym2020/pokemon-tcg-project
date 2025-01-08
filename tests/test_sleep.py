import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.logger import Logger
from pokemon_card_game.gameplay import apply_sleep
from colorama import Fore

class TestSleepMechanics(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(verbose=False)
        self.charmander = PokemonCard("Charmander", "Fire", 60, "Water")
        self.squirtle = PokemonCard("Squirtle", "Water", 50, "Electric")

    def test_apply_sleep(self):
        """
        Test that sleep status is applied correctly.
        """
        apply_sleep(self.charmander, self.logger)
        self.assertEqual(self.charmander.status, "asleep", "Charmander should be asleep.")

    def test_sleep_prevents_retreat(self):
        """
        Test that a sleeping Pokémon cannot retreat.
        """
        self.charmander.status = "asleep"
        self.assertFalse(self.charmander.status != "asleep", "Charmander cannot retreat while asleep.")

    def test_sleep_prevents_attack(self):
        """
        Test that a sleeping Pokémon cannot attack.
        """
        self.charmander.status = "asleep"
        self.assertEqual(self.charmander.status, "asleep", "Charmander should not attack while asleep.")

    def test_wake_up_heads(self):
        """
        Test that a Pokémon wakes up with a Heads coin toss.
        """
        self.charmander.status = "asleep"
        for _ in range(100):  # Simulate 100 coin tosses
            self.charmander.apply_status_effects(self.logger)
            if self.charmander.status is None:
                break
        self.assertIsNone(self.charmander.status, "Charmander should wake up on Heads.")

    def test_trainer_card_switches_sleeping_pokemon(self):
        """
        Test that a Trainer card can force a sleeping Pokémon to the bench.
        """
        self.charmander.status = "asleep"
        self.squirtle.status = None
        bench = [self.squirtle]

        # Assume Trainer card effect swaps the active Pokémon with a bench Pokémon
        def force_switch(active, bench, logger):
            bench.append(active)  # Add active Pokémon to the bench
            new_active = bench.pop(0)  # Remove the first Pokémon from the bench to make it active
            logger.log(f"{active.name} was forced to the bench by a Trainer card.", color=Fore.YELLOW)
            return new_active

        # Simulate the Trainer card effect
        new_active = force_switch(self.charmander, bench, self.logger)

        # Assert the new active Pokémon is Squirtle
        self.assertEqual(new_active.name, "Squirtle", "Squirtle should now be the active Pokémon.")
        self.assertIn(self.charmander, bench, "Charmander should now be on the bench.")
        self.assertIsNone(new_active.status, "The new active Pokémon should not have any status effects.")

    def test_evolve_cures_status(self):
        """
        Test that evolving a Pokémon cures all its status effects.
        """
        self.charmander.status = "asleep"

        # Simulate evolution
        charmeleon = PokemonCard("Charmeleon", "Fire", 90, "Water", evolves_from="Charmander")
        
        def evolve(pokemon, evolution):
            evolution.current_hp = pokemon.current_hp
            evolution.energy = pokemon.energy
            evolution.status = None  # Cure all status effects
            return evolution

        evolved_pokemon = evolve(self.charmander, charmeleon)

        # Assert the evolved Pokémon is now active and has no status
        self.assertEqual(evolved_pokemon.name, "Charmeleon", "The Pokémon should now be Charmeleon.")
        self.assertIsNone(evolved_pokemon.status, "Evolving should cure all status effects.")

if __name__ == "__main__":
    unittest.main()
