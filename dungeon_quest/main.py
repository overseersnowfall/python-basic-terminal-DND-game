"""
Dungeon Quest: ASCII Adventure
A text-based RPG game

Run this file to start the game!
"""

from game import Game


if __name__ == "__main__":
    print("Loading Dungeon Quest...")
    print("=" * 50)
    
    game = Game()
    game.run()
    
    print("\nThanks for playing!")