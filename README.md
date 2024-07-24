# Quoridor 4 Players Game

## Description
Quoridor 4 Players Game is a strategic board game where four players compete to be the first to navigate their pawn to the opposite side of the board. Unlike the classic two-player Quoridor, this version introduces a dynamic and complex layer of strategy with four players, making each move critical. The game stands out with its AI opponents, offering a challenging experience for solo players, and its unique board design that accommodates four players simultaneously.

## Features
- **Four-Player Mode:** Play against three other opponents, either AI or human.
- **AI Opponents:** Challenge yourself against different levels of AI difficulty.
- **Unique Board Design:** A board designed to accommodate the strategies of four players.
- **User-Friendly Controls:** Easy-to-use controls for both moving pawns and placing walls.

## Installation
To set up the game environment on your local machine, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/ilays1998/quoridor_4_players_AI.git
    ```
2. Navigate to the game directory:
    ```bash
    cd quoridor_4_players_AI
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Controls

### Move Pawn
- Use the arrow keys (`↑`, `↓`, `←`, `→`) to move your pawn on the board.
- Press `Enter` to confirm your move.

### Place Walls
1. Use the mouse to select the wall orientation (horizontal or vertical) in the console on the left side of the screen.
2. Click on the desired location on the board to place the wall.

## Game Rules
- The objective is to move your pawn to the opposite side of the board.
- Players can block each other with walls, which can be placed horizontally or vertically.
- Each player has a limited number of walls they can place.

## Game Preview

<img src="/assets/game_preview.png" width="500" alt="Quoridor 4 Player Game">

## How to Play

1. **Start the Game:**
   - Launch the game by running the main script.
   ```bash
   python main.py
    ```

2. **Select Player Mode:**
   - Choose to play against AI or with other human players.

3. **Make Your Move:**
   - Use the arrow keys to move your pawn.
   - Press `Enter` to confirm your move.
   - To place a wall, select the orientation and click on the board.

4. **Strategy:**
   - Plan your moves carefully, considering the positions of other players.
   - Use walls strategically to block your opponents while navigating your pawn towards the goal.

## Built With

* [Pygame](https://www.pygame.org/) - The library used for game development

## Contributing
We welcome contributions! Please follow these steps to contribute to the project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.
