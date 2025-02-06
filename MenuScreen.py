import pygame
import os
import json
from character_creator import CharacterCreator
from main_game_loop import MainGameLoop

class MenuScreen:
    def __init__(self, screen, options, title="Menu", font_size=36, title_font_size=48, title_color=(255, 255, 255), option_color=(200, 200, 200), selected_color=(255, 0, 0)):
        """
        Initialize the MenuScreen.

        :param screen: The Pygame screen surface to draw on.
        :param options: A list of menu options (strings).
        :param title: The title of the menu (string).
        :param font_size: The font size for the menu options.
        :param title_font_size: The font size for the menu title.
        :param title_color: The color of the title text.
        :param option_color: The color of the menu options.
        :param selected_color: The color of the selected menu option.
        """
        self.screen = screen
        self.options = options
        self.title = title
        self.font_size = font_size
        self.title_font_size = title_font_size
        self.title_color = title_color
        self.option_color = option_color
        self.selected_color = selected_color
        self.selected_index = 0

        # Initialize fonts
        self.title_font = pygame.font.Font(None, self.title_font_size)
        self.option_font = pygame.font.Font(None, self.font_size)

    def draw(self):
        """Draw the menu on the screen."""
        self.screen.fill((0, 0, 0))  # Clear the screen with a black background

        # Draw the title
        title_surface = self.title_font.render(self.title, True, self.title_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(title_surface, title_rect)

        # Draw the menu options
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_index else self.option_color
            option_surface = self.option_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * self.font_size))
            self.screen.blit(option_surface, option_rect)

    def handle_input(self, event):
        """
        Handle user input for navigating the menu.

        :param event: The Pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_index  # Return the selected option index

        return None

    def run(self):
        """Run the menu screen and return the selected option index."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                selected_option = self.handle_input(event)
                if selected_option is not None:
                    return selected_option

            self.draw()
            pygame.display.flip()

def check_for_character_profile():
    """
    Check if the character profile exists.

    :return: True if the profile exists, False otherwise.
    """
    return os.path.exists("character_profile.json")

def launch_pve_mode():
    """
    Launch the PvE mode. If no character profile exists, create one first.
    """
    if not check_for_character_profile():
        print("No character profile found. Launching character creator...")
        creator = CharacterCreator()
        creator.run()  # Run the character creator
        return  # Exit the function to prevent launching the game

    # If the character profile exists, launch the game
    print("Launching PvE mode...")
    game = MainGameLoop("character_profile.json", "data/monsters.json")
    game.run()


def launch_pvp_mode():
    """
    Launch the PvP mode (placeholder for now).
    """
    print("PvP mode is not implemented yet.")

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Menu Screen Example")

    menu = MenuScreen(screen, ["PvE", "PvP"], title="Main Menu")
    selected_option = menu.run()

    if selected_option is not None:
        if selected_option == 0:  # PvE
            launch_pve_mode()
        elif selected_option == 1:  # PvP
            launch_pvp_mode()

    pygame.quit()