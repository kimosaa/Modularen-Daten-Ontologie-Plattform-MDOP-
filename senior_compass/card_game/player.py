"""
Player class for the Senior Compass Card Game Module.

This module defines the Player class representing a game player with a hand of cards.
"""

from typing import List

from .card import Card
from .deck import Deck


class Player:
    """Represents a player with a hand of cards."""

    def __init__(self, name: str = "Player"):
        """
        Initialize a player with a name and empty hand.

        Args:
            name: The name of the player (default: "Player")
        """
        self.name = name
        self.hand: List[Card] = []

    def draw(self, deck: Deck) -> bool:
        """
        Adds a card from the deck to the player's hand.

        Args:
            deck: The Deck object to draw from

        Returns:
            True if a card was successfully drawn, False if the deck is empty
        """
        card = deck.deal()
        if card:
            self.hand.append(card)
            return True
        return False  # Draw failed (deck empty)

    def show_hand(self):
        """
        Prints all cards in the player's hand in a clear, simple list.

        This method uses a large, readable format suitable for the
        Senior Compass UI with high contrast and clear numbering.
        """
        print(f"\n--- {self.name}'s Hand ---")
        if not self.hand:
            print("Hand is empty.")
            return

        # Simple, readable format suitable for the Senior Compass UI
        for i, card in enumerate(self.hand, 1):
            print(f"{i}. {card}")
        print("--------------------")

    def __len__(self) -> int:
        """Returns the number of cards in the player's hand."""
        return len(self.hand)

    def __repr__(self) -> str:
        """Returns a developer-friendly representation of the player."""
        return f"Player(name='{self.name}', cards_in_hand={len(self.hand)})"
