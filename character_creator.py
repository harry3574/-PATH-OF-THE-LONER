import pygame
import json
from pathlib import Path

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (200, 200, 0)

class CharacterCreator:
    def __init__(self):
        """
        Initialize the Character Creator.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Character Creator")
        self.clock = pygame.time.Clock()

        # Load databases
        self.ascendances = self._load_json("data/ascendances.json")
        self.weapons = self._load_json("data/weapons.json")
        self.armors = self._load_json("data/armors.json")
        self.spells = self._load_json("data/spells.json")

        # Character creation state
        self.selected_ascendancy = None
        self.selected_weapon = None
        self.selected_armor = None
        self.selected_spell = None
        self.current_step = "ascendancy"  # Steps: ascendancy -> weapon -> armor -> spell -> save

    def _load_json(self, path):
        """
        Load a JSON file from the given path.

        :param path: Path to the JSON file.
        :return: Data from the JSON file.
        """
        with open(path, "r") as file:
            return json.load(file)

    def draw_text(self, text, x, y, color=WHITE):
        """
        Draw text on the screen.

        :param text: The text to display.
        :param x: X position of the text.
        :param y: Y position of the text.
        :param color: Color of the text.
        """
        text_surface = FONT.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_menu(self, title, items, selected_index):
        """
        Draw a menu with a title and a list of selectable items.

        :param title: The title of the menu.
        :param items: A list of items to display.
        :param selected_index: The index of the currently selected item.
        """
        self.draw_text(title, 50, 50)
        for i, item in enumerate(items):
            color = HIGHLIGHT if i == selected_index else WHITE
            self.draw_text(f"{i + 1}. {item['name']}", 50, 100 + i * 40, color)

    def run(self):
        """
        Run the character creator.
        """
        running = True
        selected_index = 0

        while running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(self.get_current_items())
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(self.get_current_items())
                    elif event.key == pygame.K_RETURN:
                        self.handle_selection(selected_index)
                        selected_index = 0  # Reset selection for the next step
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # Draw the current step
            if self.current_step == "ascendancy":
                self.draw_menu("Choose Your Ascendancy", self.ascendances, selected_index)
            elif self.current_step == "weapon":
                self.draw_menu("Choose Your Weapon", self.weapons, selected_index)
            elif self.current_step == "armor":
                self.draw_menu("Choose Your Armor", self.armors, selected_index)
            elif self.current_step == "spell":
                self.draw_menu("Choose Your Spell (Optional)", self.spells, selected_index)
            elif self.current_step == "save":
                self.draw_text("Character Created! Saving profile...", 50, 50)
                self.save_character()
                running = False

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def get_current_items(self):
        """
        Get the list of items for the current step.

        :return: A list of items.
        """
        if self.current_step == "ascendancy":
            return self.ascendances
        elif self.current_step == "weapon":
            return self.weapons
        elif self.current_step == "armor":
            return self.armors
        elif self.current_step == "spell":
            return self.spells
        return []

    def handle_selection(self, selected_index):
        """
        Handle the selection of an item.

        :param selected_index: The index of the selected item.
        """
        items = self.get_current_items()
        if not items:
            return

        selected_item = items[selected_index]

        if self.current_step == "ascendancy":
            self.selected_ascendancy = selected_item
            self.current_step = "weapon"
        elif self.current_step == "weapon":
            self.selected_weapon = selected_item
            self.current_step = "armor"
        elif self.current_step == "armor":
            self.selected_armor = selected_item
            self.current_step = "spell"
        elif self.current_step == "spell":
            self.selected_spell = selected_item
            self.current_step = "save"

    def save_character(self):
        """
        Save the character profile to a JSON file.
        """
        character = {
            "ascendancy": self.selected_ascendancy,
            "weapon": self.selected_weapon,
            "armor": self.selected_armor,
            "spell": self.selected_spell
        }

        with open("character_profile.json", "w") as file:
            json.dump(character, file, indent=4)

# Run the character creator
if __name__ == "__main__":
    creator = CharacterCreator()
    creator.run()