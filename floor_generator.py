import json
import random
from pathlib import Path

class FloorGenerator:
    def __init__(self, monster_db_path):
        """
        Initialize the FloorGenerator with the path to the monster database.

        :param monster_db_path: Path to the JSON file containing the monster database.
        """
        self.monster_db = self._load_monster_db(monster_db_path)

    def _load_monster_db(self, path):
        """
        Load the monster database from a JSON file.

        :param path: Path to the JSON file.
        :return: A list of monster dictionaries.
        """
        with open(path, "r") as file:
            return json.load(file)

    def _filter_monsters_by_danger_level(self, danger_level):
        """
        Filter monsters from the database based on their danger level.

        :param danger_level: The danger level to filter by (1 = normal, 2 = elite, 3 = boss).
        :return: A list of monsters matching the danger level.
        """
        return [monster for monster in self.monster_db if monster["danger_level"] == danger_level]

    def generate_floor(self):
        """
        Generate a floor with three rooms:
        - Room A: 2–5 normal monsters (danger_level = 1).
        - Room B: 2–3 elite monsters (danger_level = 2).
        - Room C: 1 boss monster (danger_level = 3).

        :return: A dictionary representing the floor with room details.
        """
        # Select 2–5 normal monsters for Room A
        normal_monsters = self._filter_monsters_by_danger_level(1)
        room_a = random.choices(normal_monsters, k=random.randint(2, 5))

        # Select 2–3 elite monsters for Room B
        elite_monsters = self._filter_monsters_by_danger_level(2)
        room_b = random.choices(elite_monsters, k=random.randint(1, 3))

        # Select 1 boss monster for Room C
        boss_monsters = self._filter_monsters_by_danger_level(3)
        if not boss_monsters:
            raise ValueError("No boss monsters found in the database! Ensure there are monsters with danger_level = 3.")
        room_c = [random.choice(boss_monsters)]

        # Return the floor structure
        return {
            "Room A": room_a,
            "Room B": room_b,
            "Room C": room_c
        }

# Example usage
if __name__ == "__main__":
    # Path to the monster database
    monster_db_path = Path("data/monsters.json")

    # Create a FloorGenerator instance
    generator = FloorGenerator(monster_db_path)

    # Generate a floor
    floor = generator.generate_floor()

    # Print the floor details
    print("Generated Floor:")
    for room, monsters in floor.items():
        print(f"{room}:")
        for monster in monsters:
            print(f"  - {monster['name']} (Danger Level: {monster['danger_level']})")