"""
Senior Compass Card Game Module

A simple, accessible card game implementation designed for senior users.
This module provides the core classes for card-based games with clear,
readable output suitable for the Senior Compass application.
"""

from .card import Card
from .deck import Deck
from .player import Player
from .game import Game

__all__ = ['Card', 'Deck', 'Player', 'Game']
__version__ = '1.0.0'
