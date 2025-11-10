# Senior Compass Card Game Module

A simple, accessible card game implementation designed for senior users with clear, readable output suitable for the Senior Compass application.

## Overview

This module provides the core classes for card-based games:
- **Card**: Represents a single playing card
- **Deck**: A standard 52-card deck with shuffle and deal functionality
- **Player**: Represents a player with a hand of cards
- **Game**: Base game class that sets up and manages the game state

## Features

- ✅ Clean, modular design with separation of concerns
- ✅ Large, readable output format for accessibility
- ✅ Clear audio feedback messages for screen readers
- ✅ Comprehensive documentation and type hints
- ✅ Full test coverage
- ✅ Easy to extend for specific card games

## Installation

No external dependencies required! This module uses only Python standard library.

```bash
# Navigate to the card_game directory
cd senior_compass/card_game

# Run the demo
python demo.py

# Run tests
python ../tests/test_card_game.py
```

## Usage

### Basic Example

```python
from card_game import Game

# Create a new game
game = Game(player_name="Evelyn")

# Show the player's hand
game.player.show_hand()

# Draw another card
game.player.draw(game.deck)
game.player.show_hand()
```

### Creating Custom Games

You can extend the `Game` class to create specific card games:

```python
from card_game import Game

class Solitaire(Game):
    def __init__(self, player_name="Player"):
        super().__init__(player_name)
        # Add custom setup

    def play_turn(self):
        # Implement game-specific logic
        pass
```

## Class Documentation

### Card

Represents a single playing card.

```python
card = Card(suit='Hearts', rank='Ace')
print(card)  # Output: "Ace of Hearts"
```

**Attributes:**
- `suit` (str): The suit of the card (Hearts, Diamonds, Clubs, Spades)
- `rank` (str): The rank of the card (Ace, 2-10, Jack, Queen, King)

### Deck

Represents a standard 52-card deck.

```python
deck = Deck()
deck.shuffle()
card = deck.deal()
```

**Methods:**
- `shuffle()`: Randomizes the order of cards
- `deal()`: Returns and removes the top card, or None if empty
- `__len__()`: Returns the number of cards remaining

### Player

Represents a player with a hand of cards.

```python
player = Player(name="Alice")
player.draw(deck)
player.show_hand()
```

**Methods:**
- `draw(deck)`: Draws a card from the specified deck
- `show_hand()`: Displays all cards in a readable format
- `__len__()`: Returns the number of cards in hand

### Game

Base class for card games.

```python
game = Game(player_name="Bob")
game.setup_game()  # Called automatically
```

**Methods:**
- `setup_game()`: Shuffles deck and deals initial hand (7 cards)
- `start_loop_placeholder()`: Placeholder for game logic

## Output Example

```
[Senior Compass Card Game Setup]
Deck has been shuffled.
Dealing 7 cards to Evelyn...

--- Evelyn's Hand ---
1. Queen of Hearts
2. 7 of Diamonds
3. Ace of Spades
4. 4 of Clubs
5. King of Hearts
6. 9 of Diamonds
7. Jack of Clubs
--------------------

--- Gameplay Example ---
Evelyn draws a card.

--- Evelyn's Hand ---
1. Queen of Hearts
2. 7 of Diamonds
3. Ace of Spades
4. 4 of Clubs
5. King of Hearts
6. 9 of Diamonds
7. Jack of Clubs
8. 3 of Spades
--------------------

Game logic loop started. (Further game rules would be implemented here.)
Deck remaining: 44 cards.
```

## Accessibility Features

- **Large, Clear Text**: All output uses full card names (e.g., "Ace of Spades")
- **Simple Numbering**: Cards in hand are numbered 1, 2, 3...
- **Audio Feedback**: Messages designed for screen reader compatibility
- **High Contrast**: Text output suitable for display in high-contrast UI

## Testing

The module includes comprehensive unit tests covering:
- Card creation and representation
- Deck initialization, shuffling, and dealing
- Player hand management
- Game setup and initialization
- Integration scenarios

Run tests with:

```bash
cd senior_compass/tests
python test_card_game.py
```

## Design Principles

This module follows the same accessibility principles as the Senior Compass App:

1. **Visual Simplicity**: Clear, uncluttered output
2. **High Contrast**: Readable text descriptions
3. **Large Targets**: Easy-to-understand card representations
4. **Audio Feedback**: Messages suitable for voice output
5. **Error Prevention**: Graceful handling of edge cases (empty deck, etc.)

## Extension Ideas

This base module can be extended to implement:
- **Solitaire**: Classic single-player card game
- **Memory Match**: Card matching game for cognitive exercise
- **Go Fish**: Simple multiplayer game
- **War**: Automated two-player game

## License

Part of the Senior Compass App project.

## Version

1.0.0 - Initial implementation
