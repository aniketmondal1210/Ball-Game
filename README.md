# Ball-Game

![Game Screenshot](screenshots/gameplay.png)

## Features

- **Classic Pong Gameplay**: Control a paddle to bounce a ball back and forth against an AI opponent
- **Multiple Difficulty Levels**: Choose between Easy, Medium, and Hard AI opponents
- **Visual Effects**: Ball trail, color changes on collision, and smooth animations
- **Game Controls**: Pause functionality, restart, and difficulty selection
- **Score Tracking**: Keep track of your score against the AI
- **Improved Physics**: Enhanced collision detection and realistic ball bouncing
- **Sound Effects**: Audio feedback for collisions and scoring

## Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Setup
- Clone this repository: git clone https://github.com/aniketmondal1210/enhanced-pong.git

## How to Play
- cd enhanced-pong

- Install the required dependencies:
pip install pygame

- Run the game:
python pong_game.py

### Controls
- **Up/Down Arrow Keys**: Move your paddle (left side) up and down
- **Space**: Start the game when in rest state
- **P**: Pause/unpause the game
- **1, 2, 3**: Change difficulty level (Easy, Medium, Hard)
- **Close Window**: Exit the game

### Game Rules
- The ball will bounce off paddles and the top/bottom boundaries
- Score a point when the ball passes your opponent's paddle
- The opponent scores when the ball passes your paddle
- First to reach the winning score wins (unlimited in current version)

## Game Mechanics

### Paddle Movement
The player controls the left paddle using the up and down arrow keys. The right paddle is controlled by the AI, which adjusts its behavior based on the selected difficulty level.

### Ball Physics
The ball moves at a constant speed but changes direction based on where it hits the paddles. Hitting the paddle near the center will return the ball at a shallow angle, while hitting near the edges will create a steeper angle.

### AI Difficulty Levels
- **Easy**: Slow reaction time, large error margin, and predictable movement
- **Medium**: Moderate reaction time and accuracy
- **Hard**: Quick reactions, high accuracy, and predictive movement

### Visual Effects
- The ball leaves a fading trail as it moves
- The ball changes color based on what it last collided with
- The center line is dashed to resemble a tennis court

## Project Structure

\`\`\`
enhanced-pong/
├── pong_game.py       # Main game file
├── assets/
│   ├── wall_collision.wav  # Sound effect for wall/paddle collisions
│   └── beep.wav            # Sound effect for scoring
├── screenshots/
│   └── gameplay.png        # Game screenshot
└── README.md               # This file
\`\`\`

## Dependencies

- **Pygame**: For game rendering, input handling, and sound
- **Python Standard Library**: math, random, time

## Future Improvements

- [ ] Add a main menu screen
- [ ] Implement a two-player mode
- [ ] Add power-ups that modify gameplay
- [ ] Create a high score system
- [ ] Add customizable paddle and ball appearances
- [ ] Implement different game modes (time attack, survival, etc.)
- [ ] Add background music and additional sound effects
- [ ] Create an options menu for customizing game settings

## Troubleshooting

### No Sound
If you encounter issues with sound:
1. Make sure the sound files (`wall_collision.wav` and `beep.wav`) are in the same directory as the game file
2. Check that your system's sound is working properly
3. Ensure Pygame's mixer is initialized correctly

### Performance Issues
If the game runs slowly:
1. Close other applications that might be using system resources
2. Reduce the window size by modifying the `WIDTH` and `HEIGHT` variables
3. Decrease the length of the ball trail by changing the `max_trail_length` variable

## Credits

This game is an enhanced version of the classic Pong arcade game originally created by Atari in 1972. The implementation uses Pygame, a set of Python modules designed for writing video games.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Pygame community for their excellent documentation and examples
- Inspired by the original Pong game by Atari
- Special thanks to all contributors and testers
\`\`\`

This README provides a comprehensive overview of your enhanced Pong game, making it easy for users to understand what the project is about, how to install and play it, and what features it offers. The structure follows GitHub best practices with clear sections, code blocks, and formatting.

You can add actual screenshots once you have the game running, and you might want to create a LICENSE file to specify how others can use your code. The README also includes a roadmap of future improvements to show potential contributors what you're planning to add.

Would you like me to make any adjustments to the README or provide any additional documentation for your GitHub repository?
\

