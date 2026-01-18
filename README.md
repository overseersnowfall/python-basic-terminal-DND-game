# Dungeon Quest: ASCII Adventure

A text-based RPG game with turn-based combat, multiple character classes, and ASCII art visuals.

## 🎮 How to Run

```bash
python main.py
```

## 📁 Project Structure

```
dungeon_quest/
├── main.py          # Entry point - RUN THIS FILE
├── game.py          # Main game loop and state management
├── combat.py        # Turn-based combat system
├── display.py       # Terminal rendering and screen layouts
├── stats.py         # Data classes (Stats, Skill, Item, StatusEffect)
├── entities.py      # Base Entity class
├── player.py        # All player classes (Warrior, Wizard, Ranger, Thief)
├── enemy.py         # Enemy class and enemy database
└── ascii_art.py     # All ASCII art assets
```

## 🎯 File Purposes

### **main.py**
- Entry point of the game
- Simply creates Game instance and runs it

### **game.py**
- Main game controller
- Manages game states (menu, exploring, combat, game over)
- Handles character creation
- Controls exploration loop

### **combat.py**
- Turn-based combat system
- Handles player and enemy turns
- Manages skills, items, fleeing
- Processes status effects each turn

### **display.py**
- `Display` class: Helper functions for terminal operations
- `GameScreen` class: Renders split-screen layouts
  - Combat screen (enemy art + stats + combat log)
  - Exploration screen (scene art + story + options)
  - Skill menu
  - Inventory menu

### **stats.py**
- `Stats`: Character statistics (HP, MP, Attack, Speed, etc.)
- `StatusEffect`: Buffs, debuffs, poison, stun, etc.
- `Skill`: Character abilities that cost MP
- `Item`: Consumable items (potions, etc.)

### **entities.py**
- `Entity`: Base class for all characters
- Contains `basic_attack()` method
- Parent class for Player and Enemy

### **player.py**
- `Player`: Abstract base class for all player types
- `Warrior`: High HP, physical damage
- `Wizard`: High MP, magic and healing
- `Ranger`: Balanced, ranged attacks
- `Thief`: High speed, status effects

### **enemy.py**
- `Enemy`: Enemy class with rewards (EXP, gold)
- `create_enemy_database()`: Returns list of all enemies

### **ascii_art.py**
- All ASCII art stored here
- Enemy art: GOBLIN, ORC, DRAGON, SKELETON, SLIME
- Scene art: DUNGEON_ENTRANCE, TREASURE_ROOM, CAMPFIRE, BOSS_ROOM

## 🔧 How to Add Content

### **Add a New Enemy**

Edit `enemy.py`:

```python
# In create_enemy_database() function
Enemy(
    name="Your Enemy Name",
    stats=Stats(hp=100, max_hp=100, mp=20, max_mp=20,
                attack=15, speed=10, level=3),
    ascii_art=ascii_art.YOUR_ART,  # Add art to ascii_art.py first
    exp_reward=50,
    gold_reward=25
)
```

### **Add ASCII Art**

Edit `ascii_art.py`:

```python
YOUR_NEW_ART = r"""
    Your
    ASCII
    Art
    Here
"""
```

### **Add a Skill to a Class**

Edit `player.py`, find your class's `_init_skills()` method:

```python
Skill(
    name="Skill Name",
    description="What it does",
    mp_cost=20,
    skill_type="damage",  # or "heal", "buff", "debuff", "dot", "stun"
    power=1.8,  # Multiplier of attack stat
    duration=3  # For buffs/debuffs/DoTs
)
```

### **Add a New Player Class**

Edit `player.py`:

```python
class YourClass(Player):
    def __init__(self, name: str):
        stats = Stats(
            hp=110, max_hp=110,
            mp=45, max_mp=45,
            attack=16,
            speed=11
        )
        super().__init__(name, stats, "YourClassName")
    
    def _init_skills(self):
        self.skills = [
            # Your skills here
        ]
```

Then update `game.py` in `_create_player()` to add the menu option.

## 🎲 Game Features

- **4 Character Classes** with unique skills
- **Turn-based Combat** with strategic choices
- **Status Effects** (buffs, debuffs, poison, stun)
- **Leveling System** with stat increases
- **Item System** (health and mana potions)
- **Random Encounters** while exploring
- **Multiple Enemies** with different difficulty levels

## 📊 Character Classes

| Class   | HP  | MP  | ATK | SPD | Playstyle           |
|---------|-----|-----|-----|-----|---------------------|
| Warrior | 120 | 30  | 18  | 8   | Tank, heavy damage  |
| Wizard  | 80  | 60  | 12  | 10  | Magic, healing      |
| Ranger  | 100 | 40  | 15  | 12  | Balanced, fast      |
| Thief   | 90  | 35  | 14  | 15  | Speed, status       |

## 🐛 Troubleshooting

**ASCII art not showing?**
- Make sure you're using raw strings (`r"""..."""`) in `ascii_art.py`
- Check your terminal supports UTF-8 encoding

**Import errors?**
- Make sure all files are in the same directory
- Run from the directory containing all the files

**Screen layout issues?**
- Try resizing your terminal to at least 100 columns × 30 rows
- The game adapts to terminal size automatically

## 📝 Future Ideas

- Save/Load system
- Equipment system (weapons, armor)
- More dungeons/areas
- Boss battles
- Party system (multiple characters)
- Crafting system
- Quest system

## 🎉 Have Fun!

Enjoy exploring the dungeon and building upon this framework!
