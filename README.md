# -PATH-OF-THE-LONER

Here’s an updated version of the README, incorporating the Player vs. Player (PvP) mode feature.

---

# Python RPG with RPS Mechanics

## Overview

Welcome to the Python RPG with Rock-Paper-Scissors (RPS) mechanics! In this game, you will engage in strategic battles against various monsters and an AI opponent using classic RPS mechanics to determine the outcome of each turn. The game is built using Python and utilizes the Pygame library for rendering graphics and handling user input.

## Features

- **Turn-Based Combat**: Players and monsters take turns choosing their moves.
- **RPS Mechanics**: Choose Rock, Paper, or Scissors to counter your opponent's move.
- **Arrow Key Navigation**: Use the arrow keys to select your move.
- **PvP Mode**: Battle against an AI opponent on equal footing in a competitive setting.
- **Interactive Gameplay**: Engage in battles with different monsters, each with unique moves.

## Gameplay Mechanics

### Turn Structure

1. **Monster Chooses Move**: At the beginning of each turn, the monster or AI opponent randomly selects its move.
2. **Player Chooses Move**: The player uses the arrow keys to choose their move (Rock, Paper, or Scissors).
3. **Resolve**: The game determines the winner based on the RPS rules:
   - Rock crushes Scissors
   - Scissors cuts Paper
   - Paper covers Rock
4. **Damage Application**: The result of the round is applied, affecting the health of either the player or the monster/AI.
5. **New Turn**: The next turn begins with the monster or AI choosing its move again.

## Controls

- **Arrow Keys**: Navigate through the available move options (Rock, Paper, Scissors).
- **ENTER**: Confirm your move selection.

## Requirements

To run this game, you will need:
- Python 3.x
- Pygame library

### Installation

1. Install Python from the [official website](https://www.python.org/downloads/).
2. Install Pygame using pip:
   ```bash
   pip install pygame
   ```

## Running the Game

To start the game, navigate to the project directory and run the following command:

```bash
python main.py
```

## Directory Structure

```
/python-rpg-rps/
│
├── main.py            # Main game file
├── assets/            # Folder for game assets (images, sounds, etc.)
├── README.md          # This README file
└── requirements.txt   # Python package requirements
```

## Future Enhancements

- Add different monster types with unique abilities.
- Include more complex moves or power-ups.
- Enhance the AI for more challenging PvP battles.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

This version includes the PvP mode, highlighting the capability for players to face an AI on equal footing. Feel free to make any additional adjustments or modifications!
