"""
Game Data Structures
Stats, StatusEffect, Skill, and Item classes
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class StatusEffect:
    """A temporary status effect (buff/debuff/DOT)"""
    name: str           # "Poison", "Burn", "Attack Buff", etc.
    effect_type: str    # "stat_mod", "damage_over_time", "stun", etc.
    stat_affected: str = ""  # "attack", "speed", etc. (for stat_mod type)
    power: int = 0      # Amount (+5 attack, -3 speed, 10 poison damage, etc.)
    duration: int = 0   # Turns remaining
    
    def tick(self) -> bool:
        """
        Reduce duration by 1 turn.
        Returns True if effect is still active, False if expired.
        """
        self.duration -= 1
        return self.duration > 0


@dataclass
class Stats:
    """Character statistics"""
    hp: int
    max_hp: int
    mp: int
    max_mp: int
    attack: int
    speed: int
    level: int = 1
    exp: int = 0
    
    # Status effects list - can hold any number of effects!
    status_effects: List[StatusEffect] = None
    
    def __post_init__(self):
        """Initialize mutable default (can't do in dataclass directly)"""
        if self.status_effects is None:
            self.status_effects = []
    
    def add_status_effect(self, effect: StatusEffect):
        """Add a new status effect"""
        # Check if same type of effect already exists
        for existing in self.status_effects:
            if existing.name == effect.name:
                # Refresh duration (take the longer one)
                existing.duration = max(existing.duration, effect.duration)
                # Stack power (for things like multiple poisons)
                if effect.effect_type == "damage_over_time":
                    existing.power += effect.power
                return
        
        # Add new effect
        self.status_effects.append(effect)
    
    def remove_status_effect(self, effect_name: str):
        """Remove a status effect by name"""
        self.status_effects = [e for e in self.status_effects if e.name != effect_name]
    
    def get_stat_modifier(self, stat_name: str) -> int:
        """Get total modifier for a stat from all effects"""
        total = 0
        for effect in self.status_effects:
            if effect.effect_type == "stat_mod" and effect.stat_affected == stat_name:
                total += effect.power
        return total
    
    def get_effective_attack(self) -> int:
        """Get attack with all modifiers applied"""
        return max(1, self.attack + self.get_stat_modifier("attack"))
    
    def get_effective_speed(self) -> int:
        """Get speed with all modifiers applied"""
        return max(1, self.speed + self.get_stat_modifier("speed"))
    
    def is_stunned(self) -> bool:
        """Check if character is stunned"""
        return any(e.effect_type == "stun" for e in self.status_effects)
    
    def tick_status_effects(self) -> List[str]:
        """
        Process all status effects for one turn.
        Returns list of messages about what happened.
        """
        messages = []
        effects_to_remove = []
        
        for effect in self.status_effects:
            # Handle damage over time (poison, burn, etc.)
            if effect.effect_type == "damage_over_time":
                damage = self.take_damage(effect.power)
                messages.append(f"[DOT] {effect.name} deals {damage} damage!")
            
            # Tick down duration
            if not effect.tick():
                effects_to_remove.append(effect.name)
                messages.append(f"[*] {effect.name} wore off!")
        
        # Remove expired effects
        for name in effects_to_remove:
            self.remove_status_effect(name)
        
        return messages
    
    def get_status_effects_text(self) -> str:
        """Get text description of all active effects"""
        if not self.status_effects:
            return "None"
        
        effect_strings = []
        for effect in self.status_effects:
            if effect.effect_type == "stat_mod":
                sign = "+" if effect.power > 0 else ""
                effect_strings.append(f"{effect.name} {sign}{effect.power} ({effect.duration}t)")
            elif effect.effect_type == "damage_over_time":
                effect_strings.append(f"{effect.name} {effect.power}/turn ({effect.duration}t)")
            elif effect.effect_type == "stun":
                effect_strings.append(f"{effect.name} ({effect.duration}t)")
        
        return ", ".join(effect_strings)
    
    def take_damage(self, damage: int) -> int:
        actual_damage = max(1, damage)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        actual_heal = max(1, amount)
        self.hp = min(self.max_hp, self.hp + amount)
        return actual_heal

    def is_alive(self) -> bool:
        return self.hp > 0
    
    def use_mp(self, amount: int) -> bool:
        """
        Try to use MP. Returns True if successful, False if not enough MP.
        """
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False
    
    def restore_mp(self, amount: int):
        """Restore MP, not exceeding max"""
        self.mp = min(self.max_mp, self.mp + amount)


@dataclass
class Skill:
    """A skill/spell that costs MP to use"""
    name: str
    description: str
    mp_cost: int
    skill_type: str  # "damage", "heal", "buff", "debuff", "dot", "stun"
    power: float = 0.0
    duration: int = 0
    status_effect: Optional[str] = None  # "poison", "burn", "stun", etc.


@dataclass
class Item:
    """Game items - potions, keys, etc."""
    name: str
    description: str
    item_type: str  # 'potion', 'ether', 'key', etc.
    effect: Dict = None  # e.g., {'hp': 40} or {'mp': 30}