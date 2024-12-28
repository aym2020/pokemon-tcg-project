import random
from pokemon_card_game.player import Player
from pokemon_card_game.gameplay import generate_energy, attach_energy, perform_attack, evolve_pokemon
from pokemon_card_game.objects_effects import object_effects
from pokemon_card_game.card import PokemonCard
from pokemon_card_game.logger import Logger
from colorama import Fore

class Game:
    def __init__(self, player1, player2, verbose=True):
        """
        Initialize the game with two players.

        :param player1: Player 1 object.
        :param player2: Player 2 object.
        """
        self.players = [player1, player2]
        self.current_turn = None  # 0 for player1, 1 for player2
        self.turn_count = 0
        self.logger = Logger(verbose=verbose)
        self.game_state = {"winner": None, "ended": False}  # Track game state

    def end_game(self, winner_name):
        """
        Mark the game as ended and set the winner.
        """
        self.game_state["winner"] = winner_name
        self.game_state["ended"] = True
        self.logger.log(f"The game has ended. Winner: {winner_name}", color=Fore.RED)
        
    def coin_toss(self):
        """
        Determine who starts first using a coin toss.
        """
        self.logger.log("Coin toss: Heads or Tails?", color=Fore.CYAN)
        result = random.choice(["Heads", "Tails"])
        self.logger.log(f"Result: {result}", color=Fore.CYAN)
        self.current_turn = 0 if result == "Heads" else 1

    def shuffle_decks(self):
        """
        Shuffle each player's deck.
        """
        for player in self.players:
            random.shuffle(player.deck)
            self.logger.log(f"{player.name}'s deck shuffled.", color=Fore.YELLOW)

    def draw_initial_hands(self):
        """
        Ensure both players draw their initial 5-card hands, with at least one basic Pokémon.
        """
        for player in self.players:
            player.generate_first_hand(self.logger)

    def set_active_and_bench(self):
        for player in self.players:
            active_pokemon = next((card for card in player.hand if isinstance(card, PokemonCard) and not card.evolves_from), None)
            if active_pokemon:
                player.play_pokemon(active_pokemon, self.logger)  # `play_pokemon` now handles appending
                player.hand.remove(active_pokemon)

            bench_pokemon = [card for card in player.hand if isinstance(card, PokemonCard) and not card.evolves_from]
            for pokemon in bench_pokemon:
                if len(player.bench) < 3:
                    player.play_pokemon(pokemon, self.logger)  # `play_pokemon` now handles appending
                    player.hand.remove(pokemon)

    def start_game(self):
        """
        Start the game setup phase.
        """
        self.logger.log("The game begins!", color=Fore.CYAN)
        self.coin_toss()
        self.shuffle_decks()
        self.draw_initial_hands()
        self.set_active_and_bench()
    
    def status_check_phase(self):
        """
        Perform a status check phase at the end of the turn.
        Apply effects of statuses like poison.
        """
        for player in self.players:
            if player.active_pokemon and player.active_pokemon.status:
                player.active_pokemon.apply_status_effects(self.logger)
    
    def end_turn(self):
        """
        Handle the end-of-turn logic for the current player.
        """
        current_player = self.players[self.current_turn]

        # Perform status check phase
        self.status_check_phase()

        # Switch turn to the next player
        self.turn_count += 1
        self.current_turn = 1 - self.current_turn  # Switch to the other player

        # Clear newly played Pokémon
        current_player.clear_newly_played_and_evolved_pokemons()

        # Log the turn transition
        self.logger.log(f"End of turn {self.turn_count}. Next turn: {self.players[self.current_turn].name}'s turn.", color=Fore.MAGENTA)

    def log_game_state(self):
        """
        Log the current state of the game.
        """
        player1, player2 = self.players
        self.logger.log(f"Turn {self.turn_count + 1}: {self.players[self.current_turn].name}'s turn.", color=Fore.CYAN)
        self.logger.log(f"Scores - {player1.name}: {player1.prizes}, {player2.name}: {player2.prizes}", color=Fore.GREEN)
        self.logger.log(f"{player1.name}'s Active: {player1.active_pokemon}, Bench: {[p.name for p in player1.bench]}", color=Fore.BLUE)
        self.logger.log(f"{player2.name}'s Active: {player2.active_pokemon}, Bench: {[p.name for p in player2.bench]}", color=Fore.BLUE)

    def play_turn(self):
        """
        Execute a player's turn based on the turn count.
        """
        # Check if the game has already ended
        if self.game_state["ended"]:
            self.logger.log("The game has already ended.", color=Fore.RED)
            return

        current_player = self.players[self.current_turn]
        opponent = self.players[1 - self.current_turn]

        # Separator for the turn
        self.logger.separator(f"Turn {self.turn_count + 1}: {current_player.name}'s Turn", color=Fore.CYAN)

        # Log game state
        self.logger.log(f"Scores - {current_player.name}: {current_player.prizes}, {opponent.name}: {opponent.prizes}", color=Fore.GREEN)
        self.logger.log(f"{current_player.name}'s Hand: {[card.name for card in current_player.hand]}", color=Fore.BLUE)
        self.logger.log(f"{opponent.name}'s Hand: {[card.name for card in opponent.hand]}", color=Fore.BLUE)
        self.logger.log(f"{current_player.name}'s Active: {current_player.active_pokemon}", color=Fore.BLUE)
        self.logger.log(f"{opponent.name}'s Active: {opponent.active_pokemon}", color=Fore.BLUE)
        self.logger.log(f"{current_player.name}'s Bench: {[p.name for p in current_player.bench]}", color=Fore.YELLOW)
        self.logger.log(f"{opponent.name}'s Bench: {[p.name for p in opponent.bench]}", color=Fore.YELLOW)

        if self.turn_count == 0:
            self.logger.log("First turn: No card draw, energy generation, or evolution allowed.", color=Fore.MAGENTA)
        else:
            # Draw a card
            card = current_player.draw_card(self.logger)
            if card:
                self.logger.log(f"{current_player.name} drew {card.name}.", color=Fore.BLUE)

            # Generate and attach energy
            generated_energy = current_player.generate_energy(self.logger)
            if current_player.active_pokemon:
                attach_energy(current_player.active_pokemon, generated_energy, 1, self.logger)
                self.logger.log(f"{current_player.name} generated {generated_energy} energy.", color=Fore.BLUE)

        # Player actions
        for card in current_player.hand[:]:  # Iterate over a copy of the hand
            if card.card_category == "Pokemon":
                # Handle evolution
                if card.evolves_from:
                    basic_pokemon = next((p for p in [current_player.active_pokemon] + current_player.bench if p and p.name == card.evolves_from), None)
                    if basic_pokemon:
                        evolve_pokemon(current_player, basic_pokemon, card, self.logger, self.turn_count)
                else:
                    # Play a basic Pokémon
                    current_player.play_pokemon(card, self.logger)
                    self.logger.log(f"{current_player.name} played {card.name} on the field.", color=Fore.GREEN)
            elif card.card_category in ["Trainer", "Object"]:
                # Handle trainer or object card effects
                effect_function = object_effects.get(card.name)
                if effect_function:
                    self.logger.log(f"{current_player.name} used {card.name}.", color=Fore.YELLOW)
                    effect_function(current_player, opponent, self.logger)  # Pass the logger
                    current_player.hand.remove(card)

        # Attack if it's not the first turn
        if self.turn_count > 0:
            self.logger.log(f"{current_player.name} attacks!", color=Fore.MAGENTA)
            perform_attack(current_player, opponent, self.logger, self)  # Pass the game instance

        # Check for win condition
        if current_player.prizes >= 3:
            self.logger.separator("Game Over", color=Fore.RED)
            self.logger.critical(f"{current_player.name} wins the game!", color=Fore.RED)
            self.end_game(current_player.name)  # End the game instead of raising an exception
            return  # Skip further processing after the game ends

        # Handle end-of-turn logic
        self.end_turn()

