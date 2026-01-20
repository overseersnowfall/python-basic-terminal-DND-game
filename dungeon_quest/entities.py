"""
Base Entity Class
Parent class for all game characters (Players and Enemies)
"""

import random
from typing import Tuple
from stats import Stats


class Entity:
    """Base class for all game characters"""
    
    def __init__(self, name: str, stats: Stats, ascii_art: str = ""):
        self.name = name
        self.stats = stats
        self.ascii_art = ascii_art
    
    def basic_attack(self, target: 'Entity') -> Tuple[int, str]:
        """Attack another entity using effective attack (with buffs/debuffs)"""
        # Use effective attack (includes buffs/debuffs)
        effective_attack = self.stats.get_effective_attack()
        damage = int(effective_attack * random.uniform(0.8, 1.2))
        actual_damage = target.stats.take_damage(damage)
        message = f"{self.name} attacks {target.name} for {actual_damage} damage!"
        return actual_damage, message