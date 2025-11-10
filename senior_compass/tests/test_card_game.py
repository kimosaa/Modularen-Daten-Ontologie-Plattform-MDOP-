"""
Unit tests for the Senior Compass Card Game Module

This test suite verifies the functionality of Card, Deck, Player, and Game classes.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from card_game.card import Card
from card_game.deck import Deck, SUITS, RANKS
from card_game.player import Player
from card_game.game import Game


class TestCard(unittest.TestCase):
    """Test cases for the Card class."""

    def test_card_creation(self):
        """Test that a card can be created with a suit and rank."""
        card = Card('Hearts', 'Ace')
        self.assertEqual(card.suit, 'Hearts')
        self.assertEqual(card.rank, 'Ace')

    def test_card_string_representation(self):
        """Test the string representation of a card."""
        card = Card('Spades', 'King')
        self.assertEqual(str(card), 'King of Spades')

    def test_card_repr(self):
        """Test the repr representation of a card."""
        card = Card('Diamonds', '10')
        self.assertEqual(repr(card), "Card(suit='Diamonds', rank='10')")


class TestDeck(unittest.TestCase):
    """Test cases for the Deck class."""

    def test_deck_creation(self):
        """Test that a new deck has 52 cards."""
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_contains_all_suits_and_ranks(self):
        """Test that the deck contains all suits and ranks."""
        deck = Deck()
        suits_found = set()
        ranks_found = set()

        for card in deck.cards:
            suits_found.add(card.suit)
            ranks_found.add(card.rank)

        self.assertEqual(suits_found, set(SUITS))
        self.assertEqual(ranks_found, set(RANKS))

    def test_deck_shuffle(self):
        """Test that shuffling changes the order of cards."""
        deck1 = Deck()
        original_order = [str(card) for card in deck1.cards]

        deck2 = Deck()
        deck2.shuffle()
        shuffled_order = [str(card) for card in deck2.cards]

        # It's extremely unlikely (but not impossible) for the orders to be the same
        self.assertNotEqual(original_order, shuffled_order)

    def test_deck_deal(self):
        """Test dealing a card from the deck."""
        deck = Deck()
        initial_count = len(deck.cards)
        card = deck.deal()

        self.assertIsNotNone(card)
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), initial_count - 1)

    def test_deck_deal_empty(self):
        """Test dealing from an empty deck returns None."""
        deck = Deck()
        # Deal all cards
        for _ in range(52):
            deck.deal()

        # Deck should now be empty
        self.assertEqual(len(deck.cards), 0)
        self.assertIsNone(deck.deal())

    def test_deck_len(self):
        """Test the __len__ method of Deck."""
        deck = Deck()
        self.assertEqual(len(deck), 52)
        deck.deal()
        self.assertEqual(len(deck), 51)


class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""

    def test_player_creation(self):
        """Test that a player can be created with a name."""
        player = Player("Alice")
        self.assertEqual(player.name, "Alice")
        self.assertEqual(len(player.hand), 0)

    def test_player_default_name(self):
        """Test that a player has a default name."""
        player = Player()
        self.assertEqual(player.name, "Player")

    def test_player_draw(self):
        """Test that a player can draw a card from a deck."""
        player = Player("Bob")
        deck = Deck()

        result = player.draw(deck)

        self.assertTrue(result)
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(len(deck.cards), 51)

    def test_player_draw_empty_deck(self):
        """Test that drawing from an empty deck fails gracefully."""
        player = Player("Charlie")
        deck = Deck()

        # Empty the deck
        for _ in range(52):
            deck.deal()

        result = player.draw(deck)

        self.assertFalse(result)
        self.assertEqual(len(player.hand), 0)

    def test_player_len(self):
        """Test the __len__ method of Player."""
        player = Player("Diana")
        deck = Deck()

        self.assertEqual(len(player), 0)
        player.draw(deck)
        self.assertEqual(len(player), 1)
        player.draw(deck)
        self.assertEqual(len(player), 2)

    def test_player_show_hand(self):
        """Test that show_hand doesn't crash (output test)."""
        player = Player("Eve")
        deck = Deck()

        # Should not crash with empty hand
        player.show_hand()

        # Draw some cards and show hand
        for _ in range(3):
            player.draw(deck)

        player.show_hand()  # Should print cards


class TestGame(unittest.TestCase):
    """Test cases for the Game class."""

    def test_game_creation(self):
        """Test that a game initializes properly."""
        game = Game("Frank")

        self.assertIsNotNone(game.deck)
        self.assertIsNotNone(game.player)
        self.assertEqual(game.player.name, "Frank")

    def test_game_default_player_name(self):
        """Test that a game has a default player name."""
        game = Game()
        self.assertEqual(game.player.name, "Evelyn")

    def test_game_initial_deal(self):
        """Test that the game deals 7 cards initially."""
        game = Game("Grace")

        # Player should have 7 cards after setup
        self.assertEqual(len(game.player.hand), 7)

        # Deck should have 45 cards remaining (52 - 7)
        self.assertEqual(len(game.deck.cards), 45)

    def test_game_deck_is_shuffled(self):
        """Test that the game deck is shuffled during setup."""
        # Create two games and check if decks are different
        game1 = Game("Helen")
        game2 = Game("Ivan")

        # Get the remaining cards from both decks
        deck1_cards = [str(card) for card in game1.deck.cards]
        deck2_cards = [str(card) for card in game2.deck.cards]

        # They should be different (extremely unlikely to be the same)
        self.assertNotEqual(deck1_cards, deck2_cards)


class TestIntegration(unittest.TestCase):
    """Integration tests for the card game module."""

    def test_complete_game_setup(self):
        """Test a complete game setup and initial gameplay."""
        # Create game
        game = Game("Julia")

        # Verify initial state
        self.assertEqual(len(game.player.hand), 7)
        self.assertEqual(len(game.deck.cards), 45)

        # Draw another card
        result = game.player.draw(game.deck)

        self.assertTrue(result)
        self.assertEqual(len(game.player.hand), 8)
        self.assertEqual(len(game.deck.cards), 44)

    def test_multiple_players_can_play(self):
        """Test that multiple players can draw from the same deck."""
        deck = Deck()
        player1 = Player("Kevin")
        player2 = Player("Laura")

        # Each player draws 5 cards
        for _ in range(5):
            player1.draw(deck)
            player2.draw(deck)

        self.assertEqual(len(player1.hand), 5)
        self.assertEqual(len(player2.hand), 5)
        self.assertEqual(len(deck.cards), 42)


def run_tests():
    """Run all tests with verbose output."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
