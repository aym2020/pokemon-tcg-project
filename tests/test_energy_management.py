import unittest
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.player import Player
from pokemon_card_game.gameplay import generate_energy, attach_energy
from pokemon_card_game.logger import Logger

class TestEnergyManagement(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment with a Logger.
        """
        self.logger = Logger(verbose=False)

    def test_generate_energy_single_type(self):
        """
        Test energy generation when the player has only one energy type.
        """
        # Set up the player
        player = Player("Ash", [], energy_colors=["F"])

        # Generate energy
        energy = generate_energy(player, self.logger)

        # Assertions
        self.assertEqual(energy, "F", "Generated energy should match the player's single energy type.")
        self.assertEqual(len(player.energy_zone), 1, "Energy zone should contain the generated energy.")
        self.assertIn("F", player.energy_zone, "Generated energy should be in the energy zone.")

    def test_generate_energy_multiple_types(self):
        """
        Test energy generation when the player has multiple energy types.
        """
        # Set up the player
        player = Player("Ash", [], energy_colors=["F", "W"])

        # Generate energy
        energy = generate_energy(player, self.logger)

        # Assertions
        self.assertIn(energy, ["F", "W"], "Generated energy should match one of the player's energy types.")
        self.assertEqual(len(player.energy_zone), 1, "Energy zone should contain the generated energy.")

    def test_attach_energy_active_pokemon(self):
        """
        Test attaching energy to the active Pokémon.
        """
        # Set up the player and active Pokémon
        active_pokemon = PokemonCard("Charmander", "Fire", 60, "Water", attacks=["10F"], energy={})
        player = Player("Ash", [], energy_colors=["F"])
        player.active_pokemon = active_pokemon

        # Generate and attach energy
        generate_energy(player, self.logger)
        energy_attached = attach_energy(player, player.active_pokemon, self.logger)

        # Assertions
        self.assertTrue(energy_attached, "Energy should be successfully attached to the active Pokémon.")
        self.assertEqual(player.active_pokemon.energy.get("F", 0), 1, "Active Pokémon should have 1 Fire energy.")
        self.assertEqual(len(player.energy_zone), 0, "Energy zone should be empty after attachment.")

    def test_attach_energy_bench_pokemon(self):
        """
        Test attaching energy to a Pokémon on the bench.
        """
        # Set up the player and bench Pokémon
        bench_pokemon = PokemonCard("Squirtle", "Water", 50, "Electric", attacks=["20W"], energy={})
        player = Player("Ash", [], energy_colors=["F"])
        player.bench = [bench_pokemon]

        # Generate and attach energy
        generate_energy(player, self.logger)
        energy_attached = attach_energy(player, player.bench[0], self.logger)

        # Assertions
        self.assertTrue(energy_attached, "Energy should be successfully attached to the bench Pokémon.")
        self.assertEqual(player.bench[0].energy.get("F", 0), 1, "Bench Pokémon should have 1 Fire energy.")
        self.assertEqual(len(player.energy_zone), 0, "Energy zone should be empty after attachment.")

    def test_attach_energy_no_energy_in_zone(self):
        """
        Test that energy attachment fails when the energy zone is empty.
        """
        # Set up the player and active Pokémon
        active_pokemon = PokemonCard("Charmander", "Fire", 60, "Water", attacks=["10F"], energy={})
        player = Player("Ash", [], energy_colors=["F"])
        player.active_pokemon = active_pokemon

        # Try attaching energy without generating any
        energy_attached = attach_energy(player, player.active_pokemon, self.logger)

        # Assertions
        self.assertFalse(energy_attached, "Energy attachment should fail when the energy zone is empty.")
        self.assertEqual(player.active_pokemon.energy.get("F", 0), 0, "Active Pokémon should not have any energy attached.")

    def test_attach_specific_energy_type(self):
        """
        Test attaching a specific energy type from the energy zone.
        """
        # Set up the player and bench Pokémon
        bench_pokemon = PokemonCard("Squirtle", "Water", 50, "Electric", attacks=["20W"], energy={})
        player = Player("Ash", [], energy_colors=["F", "W"])
        player.bench = [bench_pokemon]
        player.energy_zone = ["W", "F"]  # Pre-fill the energy zone

        # Attach specific energy type
        energy_attached = attach_energy(player, player.bench[0], self.logger, energy_type="W")

        # Assertions
        self.assertTrue(energy_attached, "Energy should be successfully attached to the bench Pokémon.")
        self.assertEqual(player.bench[0].energy.get("W", 0), 1, "Bench Pokémon should have 1 Water energy.")
        self.assertNotIn("W", player.energy_zone, "Water energy should be removed from the energy zone.")
        self.assertIn("F", player.energy_zone, "Fire energy should remain in the energy zone.")

if __name__ == "__main__":
    unittest.main()
