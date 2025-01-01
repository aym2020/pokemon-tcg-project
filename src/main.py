from pokemon_card_game.card import Card
from pokemon_card_game.card  import PokemonCard, TrainerCard, ObjectCard
from pokemon_card_game.player import Player
from pokemon_card_game.game import Game, Logger 
from pokemon_card_game.ai import BasicAI

# Create decks
deck1 = [
    PokemonCard("Ponyta", "Fire", 60, "Water", is_ex=False, attacks=["20F"], subcategory="Basic"),
    PokemonCard("Rapidash", "Fire", 100, "Water", is_ex=False, attacks=["40F"], evolves_from="Ponyta", subcategory="Stage 1"),
    ObjectCard("Poké Ball"),
    TrainerCard("Blue"),
] * 5

deck2 = [
    PokemonCard("Squirtle", "Water", 50, "Electric", is_ex=False, attacks=["20W"], subcategory="Basic"),
    PokemonCard("Wartortle", "Water", 70, "Electric", is_ex=False, attacks=["40WW"], evolves_from="Squirtle", subcategory="Stage 1"),
    PokemonCard("Blastoise", "Water", 180, "Electric", is_ex=True, attacks=["40"], evolves_from="Wartortle", subcategory="Stage 2"),
    ObjectCard("Poké Ball"),
    TrainerCard("Giovanni"),
] * 4

 # Deck Grass
deck3 = [
    PokemonCard("Bulbasaur", "Grass", 60, "Fire", is_ex=False, attacks=["20G"], subcategory="Basic"),
    PokemonCard("Ivysaur", "Grass", 100, "Fire", is_ex=False, attacks=["40G"], evolves_from="Bulbasaur", subcategory="Stage 1"),
    PokemonCard("Venusaur", "Grass", 180, "Fire", is_ex=True, attacks=["120GGG"], evolves_from="Ivysaur", subcategory="Stage 2"),
    ObjectCard("Poké Ball"),
    TrainerCard("Erika"),
] * 4
    
# Define energy colors
deck1_energy_colors = ["F"]
deck2_energy_colors = ["W"]
deck3_energy_colors = ["G"]

# Create players
player1 = Player(name="Ash", deck=deck1, energy_colors=deck1_energy_colors)
player2 = Player(name="Gary", deck=deck3, energy_colors=deck3_energy_colors)

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