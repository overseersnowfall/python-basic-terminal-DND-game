"""
Enemy Class
Enemies that the player fights
"""

from typing import List
from entities import Entity
from stats import Stats
import ascii_art


class Enemy(Entity):
    """Enemy character - drops EXP and gold when defeated"""
    
    def __init__(self, name: str, stats: Stats, ascii_art: str, 
                 exp_reward: int, gold_reward: int):
        # Call parent (Entity) constructor
        super().__init__(name, stats, ascii_art)
        
        # Add enemy-specific attributes
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward


# ============================================================================
# ENEMY DATABASE
# ============================================================================

def create_enemy_database() -> List[Enemy]:
    """Create all enemies in the game - ADD NEW ENEMIES HERE"""
    
    return [
        Enemy(
            name="Goblin Scout",
            stats=Stats(hp=40, max_hp=40, mp=10, max_mp=10, 
                       attack=10, speed=8),
            ascii_art=ascii_art.GOBLIN,
            exp_reward=30,
            gold_reward=15
        ),
        Enemy(
            name="Orc Warrior",
            stats=Stats(hp=80, max_hp=80, mp=20, max_mp=20, 
                       attack=18, speed=6, level=3),
            ascii_art=ascii_art.ORC,
            exp_reward=75,
            gold_reward=35
        ),
        Enemy(
            name="Skeleton Archer",
            stats=Stats(hp=60, max_hp=60, mp=15, max_mp=15,
                       attack=14, speed=10, level=2),
            ascii_art=ascii_art.SKELETON,
            exp_reward=50,
            gold_reward=25
        ),
        Enemy(
            name="Slime",
            stats=Stats(hp=30, max_hp=30, mp=5, max_mp=5,
                       attack=6, speed=4, level=1),
            ascii_art=ascii_art.SLIME,
            exp_reward=20,
            gold_reward=10
        ),
        # ADD MORE ENEMIES HERE
        # Enemy(
        #     name="Ancient Dragon",
        #     stats=Stats(hp=200, max_hp=200, mp=50, max_mp=50,
        #                attack=30, speed=12, level=10),
        #     ascii_art=ascii_art.DRAGON,
        #     exp_reward=500,
        #     gold_reward=200
        # ),
    ]
