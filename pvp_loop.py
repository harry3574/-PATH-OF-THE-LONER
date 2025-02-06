import pygame
import json
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (200, 200, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# UI Constants
UI_PADDING = 20

class MainGameLoop:
    def __init__(self, player_profile_path):
        """
        Initialize the Main Game Loop.

        :param player_profile_path: Path to the player profile JSON file.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PvP Battle RPG")
        self.clock = pygame.time.Clock()

        # Load player profile
        self.character = self._load_json(player_profile_path)
        self.player_stats = self._get_player_stats()
        self.enemy = self._create_enemy()  # Create a single enemy for PvP
        self.combat_log = []
        self.turn_state = "enemy_turn"  # Start with enemy's turn
        self.enemy_move = None  # Variable to store enemy's chosen move

    def _load_json(self, path):
        """
        Load a JSON file from the given path.

        :param path: Path to the JSON file.
        :return: Data from the JSON file.
        """
        with open(path, "r") as file:
            return json.load(file)

    def _get_player_stats(self):
        """
        Calculate the player's stats based on their equipment.

        :return: A dictionary of player stats.
        """
        stats = {
            "health": 100,
            "attack": 10,
            "defense": 5,
            "armor_rating": self.character["armor"]["armor_value"],
            "moves": [],
            "weapon": self.character["weapon"]["name"],
            "armor": self.character["armor"]["name"],
            "spell": self.character["spell"]["name"] if "spell" in self.character else "None"
        }

        # Add weapon damage to attack
        if "weapon" in self.character:
            stats["attack"] += self.character["weapon"]["damage"]

        # Add armor value to defense
        if "armor" in self.character:
            stats["defense"] += self.character["armor"]["armor_value"]

        # Add spells to moves
        if "spell" in self.character:
            stats["moves"].append(self.character["spell"])

        # Add weapon as a move
        if "weapon" in self.character:
            stats["moves"].append({
                "name": self.character["weapon"]["name"],
                "type": self.character["weapon"]["type"],
                "damage": self.character["weapon"]["damage"],
                "description": f"A basic attack with the {self.character['weapon']['name']}."
            })

        return stats

    def _create_enemy(self):
        """
        Create a basic enemy for the PvP battle.

        :return: A dictionary representing the enemy.
        """
        return {
            "name": "Rival Warrior",
            "health": 100,
            "attack": 15,
            "armor_rating": 10,
            "moves": [
                {
                    "name": "Sword Slash",
                    "type": "Rock",
                    "damage": 20,
                },
                {
                    "name": "Shield Bash",
                    "type": "Paper",
                    "damage": 15,
                },
                {
                    "name": "Spear Thrust",
                    "type": "Scissors",
                    "damage": 25,
                }
            ]
        }

    def draw_text(self, text, x, y, color=WHITE, font=FONT):
        """
        Draw text on the screen.

        :param text: The text to display.
        :param x: X position of the text.
        :param y: Y position of the text.
        :param color: Color of the text.
        :param font: Font to use for the text.
        """
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_combat_log(self):
        """
        Draw the combat log on the screen.
        """
        self.draw_text("Combat Log:", UI_PADDING, 400, WHITE, SMALL_FONT)
        y = 430
        for log_entry in self.combat_log[-5:]:  # Show the last 5 log entries
            self.draw_text(log_entry, UI_PADDING, y, WHITE, SMALL_FONT)
            y += 20

    def draw_player_stats(self):
        """
        Draw the player's stats on the screen.
        """
        self.draw_text("Player Stats:", SCREEN_WIDTH // 1.35 + UI_PADDING, 20, WHITE)
        self.draw_text(f"Health: {self.player_stats['health']}", SCREEN_WIDTH // 1.35 + UI_PADDING, 60, GREEN, SMALL_FONT)
        self.draw_text(f"Attack: {self.player_stats['attack']}", SCREEN_WIDTH // 1.35 + UI_PADDING, 90, RED, SMALL_FONT)
        self.draw_text(f"Defense: {self.player_stats['defense']}", SCREEN_WIDTH // 1.35 + UI_PADDING, 120, BLUE, SMALL_FONT)
        self.draw_text(f"Weapon: {self.player_stats['weapon']}", SCREEN_WIDTH // 1.35 + UI_PADDING, 150, WHITE, SMALL_FONT)
        self.draw_text(f"Armor: {self.player_stats['armor']}", SCREEN_WIDTH // 1.35 + UI_PADDING, 180, WHITE, SMALL_FONT)
        self.draw_text(f"Spell: {self.player_stats['spell']}", SCREEN_WIDTH // 1.35 + UI_PADDING, 210, WHITE, SMALL_FONT)

    def draw_enemy_stats(self):
        """
        Draw the enemy's stats on the screen.
        """
        self.draw_text("Enemy Stats:", UI_PADDING, 20, WHITE)
        self.draw_text(f"Name: {self.enemy['name']}", UI_PADDING, 60, WHITE, SMALL_FONT)
        self.draw_text(f"Health: {self.enemy['health']}", UI_PADDING, 90, GREEN, SMALL_FONT)

    def draw_menu(self, title, items, selected_index):
        """
        Draw a menu with a title and a list of selectable items.

        :param title: The title of the menu.
        :param items: A list of items to display.
        :param selected_index: The index of the currently selected item.
        """
        self.draw_text(title, UI_PADDING, 250, WHITE)
        for i, item in enumerate(items):
            color = HIGHLIGHT if i == selected_index else WHITE
            self.draw_text(f"{i + 1}. {item['name']} ({item['type']}) - {item['damage']} DMG", UI_PADDING, 280 + i * 30, color, SMALL_FONT)

    def draw_prompt(self):
        """
        Draw a prompt to guide the player on what to do.
        """
        if self.turn_state == "player_turn":
            self.draw_text("Choose your move (UP/DOWN to select, ENTER to confirm):", UI_PADDING, 350, YELLOW, SMALL_FONT)
        elif self.turn_state == "enemy_defeated":
            self.draw_text("You defeated the enemy! Press ENTER to continue...", UI_PADDING, 350, YELLOW, SMALL_FONT)

    def run(self):
        """
        Run the main game loop.
        """
        running = True
        selected_index = 0

        while running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.turn_state == "enemy_turn":
                        self.enemy_turn()  # Let the enemy choose its move
                    elif self.turn_state == "player_turn":
                        if event.key == pygame.K_UP:
                            selected_index = (selected_index - 1) % len(self.player_stats["moves"])
                        elif event.key == pygame.K_DOWN:
                            selected_index = (selected_index + 1) % len(self.player_stats["moves"])
                        elif event.key == pygame.K_RETURN:
                            self.player_move = self.player_stats["moves"][selected_index]
                            self.combat_log.append(f"You use {self.player_move['name']}!")
                            self.resolve_combat()
                            selected_index = 0  # Reset selection for the next turn

                    elif self.turn_state == "enemy_defeated" and event.key == pygame.K_RETURN:
                        running = False  # Exit the game after victory

            # Draw UI
            self.draw_player_stats()
            self.draw_enemy_stats()
            if self.turn_state == "player_turn":
                self.draw_menu("Choose Your Move", self.player_stats["moves"], selected_index)
            self.draw_combat_log()
            self.draw_prompt()

            pygame.display.flip()
            self.clock.tick(30)

    def enemy_turn(self):
        """
        Execute the enemy's turn logic.
        """
        self.enemy_move = random.choice(self.enemy["moves"])  # Enemy randomly selects a move
        self.combat_log.append(f"{self.enemy['name']} selects {self.enemy_move['name']}!")
        self.turn_state = "player_turn"  # Switch to player turn after enemy selects a move

    def resolve_combat(self):
        """
        Resolve combat between the player and the enemy.
        """
        # Determine the outcome based on Rock-Paper-Scissors logic
        player_type = self.player_move["type"]
        enemy_type = self.enemy_move["type"]

        # Determine the winner of this round based on RPS logic
        if (player_type == "Rock" and enemy_type == "Scissors") or \
           (player_type == "Scissors" and enemy_type == "Paper") or \
           (player_type == "Paper" and enemy_type == "Rock"):
            # Player wins this round
            enemy_damage = max(0, self.player_move["damage"] - self.enemy["armor_rating"])
            self.enemy["health"] -= enemy_damage
            self.combat_log.append(f"You attack {self.enemy['name']} with {self.player_move['name']} and deal {enemy_damage} damage!")
        elif (enemy_type == "Rock" and player_type == "Scissors") or \
             (enemy_type == "Scissors" and player_type == "Paper") or \
             (enemy_type == "Paper" and player_type == "Rock"):
            # Enemy wins this round
            player_damage = max(0, self.enemy_move["damage"] - self.player_stats["armor_rating"])
            self.player_stats["health"] -= player_damage
            self.combat_log.append(f"{self.enemy['name']} attacks you with {self.enemy_move['name']} and deals {player_damage} damage!")
        else:
            # It's a draw
            self.combat_log.append("It's a draw! No damage dealt.")

        # Check if the player is defeated
        if self.player_stats["health"] <= 0:
            self.combat_log.append("You have been defeated!")
            self.turn_state = "player_turn"  # End the game after a loss
        elif self.enemy["health"] <= 0:
            self.combat_log.append(f"You have defeated {self.enemy['name']}!")
            self.turn_state = "enemy_defeated"  # Set state for victory
        else:
            self.turn_state = "enemy_turn"  # Switch back to enemy turn after resolving combat

if __name__ == "__main__":
    game = MainGameLoop("pvp_profile.json")
    game.run()
    pygame.quit()
