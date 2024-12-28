from pokemon_card_game.card import Card
from pokemon_card_game.card  import PokemonCard, TrainerCard, ObjectCard
from pokemon_card_game.player import Player
from pokemon_card_game.game import Game

# Create decks
deck1 = [
    PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"]),
    PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, attacks=["50FF"], evolves_from="Charmander"),
    PokemonCard("Charizard", "Fire", 200, "Water", is_ex=True, attacks=["200FFFF(discardEnergy(2F))"], evolves_from="Charmeleon"),
    TrainerCard("Potion", effect="Heal 20 damage from a Pokémon."),
    TrainerCard("Red Card", effect="Shuffle opponent's hand into their deck and draw 3 cards."),
] * 4

deck2 = [
    PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"]),
    PokemonCard("Wartortle", "Water", 70, "Electric", is_ex=False, attacks=["40WW"], evolves_from="Squirtle"),
    PokemonCard("Blastoise", "Water", 180, "Electric", is_ex=True, attacks=["40"], evolves_from="Wartortle"),
    TrainerCard("Potion", effect="Heal 20 damage from a Pokémon."),
    TrainerCard("Red Card", effect="Shuffle opponent's hand into their deck and draw 3 cards."),
] * 4

# Define energy colors
deck1_energy_colors = ["F"]
deck2_energy_colors = ["W"]

# Create players
player1 = Player(name="Ash", deck=deck1, energy_colors=deck1_energy_colors)
player2 = Player(name="Gary", deck=deck2, energy_colors=deck2_energy_colors)

# Initialize the game
game = Game(player1, player2, verbose=True)  # Enable detailed logs
game.start_game()

# Simulate turns
for _ in range(30):  # Simulate x turns
    game.play_turn()