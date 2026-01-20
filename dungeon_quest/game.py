"""
Game Controller
Main game loop and state management
"""

import time
import random
from typing import Optional, List
from display import Display, GameScreen
from player import Player, Warrior, Wizard, Ranger, Thief
from enemy import Enemy, create_enemy_database
from combat import CombatSystem
from stats import Stats, Item


class Game:
    """Main game controller - ties everything together"""
    
    def __init__(self):
        self.screen = GameScreen()
        self.player: Optional[Player] = None
        self.enemies = create_enemy_database()
        self.game_state = "menu"  # "menu", "exploring", "combat", "game_over"
    
    def main_menu(self) -> bool:
        """Display main menu. Returns False to quit game."""
        Display.clear_screen()
        
        print("\n" * 5)
        print(Display.center_text("╔═══════════════════════════════════╗", self.screen.width))
        print(Display.center_text("║   DUNGEON QUEST: ASCII ADVENTURE  ║", self.screen.width))
        print(Display.center_text("╚═══════════════════════════════════╝", self.screen.width))
        print("\n" * 2)
        print(Display.center_text("[1] New Game", self.screen.width))
        print(Display.center_text("[2] Quit", self.screen.width))
        print("\n")
        
        choice = input(Display.center_text("Select: ", self.screen.width)).strip()
        
        if choice == '1':
            self.player = self._create_player()
            self.game_state = "exploring"
            return True
        elif choice == '2':
            return False
        
        return True
    
    def _create_player(self) -> Player:
        """Character creation"""
        Display.clear_screen()
        
        print("\n" + "=" * 50)
        print("CHARACTER CREATION".center(50))
        print("=" * 50 + "\n")
        
        name = input("Enter your hero's name: ").strip() or "Hero"
        
        print("\nChoose your class:")
        print("  [1] Warrior - High HP, powerful physical attacks")
        print("  [2] Ranger  - Balanced, quick ranged attacks")
        print("  [3] Wizard  - High MP, devastating magic")
        print("  [4] Thief   - High speed, critical strikes")
        
        while True:
            choice = input("\nClass choice (1-4): ").strip()
            
            if choice == '1':
                player = Warrior(name)
                break
            elif choice == '2':
                player = Ranger(name)
                break
            elif choice == '3':
                player = Wizard(name)
                break
            elif choice == '4':
                player = Thief(name)
                break
            else:
                print("Invalid choice!")
        
        # Starting items
        player.add_item(Item("Health Potion", "Restores 40 HP", "potion", {"hp": 40}))
        player.add_item(Item("Mana Potion", "Restores 30 MP", "ether", {"mp": 30}))
        player.add_item(Item("Health Potion", "Restores 40 HP", "potion", {"hp": 40}))
        
        print(f"\n{player.name} the {player.class_name} is ready for adventure!")
        time.sleep(2)
        
        return player
    
    def exploration_loop(self):
        """Main exploration gameplay"""
        story = ("You enter the dark dungeon. The air is thick with the smell of decay. "
                "Torch light flickers on ancient stone walls. What will you do?")
        options = ["Explore deeper", "Search for treasure", "Rest at campfire", "Exit dungeon"]
        
        while self.game_state == "exploring":
            self.screen.render_exploration_screen(self.player, story, options)
            choice = input("\nYour choice: ").strip()
            
            if choice == '1':  # Explore - random encounter
                if random.random() < 0.7:  # 70% chance of enemy
                    enemy_template = random.choice(self.enemies)
                    
                    # Create fresh enemy (reset HP)
                    enemy = Enemy(
                        enemy_template.name,
                        Stats(
                            enemy_template.stats.max_hp, 
                            enemy_template.stats.max_hp,
                            enemy_template.stats.max_mp, 
                            enemy_template.stats.max_mp,
                            enemy_template.stats.attack, 
                            enemy_template.stats.speed,
                            enemy_template.stats.level
                        ),
                        enemy_template.ascii_art, 
                        enemy_template.exp_reward, 
                        enemy_template.gold_reward
                    )
                    
                    combat = CombatSystem(self.player, enemy, self.screen)
                    won = combat.run_combat()
                    
                    if not won and not self.player.stats.is_alive():
                        self.game_state = "game_over"
                        break
                    
                    story = "You defeated the enemy and continue exploring."
                else:
                    story = "You find an empty chamber. The silence is eerie."
                    time.sleep(2)
            
            elif choice == '2':  # Search
                if random.random() < 0.4:
                    gold = random.randint(10, 30)
                    self.player.gold += gold
                    story = f"You found {gold} gold hidden in a dusty chest!"
                else:
                    story = "You search thoroughly but find nothing of value."
                time.sleep(2)
            
            elif choice == '3':  # Rest
                heal = self.player.stats.max_hp // 3
                mp_restore = self.player.stats.max_mp // 2
                self.player.stats.heal(heal)
                self.player.stats.restore_mp(mp_restore)
                story = f"You rest by the campfire. Recovered {heal} HP and {mp_restore} MP."
                time.sleep(2)
            
            elif choice == '4':  # Exit
                self.game_state = "menu"
                break
    
    def run(self):
        """Main game loop - this is what you call to start the game!"""
        running = True
        
        while running:
            if self.game_state == "menu":
                running = self.main_menu()
            
            elif self.game_state == "exploring":
                self.exploration_loop()
            
            elif self.game_state == "game_over":
                Display.clear_screen()
                print("\n" * 10)
                print(Display.center_text("╔══════════════╗", self.screen.width))
                print(Display.center_text("║  GAME OVER   ║", self.screen.width))
                print(Display.center_text("╚══════════════╝", self.screen.width))
                input("\nPress Enter to return to menu...")
                self.game_state = "menu"
                # Reset player
                self.player = None
