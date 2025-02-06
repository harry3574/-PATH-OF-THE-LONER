import pygame
import json
import random
from pathlib import Path
from floor_generator import FloorGenerator

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
UI_SECTION_WIDTH = (SCREEN_WIDTH - 3 * UI_PADDING) // 2
UI_SECTION_HEIGHT = SCREEN_HEIGHT - 2 * UI_PADDING

class MainGameLoop:
    def __init__(self, character_profile_path, monster_db_path):
        """
        Initialize the Main Game Loop.

        :param character_profile_path: Path to the character profile JSON file.
        :param monster_db_path: Path to the monster database JSON file.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Turn-Based RPG")
        self.clock = pygame.time.Clock()

        # Load character profile
        self.character = self._load_json(character_profile_path)
        self.player_stats = self._get_player_stats()

        # Load monster database and generate a floor
        self.floor_generator = FloorGenerator(monster_db_path)
        self.current_floor = self.floor_generator.generate_floor()
        self.current_floor_number = 1
        self.current_room = "Room A"
        self.current_enemies = self.current_floor[self.current_room]
        self.current_enemy_index = 0
        self.current_enemy = self.current_enemies[self.current_enemy_index]
        self.enemy_move = None
        self.player_move = None
        self.combat_log = []
        self.turn_state = "enemy_turn"  # States: enemy_turn, player_turn, resolve_turn, game_over
        self.show_rewards_popup = False
        self.show_game_over_popup = False
        self.rewards = []

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
        Calculate the player's stats based on their equipment and ascendancy.

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
        self.draw_text(f"Name: {self.current_enemy['name']}", UI_PADDING, 60, WHITE, SMALL_FONT)
        self.draw_text(f"Health: {self.current_enemy['health']}", UI_PADDING, 90, GREEN, SMALL_FONT)
        self.draw_text(f"Type: {self.current_enemy['type']}", UI_PADDING, 120, WHITE, SMALL_FONT)
        self.draw_text(f"Weakness: {self.current_enemy['weakness']}", UI_PADDING, 150, WHITE, SMALL_FONT)

    def draw_floor_info(self):
        """
        Draw the current floor and room information.
        """
        self.draw_text(f"Floor: {self.current_floor_number}", SCREEN_WIDTH // 2 - 100, 20, WHITE)
        self.draw_text(f"Room: {self.current_room}", SCREEN_WIDTH // 2 - 100, 60, WHITE)
        self.draw_text(f"Enemies Left: {len(self.current_enemies) - self.current_enemy_index}", SCREEN_WIDTH // 2 - 100, 100, WHITE)

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
        if self.turn_state == "enemy_turn":
            self.draw_text("Enemy is choosing a move...", UI_PADDING, 350, YELLOW, SMALL_FONT)
        elif self.turn_state == "player_turn":
            self.draw_text("Choose your move (UP/DOWN to select, ENTER to confirm):", UI_PADDING, 350, YELLOW, SMALL_FONT)
        elif self.turn_state == "resolve_turn":
            self.draw_text("Press ENTER to resolve the turn...", UI_PADDING, 350, YELLOW, SMALL_FONT)

    def draw_rewards_popup(self):
        """
        Draw a pop-up window displaying the rewards for defeating the enemy.
        """
        # Darken the background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Draw the pop-up window
        popup_width = 400
        popup_height = 300
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        pygame.draw.rect(self.screen, BLACK, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, WHITE, (popup_x, popup_y, popup_width, popup_height), 2)

        # Draw the title
        self.draw_text("Victory!", popup_x + 20, popup_y + 20, WHITE)
        self.draw_text(f"You have killed {self.current_enemy['name']}!", popup_x + 20, popup_y + 60, WHITE, SMALL_FONT)

        # Draw the rewards
        y = popup_y + 100
        for reward in self.rewards:
            self.draw_text(f"- {reward['item']} x{reward['quantity']}", popup_x + 20, y, WHITE, SMALL_FONT)
            y += 30

        # Draw the prompt
        self.draw_text("Press ENTER to continue...", popup_x + 20, popup_y + 240, YELLOW, SMALL_FONT)

    def draw_game_over_popup(self):
        """
        Draw a pop-up window for the game over screen.
        """
        # Darken the background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Draw the pop-up window
        popup_width = 400
        popup_height = 300
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        pygame.draw.rect(self.screen, BLACK, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, WHITE, (popup_x, popup_y, popup_width, popup_height), 2)

        # Draw the title
        self.draw_text("Game Over!", popup_x + 20, popup_y + 20, RED)
        self.draw_text("You have been defeated!", popup_x + 20, popup_y + 60, WHITE, SMALL_FONT)

        # Draw the options
        self.draw_text("Press UP ARROW to restart", popup_x + 20, popup_y + 120, WHITE, SMALL_FONT)
        self.draw_text("Press DOWN ARROW to quit", popup_x + 20, popup_y + 160, WHITE, SMALL_FONT)

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
                    if self.show_rewards_popup:
                        if event.key == pygame.K_RETURN:
                            self.show_rewards_popup = False
                            self.next_enemy()
                    elif self.turn_state == "player_turn":
                        if event.key == pygame.K_UP:
                            selected_index = (selected_index - 1) % len(self.player_stats["moves"])
                        elif event.key == pygame.K_DOWN:
                            selected_index = (selected_index + 1) % len(self.player_stats["moves"])
                        elif event.key == pygame.K_RETURN:
                            self.player_move = self.player_stats["moves"][selected_index]
                            self.combat_log.append(f"You use {self.player_move['name']} ({self.player_move['type']})!")
                            self.turn_state = "resolve_turn"
                    elif self.turn_state == "resolve_turn" and event.key == pygame.K_RETURN:
                        self.resolve_combat()
                        selected_index = 0  # Reset selection for the next turn
                    elif self.turn_state == "game_over":
                        if event.key == pygame.K_UP:  # Restart the game
                            self.reset_game()
                        elif event.key == pygame.K_DOWN:  # Quit the game
                            running = False

            # Enemy turn logic
            if self.turn_state == "enemy_turn":
                self.enemy_move = random.choice(self.current_enemy["attacks"])
                self.combat_log.append(f"Enemy uses {self.enemy_move['name']} ({self.enemy_move['type']})!")
                self.turn_state = "player_turn"

            # Draw UI
            self.draw_enemy_stats()
            self.draw_player_stats()
            if self.turn_state == "player_turn":
                self.draw_menu("Choose Your Move", self.player_stats["moves"], selected_index)
            self.draw_combat_log()
            self.draw_prompt()
            self.draw_floor_info()

            # Draw rewards pop-up if applicable
            if self.show_rewards_popup:
                self.draw_rewards_popup()

            # Draw game over pop-up if applicable
            if self.turn_state == "game_over":
                self.draw_game_over_popup()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def resolve_combat(self):
        """
        Resolve the combat between the player and the enemy.
        """
        # Determine RPS outcome
        player_type = self.player_move["type"]
        enemy_type = self.enemy_move["type"]

        if player_type == enemy_type:
            outcome = "neutral"
        elif (player_type == "Rock" and enemy_type == "Scissors") or \
             (player_type == "Paper" and enemy_type == "Rock") or \
             (player_type == "Scissors" and enemy_type == "Paper"):
            outcome = "superior"
        else:
            outcome = "weak"

        # Apply RPS mechanics
        if outcome == "superior":
            # Player counters enemy move, enemy flinches
            damage_multiplier = 1.75
            self.combat_log.append(f"Your {player_type} counters {enemy_type}! Enemy flinches!")
            enemy_damage = 0  # Enemy skips their attack
        elif outcome == "neutral":
            # Neutral outcome
            damage_multiplier = 1.0
            if random.random() < 0.05:  # 5% chance to flinch
                self.combat_log.append(f"Enemy flinches!")
                enemy_damage = 0
            else:
                enemy_damage = self.enemy_move["damage"]
        elif outcome == "weak":
            # Weak outcome
            damage_multiplier = 0.75
            enemy_damage = self.enemy_move["damage"] * 1.25
            self.combat_log.append(f"Your {player_type} is weak against {enemy_type}!")

        # Player attacks enemy
        player_damage = self.player_move["damage"] * damage_multiplier
        self.current_enemy["health"] -= player_damage
        self.combat_log.append(f"You deal {player_damage} {player_type} damage to {self.current_enemy['name']}!")

        # Enemy attacks player
        if enemy_damage > 0:
            player_damage_taken = (enemy_damage) * (1 - self.player_stats["armor_rating"] / 100)
            self.player_stats["health"] -= player_damage_taken
            self.combat_log.append(f"{self.current_enemy['name']} deals {player_damage_taken} {enemy_type} damage to you!")

        # Check if the enemy is defeated
        if self.current_enemy["health"] <= 0:
            self.combat_log.append(f"{self.current_enemy['name']} is defeated!")
            self.generate_rewards()
            self.show_rewards_popup = True

        # Check if the player is defeated
        if self.player_stats["health"] <= 0:
            self.combat_log.append("You have been defeated!")
            self.turn_state = "game_over"

        # Reset moves for the next turn
        self.enemy_move = None
        self.player_move = None
        if self.turn_state != "game_over":
            self.turn_state = "enemy_turn"

    def generate_rewards(self):
        """
        Generate rewards for defeating the enemy.
        """
        self.rewards = []
        for loot in self.current_enemy["loot_table"]:
            if random.random() < loot["chance"]:
                quantity = loot["quantity"] if isinstance(loot["quantity"], int) else random.randint(loot["quantity"][0], loot["quantity"][1])
                self.rewards.append({"item": loot["item"], "quantity": quantity})

    def next_enemy(self):
        """
        Move to the next enemy in the room.
        """
        self.current_enemy_index += 1
        if self.current_enemy_index < len(self.current_enemies):
            self.current_enemy = self.current_enemies[self.current_enemy_index]
            self.reset_combat_state()
        else:
            self.next_room()

    def next_room(self):
        """
        Move to the next room on the floor.
        """
        if self.current_room == "Room A":
            self.current_room = "Room B"
        elif self.current_room == "Room B":
            self.current_room = "Room C"
        elif self.current_room == "Room C":
            self.combat_log.append("You have cleared the floor!")
            self.current_floor_number += 1
            self.current_floor = self.floor_generator.generate_floor()
            self.current_room = "Room A"

        self.current_enemies = self.current_floor[self.current_room]
        self.current_enemy_index = 0
        self.current_enemy = self.current_enemies[self.current_enemy_index]
        self.reset_combat_state()

    def reset_combat_state(self):
        """
        Reset the combat state when entering a new room or floor.
        """
        self.enemy_move = None
        self.player_move = None
        self.turn_state = "enemy_turn"
        self.combat_log.clear()

    def reset_game(self):
        """
        Reset the game to its initial state.
        """
        # Reset player stats
        self.player_stats = self._get_player_stats()

        # Reset floor and room
        self.current_floor = self.floor_generator.generate_floor()
        self.current_floor_number = 1
        self.current_room = "Room A"
        self.current_enemies = self.current_floor[self.current_room]
        self.current_enemy_index = 0
        self.current_enemy = self.current_enemies[self.current_enemy_index]

        # Reset combat state
        self.reset_combat_state()

        # Reset game over state
        self.turn_state = "enemy_turn"
        self.show_game_over_popup = False

# Run the game
if __name__ == "__main__":
    game = MainGameLoop("character_profile.json", "data/monsters.json")
    game.run()