"""
Combat System
Handles turn-based combat between player and enemies
"""

import random
from typing import List
from player import Player
from enemy import Enemy
from display import GameScreen


class CombatSystem:
    """Handles turn-based combat"""
    
    def __init__(self, player: Player, enemy: Enemy, screen: GameScreen):
        self.player = player
        self.enemy = enemy
        self.screen = screen
        self.messages: List[str] = [f"A wild {enemy.name} appears!"]
        self.turn = 0
    
    def run_combat(self) -> bool:
        """
        Run the combat loop.
        Returns True if player won, False if player lost/fled
        """
        while self.player.stats.is_alive() and self.enemy.stats.is_alive():
            self.turn += 1
            
            # Render screen
            self.screen.render_combat_screen(self.player, self.enemy, self.messages)
            
            # Check if player is stunned
            if self.player.stats.is_stunned():
                self.messages.append(f"{self.player.name} is stunned and cannot act!")
                input("\nPress Enter to continue...")
                self._enemy_turn()
                self._end_of_turn()
                continue
            
            # Player's turn
            choice = input("\nYour choice: ").strip()
            
            if choice == '1':  # Basic Attack
                damage, msg = self.player.basic_attack(self.enemy)
                self.messages.append(msg)
                
                if not self.enemy.stats.is_alive():
                    return self._handle_victory()
                
                # Enemy's turn
                self._enemy_turn()
            
            elif choice == '2':  # Skills
                skill_used = self._handle_skills()
                
                if skill_used:
                    if not self.enemy.stats.is_alive():
                        return self._handle_victory()
                    
                    # Enemy's turn only if skill was used
                    self._enemy_turn()
                else:
                    continue  # Skill cancelled, don't advance turn
            
            elif choice == '3':  # Items
                item_used = self._handle_items()
                
                if item_used:
                    # Enemy's turn
                    self._enemy_turn()
                else:
                    continue  # No item used, don't advance turn
            
            elif choice == '4':  # Run
                if self._attempt_flee():
                    return False
                else:
                    # Failed to flee, enemy attacks
                    self._enemy_turn()
            
            # End of turn processing (status effects tick)
            self._end_of_turn()
        
        # If loop ends and player is dead
        if not self.player.stats.is_alive():
            self.messages.append(f"{self.player.name} has been defeated...")
            self.screen.render_combat_screen(self.player, self.enemy, self.messages)
            input("\nPress Enter to continue...")
            return False
        
        return True
    
    def _handle_skills(self) -> bool:
        """Show skill menu and use selected skill. Returns True if skill used."""
        self.screen.render_skill_menu(self.player)
        choice = input("\nChoose skill: ").strip()
        
        if choice == '0':
            return False  # Cancelled
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.skills):
                skill = self.player.skills[idx]
                damage, msg = self.player.use_skill(skill, self.enemy)
                
                if damage is None:
                    # Skill failed (not enough MP)
                    self.messages.append(msg)
                    input("\nPress Enter to continue...")
                    return False
                else:
                    self.messages.append(msg)
                    return True
        
        return False
    
    def _handle_items(self) -> bool:
        """Show inventory and use selected item. Returns True if item used."""
        if not self.player.inventory:
            print("You have no items!")
            input("Press Enter to continue...")
            return False
        
        self.screen.render_inventory_menu(self.player)
        choice = input("\nUse item: ").strip()
        
        if choice == '0':
            return False  # Cancelled
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.player.inventory):
                item = self.player.inventory[idx]
                result = self.player.use_item(item.name)
                if result:
                    self.messages.append(result)
                    return True
        
        return False
    
    def _enemy_turn(self):
        """Enemy attacks the player"""
        # Check if enemy is stunned
        if self.enemy.stats.is_stunned():
            self.messages.append(f"{self.enemy.name} is stunned and cannot act!")
            return
        
        # Enemy uses basic attack (you can add AI for skills later!)
        damage, msg = self.enemy.basic_attack(self.player)
        self.messages.append(msg)
    
    def _end_of_turn(self):
        """Process end-of-turn effects (status effects tick)"""
        # Player status effects
        player_messages = self.player.stats.tick_status_effects()
        self.messages.extend(player_messages)
        
        # Enemy status effects
        enemy_messages = self.enemy.stats.tick_status_effects()
        self.messages.extend(enemy_messages)
    
    def _attempt_flee(self) -> bool:
        """Try to run away. 50% chance."""
        if random.random() < 0.5:
            self.messages.append(f"{self.player.name} successfully fled!")
            input("\nPress Enter to continue...")
            return True
        else:
            self.messages.append(f"{self.player.name} couldn't escape!")
            return False
    
    def _handle_victory(self) -> bool:
        """Handle enemy defeat - give rewards"""
        self.messages.append(f"{self.enemy.name} defeated!")
        
        # Store old level before gaining exp
        old_level = self.player.stats.level
        
        # Give rewards
        self.player.gain_exp(self.enemy.exp_reward)
        self.player.gold += self.enemy.gold_reward
        
        reward_msg = f"Gained {self.enemy.exp_reward} EXP and {self.enemy.gold_reward} gold!"
        self.messages.append(reward_msg)
        
        # Check if leveled up by comparing old and new level
        if self.player.stats.level > old_level:
            self.messages.append(f"[LEVEL UP!] Now level {self.player.stats.level}!")
        
        self.screen.render_combat_screen(self.player, self.enemy, self.messages)
        input("\nPress Enter to continue...")
        return True