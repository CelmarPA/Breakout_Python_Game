# 🧱 Breakout Game (Turtle Edition)

A visually enhanced **Breakout-style game** built with **Python** and the **Turtle graphics** library. The game features animated paddle and ball mechanics, multiple levels with increasing difficulty, sound effects, power-ups, lives represented as hearts, and a scoreboard. Designed for two players.

---

## 📌 Table of Contents

- [🧱 Breakout Game (Turtle Edition)](#-breakout-game-turtle-edition)
  - [📌 Table of Contents](#-table-of-contents)
  - [🚀 Features](#-features)
  - [⚙️ How It Works](#️-how-it-works)
  - [🧰 Technologies](#-technologies)
  - [🛠️ Getting Started](#️-getting-started)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Run the game](#2-run-the-game)
  - [🎮 Gameplay](#-gameplay)
  - [🧪 Power-Ups \& Effects](#-power-ups--effects)
  - [📚 What I Learned](#-what-i-learned)
  - [📄 License](#-license)
  - [👤 Author](#-author)
  - [💬 Feedback](#-feedback)

---

## 🚀 Features

- Two-player support with turn-based lives and scoring
- Multiple levels with increasing difficulty
- Dynamic paddle resizing as a power-down
- Life recovery as a power-up
- Visual scoreboard with names, scores, and hearts
- Pause and resume using the `Return` key
- Sound effects for bounce, block hits, level up, game over, etc.
- Fully responsive to window resizing
- Built with **pure Python + Turtle**

---

## ⚙️ How It Works

- The game uses Turtle and Tkinter for rendering and events
- `main.py` initializes all game components
- Levels add more block rows and increase ball speed
- Score and lives are managed by a custom `ScoreBoard` with image rendering
- Game logic includes collision detection, block removal, and effects
- Sounds are managed with `pygame.mixer`

---

## 🧰 Technologies

- **Python 3**
- `turtle` (graphics and input)
- `pygame` (sound effects)
- `Pillow` (custom text-to-image rendering)
- `tkinter` (underlying canvas and root window)

---

## 🛠️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/CelmarPA/Breakout_Python_Game
cd breakout-game
```

### 2. Run the game

```bash
python3 main.py
```

> Make sure the `sounds/` and `gifs/` folders exist with the proper files.

---

## 🎮 Gameplay

- Use **Arrow keys** or **A/D** to move the paddle
- Press **SPACE** to start a turn
- Press **Return** to pause or resume the game
- Lose a life if the ball falls below the paddle
- Clear all blocks to progress to the next level
- After one player loses all lives, the second player plays
- The player with the highest score wins!

---

## 🧪 Power-Ups & Effects

- **Power-Up Block**: Adds one life to the current player
- **Power-Down Block**: Shrinks paddle for 5 seconds
- **Standard Blocks**: Add 1 point when destroyed

---

## 📚 What I Learned

This project helped me practice:

- Object-oriented programming with custom classes
- Game loop architecture and collision mechanics
- Sound integration using `pygame`
- Real-time graphics with `turtle`
- Image generation for score display with `Pillow`
- UI responsiveness and event handling

---

## 📄 License

This project is licensed under the **MIT License** – feel free to use and modify it as you like.

---

## 👤 Author

**Celmar Pereira**

- [GitHub](https://github.com/CelmarPA)
- [LinkedIn](https://linkedin.com/in/celmar-pereira-de-andrade-039830181)
- [Portfolio](https://yourportfolio.com)

---

## 💬 Feedback

If you find a bug or have suggestions for improvement, feel free to **open an issue** or **submit a pull request**. Contributions are welcome!
