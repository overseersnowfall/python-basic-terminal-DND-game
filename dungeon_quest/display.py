"""
Display System
Handles terminal rendering and screen layouts
"""

import os
from typing import Tuple, List
from player import Player
from enemy import Enemy


class Display:
    """Helper methods for terminal display"""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """Get terminal dimensions - Returns: (width, height)"""
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except:
            return 100, 30  # Fallback
    
    @staticmethod
    def center_text(text: str, width: int) -> str:
        """Center text within given width"""
        padding = (width - len(text)) // 2
        return " " * padding + text
    
    @staticmethod
    def render_ascii_art(art: str, width: int) -> List[str]:
        """Prepare ASCII art for display, centered in the given width"""
        lines = art.split('\n')
        centered_lines = []
        
        for line in lines:
            if len(line) < width - 4:
                centered_lines.append(Display.center_text(line, width - 2))
            else:
                centered_lines.append(line[:width-4])
        
        return centered_lines


class GameScreen:
    """Manages the split-screen game layout"""
    
    def __init__(self):
        self.width, self.height = Display.get_terminal_size()
        
        # Screen divisions
        self.visual_height = int(self.height * 0.4)  # 40% for enemy/scene
        self.stats_height = 8  # Fixed 8 lines for stats
        self.story_height = self.height - self.visual_height - self.stats_height - 4
    
    def _draw_horizontal_line(self, style: str = "double") -> str:
        """Draw a horizontal divider line"""
        if style == "double":
            return "╠" + "═" * (self.width - 2) + "╣"
        else:
            return "├" + "─" * (self.width - 2) + "┤"
    
    def render_combat_screen(self, player: Player, enemy: Enemy, messages: List[str]):
        """Render the combat view"""
        Display.clear_screen()

        # ===== TOP SECTION: Enemy Visual =====
        print("╔" + "═" * (self.width - 2) + "╗")

        # Render enemy ASCII art
        art_lines = Display.render_ascii_art(enemy.ascii_art, self.width)
        for i in range(self.visual_height - 2):
            if i < len(art_lines):
                print("║" + art_lines[i].ljust(self.width - 2) + "║")
            else:
                print("║" + " " * (self.width - 2) + "║")

        # ===== MIDDLE SECTION: Stats Side-by-Side =====
        print(self._draw_horizontal_line())

        # Calculate column widths (50/50 split)
        col_width = (self.width - 3) // 2

        # Build player stats lines
        player_lines = [
            "╔" + "═" * (col_width - 1) + "╗",
            f"║ {player.name} ({player.class_name})".ljust(col_width) + "║",
            f"║ Level: {player.stats.level}".ljust(col_width) + "║",
            f"║ HP: {player.stats.hp}/{player.stats.max_hp}".ljust(col_width) + "║",
            f"║ MP: {player.stats.mp}/{player.stats.max_mp}".ljust(col_width) + "║",
            f"║ ATK: {player.stats.get_effective_attack()} | SPD: {player.stats.get_effective_speed()}".ljust(col_width) + "║",
            f"║ Status: {player.stats.get_status_effects_text()[:col_width-10]}".ljust(col_width) + "║",
            "╚" + "═" * (col_width - 1) + "╝",
        ]

        # Build enemy stats lines
        enemy_lines = [
            "╔" + "═" * (col_width - 1) + "╗",
            f"║ {enemy.name}".ljust(col_width) + "║",
            f"║ Level: {enemy.stats.level}".ljust(col_width) + "║",
            f"║ HP: {enemy.stats.hp}/{enemy.stats.max_hp}".ljust(col_width) + "║",
            f"║ MP: {enemy.stats.mp}/{enemy.stats.max_mp}".ljust(col_width) + "║",
            f"║ ATK: {enemy.stats.get_effective_attack()} | SPD: {enemy.stats.get_effective_speed()}".ljust(col_width) + "║",
            f"║ Status: {enemy.stats.get_status_effects_text()[:col_width-10]}".ljust(col_width) + "║",
            "╚" + "═" * (col_width - 1) + "╝",
        ]

        # Print stats side by side
        for p_line, e_line in zip(player_lines, enemy_lines):
            print("║" + p_line + "│" + e_line + "║")

        # ===== BOTTOM SECTION: Combat Log and Options =====
        print(self._draw_horizontal_line())

        # Combat log header
        print("║ " + "COMBAT LOG".ljust(self.width - 3) + "║")
        print("║" + "─" * (self.width - 2) + "║")

        # Show last few messages
        for msg in messages[-5:]:
            display_msg = msg[:self.width - 4]
            print("║ " + display_msg.ljust(self.width - 3) + "║")

        # Fill remaining space
        used_lines = 2 + len(messages[-5:])
        for _ in range(self.story_height - used_lines - 2):
            print("║" + " " * (self.width - 2) + "║")

        # Options
        print(self._draw_horizontal_line())
        print("║ [1] Attack  [2] Skills  [3] Items  [4] Run".ljust(self.width - 1) + "║")
        print("╚" + "═" * (self.width - 2) + "╝")
    
    def render_exploration_screen(self, player: Player, story_text: str, options: List[str]):
        """Render the exploration view"""
        Display.clear_screen()
        
        # ===== TOP: Scene Art =====
        print("╔" + "═" * (self.width - 2) + "╗")
        
        # Import and use dungeon entrance art
        from ascii_art import DUNGEON_ENTRANCE
        art_lines = Display.render_ascii_art(DUNGEON_ENTRANCE, self.width)
        
        for i in range(self.visual_height - 2):
            if i < len(art_lines):
                print("║" + art_lines[i].ljust(self.width - 2) + "║")
            else:
                print("║" + " " * (self.width - 2) + "║")
        
        # ===== MIDDLE: Player Stats =====
        print(self._draw_horizontal_line())
        
        player_info = (f"[{player.name} - {player.class_name}] "
                      f"LVL:{player.stats.level} | "
                      f"HP:{player.stats.hp}/{player.stats.max_hp} | "
                      f"MP:{player.stats.mp}/{player.stats.max_mp} | "
                      f"Gold:{player.gold} | "
                      f"EXP:{player.stats.exp}")
        print("║ " + player_info.ljust(self.width - 3) + "║")
        
        # ===== BOTTOM: Story and Options =====
        print(self._draw_horizontal_line())
        
        # Word wrap story text
        words = story_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 < self.width - 4:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Print story text
        for line in lines[:self.story_height - 4]:
            print("║ " + line.ljust(self.width - 3) + "║")
        
        # Divider before options
        print("║" + "─" * (self.width - 2) + "║")
        
        # Print options
        for i, option in enumerate(options, 1):
            option_text = f"[{i}] {option}"
            print("║ " + option_text.ljust(self.width - 3) + "║")
        
        # Fill remaining space
        used = len(lines[:self.story_height - 4]) + 1 + len(options)
        for _ in range(self.story_height - used - 1):
            print("║" + " " * (self.width - 2) + "║")
        
        print("╚" + "═" * (self.width - 2) + "╝")
    
    def render_skill_menu(self, player: Player):
        """Display skill selection menu"""
        Display.clear_screen()
        
        print("╔" + "═" * (self.width - 2) + "╗")
        print("║" + "SKILLS".center(self.width - 2) + "║")
        print("╠" + "═" * (self.width - 2) + "╣")
        
        for i, skill in enumerate(player.skills, 1):
            skill_line = (f" [{i}] {skill.name} (MP: {skill.mp_cost}) - "
                         f"{skill.description}")
            print("║" + skill_line.ljust(self.width - 2) + "║")
        
        print("║" + " [0] Back".ljust(self.width - 2) + "║")
        
        # Fill space
        used = 3 + len(player.skills) + 1
        for _ in range(self.height - used - 2):
            print("║" + " " * (self.width - 2) + "║")
        
        print("╚" + "═" * (self.width - 2) + "╝")
    
    def render_inventory_menu(self, player: Player):
        """Display inventory selection menu"""
        Display.clear_screen()
        
        print("╔" + "═" * (self.width - 2) + "╗")
        print("║" + "INVENTORY".center(self.width - 2) + "║")
        print("╠" + "═" * (self.width - 2) + "╣")
        
        if not player.inventory:
            print("║" + "  (Empty)".ljust(self.width - 2) + "║")
        else:
            for i, item in enumerate(player.inventory, 1):
                item_line = f" [{i}] {item.name} - {item.description}"
                print("║" + item_line.ljust(self.width - 2) + "║")
        
        print("║" + " [0] Back".ljust(self.width - 2) + "║")
        
        # Fill space
        used = 3 + (len(player.inventory) if player.inventory else 1) + 1
        for _ in range(self.height - used - 2):
            print("║" + " " * (self.width - 2) + "║")
        
        print("╚" + "═" * (self.width - 2) + "╝")