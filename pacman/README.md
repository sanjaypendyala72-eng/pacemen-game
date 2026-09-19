# Pacman Game in Python

A classic Pacman game implemented in Python using pygame.

## Features

- Classic Pacman gameplay with maze navigation
- 4 colored ghosts (Red, Pink, Cyan, Orange) with AI behavior
- Dots and power pellets
- Power mode: Eat power pellets to turn ghosts blue and eat them
- Score tracking and lives system
- Game over and win conditions
- Restart functionality

## Controls

- **Arrow Keys**: Move Pacman (Up, Down, Left, Right)
- **R**: Restart game (when game over or won)

## Installation

1. Make sure you have Python installed
2. Install pygame:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python pacman.py
```

## Game Rules

- Navigate Pacman through the maze to eat all dots
- Avoid ghosts - they will cost you a life
- Eat power pellets (large dots) to turn ghosts blue
- When ghosts are blue, you can eat them for bonus points
- Collect all dots to win
- You have 3 lives

## Scoring

- Regular dot: 10 points
- Power pellet: 50 points
- Eating a scared ghost: 200 points
