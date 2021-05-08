# Snake AI Project

### Description
This project is developed for 4450:498 special topics in computer engineering : Intelligent Systems to apply AI concepts learned in class.
The project is based on the original [snake game](https://en.wikipedia.org/wiki/Snake_(video_game_genre)). Code modified from [@TokyoEdTech](https://github.com/wynand1004/Projects/tree/master/Snake%20Game) uses the python standard library [Turtle](https://docs.python.org/3/library/turtle.html) package for graphics to demonstate intelligent behavior. 
The premise of the game is a singular block acts as the head of a snake that can only move in one of four direction (up, down, left, right), and cannot collide with itself. The snake grows an additional trailing segment for each food source obtained. Additional obstacles are added such as walls (black squares) that the snake is informed of that have an increased cost compared to empty spaces. The snake is not currently informed of traps (red triangles) which will cause the snake to "lose." Additional food objects "power pellets"(green arrows) make the snake "powered" for a short duration, during which the snake can destroy traps that it moves onto. 
In it's current state, this game demonstrates search algorithms including depth first search, breadth first search, uniform cost search, and A*. 


### Usage
A python interpreter version >= 3.10 is required

main.py can be ran with arguments specifying operation. See -h, --help argument for details
```bash
python.exe main.py --help
```