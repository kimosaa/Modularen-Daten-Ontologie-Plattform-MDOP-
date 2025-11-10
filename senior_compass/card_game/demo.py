"""
Demonstration of the Senior Compass Card Game Module

This script demonstrates the functionality of the card game module,
showing how to create a game, deal cards, and interact with the player's hand.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from card_game import Game


def main():
    """Main demonstration function."""
    # 1. Create a new Game instance (which creates and shuffles a deck)
    print("=" * 50)
    print("Senior Compass Card Game - Demonstration")
    print("=" * 50)

    solitaire_game = Game(player_name="Evelyn")

    # 2. The player and the initial hand of 7 cards have already been created and dealt
    # in the Game.__init__ and Game.setup_game methods.

    # 3. Printing the player's hand in a simple, readable format
    solitaire_game.player.show_hand()

    # Example of a player drawing another card during gameplay
    print("\n--- Gameplay Example ---")
    if solitaire_game.player.draw(solitaire_game.deck):
        print("Evelyn draws a card.")
        solitaire_game.player.show_hand()
    else:
        print("Cannot draw - deck is empty!")

    # Placeholder for the main game loop
    solitaire_game.start_loop_placeholder()

    # Show final game state
    print(f"\nFinal State: {solitaire_game}")


if __name__ == "__main__":
    main()
