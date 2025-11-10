"""
Deck class for the Senior Compass Card Game Module.

This module defines the Deck class representing a standard 52-card deck.
"""

import random
from typing import List, Optional

from .card import Card


# Configuration for standard deck
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']


class Deck:
    """Represents a standard 52-card deck."""

    def __init__(self):
        """Initialize a new deck with all 52 cards."""
        # Generates a full deck of 52 Card objects
        self.cards: List[Card] = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        """
        Randomizes the order of the cards in the deck.

        Provides audio feedback message suitable for accessibility.
        """
        random.shuffle(self.cards)
        print("Deck has been shuffled.")

    def deal(self) -> Optional[Card]:
        """
        Removes and returns a single card from the top of the deck.

        Returns:
            A Card object if the deck is not empty, None otherwise.
        """
        if not self.cards:
            return None  # Deck is empty
        return self.cards.pop()

    def __len__(self) -> int:
        """Returns the number of cards remaining in the deck."""
        return len(self.cards)

    def __repr__(self) -> str:
        """Returns a developer-friendly representation of the deck."""
        return f"Deck(cards_remaining={len(self.cards)})"
