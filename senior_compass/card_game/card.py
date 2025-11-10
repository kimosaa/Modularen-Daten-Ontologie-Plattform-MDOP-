"""
Card class for the Senior Compass Card Game Module.

This module defines the Card class representing a single playing card.
"""


class Card:
    """Represents a single playing card with a suit and rank."""

    def __init__(self, suit: str, rank: str):
        """
        Initialize a Card with a suit and rank.

        Args:
            suit: The suit of the card (e.g., 'Hearts', 'Diamonds', 'Clubs', 'Spades')
            rank: The rank of the card (e.g., 'Ace', '2', '3', ..., 'King')
        """
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        """
        Returns a human-readable description of the card.

        Returns:
            A string representation of the card (e.g., 'Ace of Spades')
        """
        return f"{self.rank} of {self.suit}"

    def __repr__(self) -> str:
        """Returns a developer-friendly representation of the card."""
        return f"Card(suit='{self.suit}', rank='{self.rank}')"
