from pokemon_card_game.card import Card
from pokemon_card_game.card  import PokemonCard, TrainerCard, ObjectCard
from pokemon_card_game.player import Player
from pokemon_card_game.game import Game, Logger 
from pokemon_card_game.ai import BasicAI

# Create decks
deck1 = [
    PokemonCard("Charmander", "Fire", 60, "Water", is_ex=False, attacks=["30F"]),
    PokemonCard("Charmeleon", "Fire", 90, "Water", is_ex=False, attacks=["50FF"], evolves_from="Charmander"),
    PokemonCard("Charizard", "Fire", 200, "Water", is_ex=True, attacks=["200FFFF(discardEnergy(2F))"], evolves_from="Charmeleon"),
    TrainerCard("Misty"),
    TrainerCard("Potion"),
] * 4

deck2 = [
    PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"]),
    PokemonCard("Wartortle", "Water", 70, "Electric", is_ex=False, attacks=["40WW"], evolves_from="Squirtle"),
    PokemonCard("Blastoise", "Water", 180, "Electric", is_ex=True, attacks=["40"], evolves_from="Wartortle"),
    TrainerCard("Potion"),
    TrainerCard("Misty"),
] * 4

# Define energy colors
deck1_energy_colors = ["F"]
deck2_energy_colors = ["W"]

# Create players
player1 = Player(name="Ash", deck=deck1, energy_colors=deck1_energy_colors)
player2 = Player(name="Gary", deck=deck2, energy_colors=deck2_energy_colors)

# Logger instance
logger = Logger()

# Set up AI for player 1 and player 2
ai1 = BasicAI(player1, logger)
ai2 = BasicAI(player2, logger)

# Initialize the game
game = Game(player1, player2, verbose=True, ai1=ai1, ai2=ai2)

def main():
    game.start_game()
    while not game.game_state["ended"]:
        game.play_turn()

if __name__ == "__main__":
    main()