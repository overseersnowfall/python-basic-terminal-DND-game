"""
Player Classes
All playable character classes: Warrior, Wizard, Ranger, Thief
"""

import random
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from entities import Entity
from stats import Stats, Skill, Item, StatusEffect


class Player(Entity, ABC):
    """
    Base Player class - must be subclassed (Warrior, Wizard, etc.)
    ABC = Abstract Base Class
    """
    
    def __init__(self, name: str, stats: Stats, class_name: str, ascii_art: str = ""):
        # Call Entity constructor
        super().__init__(name, stats, ascii_art)
        
        # Add player-specific attributes
        self.class_name = class_name
        self.inventory: List[Item] = []
        self.skills: List[Skill] = []
        self.gold: int = 0
        
        # Each subclass will define their own skills
        self._init_skills()
    
    @abstractmethod
    def _init_skills(self):
        """
        Each player class (Warrior, Wizard, etc.) must implement this
        This is where they add their unique skills
        """
        pass
    
    def gain_exp(self, exp: int):
        """Gain experience points"""
        self.stats.exp += exp
        exp_needed = self.stats.level * 100
        
        # Level up if enough exp
        if self.stats.exp >= exp_needed:
            self.level_up()
    
    def level_up(self):
        """Increase level and stats"""
        self.stats.level += 1
        self.stats.max_hp += int(self.stats.max_hp * 0.1)  # Increase max HP by 10%
        self.stats.max_mp += int(self.stats.max_mp * 0.1)  # Increase max MP by 10%
        self.stats.hp = self.stats.max_hp  # Full heal on level up
        self.stats.mp = self.stats.max_mp
        self.stats.attack += int(self.stats.attack * 0.1)  # Increase attack by 10%
        self.stats.speed += 1
        
        # Don't print here - let combat system handle the message

    def add_item(self, item: Item):
        """Add item to inventory"""
        self.inventory.append(item)
    
    def use_item(self, item_name: str) -> Optional[str]:
        """Use an item from inventory"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if item.effect:
                    # Health potion
                    if 'hp' in item.effect:
                        self.stats.heal(item.effect['hp'])
                        self.inventory.remove(item)
                        return f"Used {item.name}! Restored {item.effect['hp']} HP."
                    # Mana potion
                    elif 'mp' in item.effect:
                        self.stats.restore_mp(item.effect['mp'])
                        self.inventory.remove(item)
                        return f"Used {item.name}! Restored {item.effect['mp']} MP."
                return f"Used {item.name}."
        return None

    def use_skill(self, skill: Skill, target: Entity) -> Tuple[Optional[int], str]:
        """Use a skill on a target"""
        # Check MP
        if not self.stats.use_mp(skill.mp_cost):
            return None, f"Not enough MP! Need {skill.mp_cost} MP."
        
        effect_amount = int(self.stats.attack * skill.power)
        
        if skill.skill_type == "damage":
            # Direct damage
            damage = int(effect_amount * random.uniform(0.9, 1.1))
            actual_damage = target.stats.take_damage(damage)
            message = f"{self.name} uses {skill.name}! Deals {actual_damage} damage!"
            return actual_damage, message
        
        elif skill.skill_type == "heal":
            # Healing
            heal_amount = effect_amount
            target.stats.heal(heal_amount)
            message = f"{self.name} uses {skill.name}! Restored {heal_amount} HP!"
            return 0, message
        
        elif skill.skill_type == "buff":
            # Buff - increase caster's stats (self-buff)
            buff_amount = max(1, effect_amount)
            effect = StatusEffect(
                name=f"{skill.name}",
                effect_type="stat_mod",
                stat_affected="attack",
                power=buff_amount,
                duration=skill.duration
            )
            self.stats.add_status_effect(effect)  # Apply to self, not target!
            message = f"{self.name} uses {skill.name}! Attack +{buff_amount} for {skill.duration} turns!"
            return 0, message
        
        elif skill.skill_type == "debuff":
            # Debuff - decrease target's stats
            debuff_amount = max(1, effect_amount)
            effect = StatusEffect(
                name=f"{skill.name}",
                effect_type="stat_mod",
                stat_affected="attack",
                power=-debuff_amount,
                duration=skill.duration
            )
            target.stats.add_status_effect(effect)
            message = f"{self.name} uses {skill.name}! {target.name}'s attack -{debuff_amount} for {skill.duration} turns!"
            return 0, message
        
        elif skill.skill_type == "dot":
            # Damage over time (poison, burn, bleed, etc.)
            dot_damage = max(1, effect_amount)
            effect = StatusEffect(
                name=skill.status_effect or skill.name,
                effect_type="damage_over_time",
                power=dot_damage,
                duration=skill.duration
            )
            target.stats.add_status_effect(effect)
            message = f"{self.name} uses {skill.name}! {target.name} is afflicted with {effect.name}!"
            return 0, message
        
        elif skill.skill_type == "stun":
            # Stun effect
            effect = StatusEffect(
                name="Stunned",
                effect_type="stun",
                duration=skill.duration
            )
            target.stats.add_status_effect(effect)
            message = f"{self.name} uses {skill.name}! {target.name} is stunned for {skill.duration} turns!"
            return 0, message
        
        else:
            return None, f"Unknown skill type: {skill.skill_type}"


# ============================================================================
# PLAYER CLASSES
# ============================================================================

class Warrior(Player):
    """Warrior - High HP, powerful physical attacks"""
    
    def __init__(self, name: str):
        stats = Stats(
            hp=120, max_hp=120,
            mp=30, max_mp=30,
            attack=18,
            speed=8
        )
        super().__init__(name, stats, "Warrior")
    
    def _init_skills(self):
        """Warrior gets physical damage skills and buffs"""
        self.skills = [
            Skill(
                name="Power Strike",
                description="Heavy attack dealing 150% damage",
                mp_cost=10,
                skill_type="damage",
                power=1.5
            ),
            Skill(
                name="Whirlwind",
                description="Spinning attack dealing 200% damage",
                mp_cost=20,
                skill_type="damage",
                power=2.0
            ),
            Skill(
                name="Battle Cry",
                description="Boost attack by 30% for 3 turns",
                mp_cost=15,
                skill_type="buff",
                power=0.3,
                duration=3
            ),
        ]


class Wizard(Player):
    """Wizard - High MP, powerful magic attacks"""
    
    def __init__(self, name: str):
        stats = Stats(
            hp=80, max_hp=80,
            mp=60, max_mp=60,
            attack=12,
            speed=10
        )
        super().__init__(name, stats, "Wizard")
    
    def _init_skills(self):
        """Wizard gets various magic types"""
        self.skills = [
            Skill(
                name="Fireball",
                description="Fire spell dealing 160% damage",
                mp_cost=12,
                skill_type="damage",
                power=1.6
            ),
            Skill(
                name="Poison Cloud",
                description="Poison enemy for 50% attack/turn for 3 turns",
                mp_cost=15,
                skill_type="dot",
                power=0.5,
                duration=3,
                status_effect="Poison"
            ),
            Skill(
                name="Flame Curse",
                description="Burn enemy for 40% attack/turn for 4 turns",
                mp_cost=18,
                skill_type="dot",
                power=0.4,
                duration=4,
                status_effect="Burn"
            ),
            Skill(
                name="Heal",
                description="Restore HP based on 80% of attack",
                mp_cost=15,
                skill_type="heal",
                power=0.8
            ),
        ]


class Ranger(Player):
    """Ranger - Balanced stats, ranged attacks"""
    
    def __init__(self, name: str):
        stats = Stats(
            hp=100, max_hp=100,
            mp=40, max_mp=40,
            attack=15,
            speed=12
        )
        super().__init__(name, stats, "Ranger")
    
    def _init_skills(self):
        """Ranger gets precision attacks"""
        self.skills = [
            Skill(
                name="Rapid Shot",
                description="Quick attack dealing 130% damage",
                mp_cost=8,
                skill_type="damage",
                power=1.3
            ),
            Skill(
                name="Piercing Arrow",
                description="Armor-piercing shot dealing 180% damage",
                mp_cost=15,
                skill_type="damage",
                power=1.8
            ),
        ]


class Thief(Player):
    """Thief - High speed, status effects and crits"""
    
    def __init__(self, name: str):
        stats = Stats(
            hp=90, max_hp=90,
            mp=35, max_mp=35,
            attack=14,
            speed=15
        )
        super().__init__(name, stats, "Thief")
    
    def _init_skills(self):
        """Thief gets bleed and stun effects"""
        self.skills = [
            Skill(
                name="Backstab",
                description="Critical strike dealing 170% damage",
                mp_cost=10,
                skill_type="damage",
                power=1.7
            ),
            Skill(
                name="Poison Blade",
                description="Attack that poisons for 60% attack/turn for 3 turns",
                mp_cost=12,
                skill_type="dot",
                power=0.6,
                duration=3,
                status_effect="Poison"
            ),
            Skill(
                name="Stunning Strike",
                description="Stun enemy for 1 turn",
                mp_cost=15,
                skill_type="stun",
                duration=1
            ),
        ]