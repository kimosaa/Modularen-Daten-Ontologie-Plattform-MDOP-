"""
Game class for the Senior Compass Card Game Module.

This module defines the Game class, a foundational class for card games
that sets up the deck and player(s).
"""

from .deck import Deck
from .player import Player


class Game:
    """
    A foundational class for card games, setting up the deck and player.
    This serves as the base setup for games like Solitaire.
    """

    def __init__(self, player_name: str = "Evelyn"):
        """
        Initialize a new game with a deck and player.

        Args:
            player_name: The name of the player (default: "Evelyn")
        """
        self.deck = Deck()
        self.player = Player(player_name)
        self.setup_game()

    def setup_game(self):
        """
        Sets up the initial state: shuffles the deck and deals the starting hand.

        Deals 7 cards to the player as the initial hand size.
        Provides clear audio feedback for accessibility.
        """
        print("\n[Senior Compass Card Game Setup]")
        self.deck.shuffle()

        # Deal initial hand of 7 cards
        initial_deal_size = 7
        print(f"Dealing {initial_deal_size} cards to {self.player.name}...")
        for _ in range(initial_deal_size):
            self.player.draw(self.deck)

    def start_loop_placeholder(self):
        """
        Placeholder for the main game logic loop.

        This method is intended to be overridden by specific game implementations
        that inherit from this base Game class.
        """
        print("\nGame logic loop started. (Further game rules would be implemented here.)")
        # Example of a turn:
        # while game_is_active:
        #     action = self.get_player_action()
        #     self.process_action(action)
        print(f"Deck remaining: {len(self.deck.cards)} cards.")

    def __repr__(self) -> str:
        """Returns a developer-friendly representation of the game state."""
        return f"Game(player='{self.player.name}', deck_remaining={len(self.deck.cards)}, player_hand={len(self.player.hand)})"
