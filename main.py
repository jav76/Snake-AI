import turtle
import time, sys, argparse
import random

random.seed()
delay = 0.1
powerPelletDuration = 5

"""
TODO:
Add power pellets in addition to regular food that give snake power to delete traps within some duration (done?)
Add noisy sensor for position of traps
Add parameters for running different algorithms and update README for usage (done?)
"""

# Score
playerScore = 50
playerHighScore = 50
agentScore = 50
agentHighScore = 50

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("white")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

def posToTup(t):
    return (t.pos()[0], t.pos()[1])

def getDistance(x1, y1, x2, y2):
    return ( (x2 - x1)**2 + (y2 - y1)**2 ) ** (1/2)

def getManhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def heuristic(node):
    return ( getDistance(node.pos[0], node.pos[1], node.goal[0], node.goal[1]) + getManhattan(node.pos[0], node.pos[1], node.goal[0], node.goal[1]) ) * 0.9

def reverseDirection(direction):
    if direction == "up":
        return "down"
    elif direction == "down":
        return "up"
    elif direction == "left":
        return "right"
    elif direction == "right":
        return "left"
    else:
        return "stop"


class stateSpace:
    def __init__(self):
        self.snakes = []
        self.food = []
        self.powerPellets = []
        self.walls = []
        self.traps = []
    def addSnake(self, name, player=True):
        newSnake = snake(name, player)
        newSnake.head.goto(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)
        self.snakes.append(newSnake)
    def addFood(self, xPos=None, yPos=None):
        if self.isEmpty(xPos, yPos):
            newFood = food(xPos, yPos)
            self.food.append(newFood)
            return 0
        else:
            return 1
    def addPowerPellet(self, xPos=None, yPos=None):
        if self.isEmpty(xPos, yPos):
            newPellet = powerPellet(xPos, yPos)
            self.powerPellets.append(newPellet)
            return 0
        else:
            return 1
    def addWall(self, xPos, yPos):
        if self.isEmpty(xPos, yPos):
            newWall = wall(xPos, yPos)
            self.walls.append(newWall)
            return 0
        else:
            return 1
    def addTrap(self, xPos, yPos):
        if self.isEmpty(xPos, yPos):
            newTrap = trap(xPos, yPos)
            self.traps.append(newTrap)
            return 0
        else:
            return 1

    def isEmpty(self, xPos, yPos):
        if self.getObject(xPos, yPos)[0] == "empty":
            return True
        else:
            return False

    def getObject(self, xPos, yPos):


        if xPos == None or yPos == None:
            return ["empty", None]

        # snakes
        for i in self.snakes:
            pos = posToTup(i.head)
            dist = getDistance(pos[0], pos[1], xPos, yPos)
            if i.head.distance((xPos, yPos)) < 20:
                return ["head", i]
            for j in i.segments:
                pos = posToTup(j)
                if pos == (xPos, yPos):
                    return ["segment", j]

        # food
        for i in self.food:
            pos = posToTup(i.head)
            dist = getDistance(pos[0], pos[1], xPos, yPos)
            if i.head.distance((xPos, yPos)) < 20:
                return ["food", i]

        # power pellets
        for i in self.powerPellets:
            pos = posToTup(i.head)
            dist = getDistance(pos[0], pos[1], xPos, yPos)
            if i.head.distance((xPos, yPos)) < 20:
                return ["powerPellet", i]

        # walls
        for i in self.walls:
            pos = posToTup(i.head)
            dist = getDistance(pos[0], pos[1], xPos, yPos)
            if i.head.distance((xPos, yPos)) < 20:
                return ["wall", i]

        #border
        if xPos >= 270 or xPos <= -270 or yPos >= 270 or yPos <= -270:
            return ["border", None]

        # traps
        for i in self.traps:
            pos = posToTup(i.head)
            dist = getDistance(pos[0], pos[1], xPos, yPos)
            if i.head.distance((xPos, yPos)) < 20:
                return ["trap", i]

        return ["empty", None]

    def getEmpty(self, rand=True):
        empties = []
        for x in range(-28, 28):
            for y in range(-28, 28):
                if self.getObject(x * 10, y * 10)[0] == "empty":
                    pos = (x * 10, y * 10)
                    empties.append(pos)

        if rand:
            return empties[random.randint(0, len(empties) - 1)]

    def closeToFood(self, currentSnake, currentFood,  distance=40):
        headPos = posToTup(currentSnake.head)
        foodPos = posToTup(currentFood.head)
        return getDistance(headPos[0], headPos[1], foodPos[0], foodPos[1]) <= distance

    def inCorner(self, currentSnake):
        corners = [
            [270, 270],
            [-270, 270],
            [270, -270],
            [-270, -270]
        ]
        headPos = posToTup(currentSnake.head)
        for i in corners:
            if getDistance(headPos[0], headPos[1], i[0], i[1]) <= 20:
                return True
        return False

    def noisySensor(self):
        return NotImplemented


class wall:
    def __init__(self, xPos, yPos, cost=10):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.color("black")
        self.head.shape("square")
        self.head.penup()
        self.head.goto(xPos, yPos)
        self.cost = cost

class trap:
    def __init__(self, xPos, yPos, cost=50):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.color("red")
        self.head.shape("triangle")
        self.head.penup()
        self.head.goto(xPos, yPos)
        self.cost = cost


class food:
    def __init__(self, xPos=None, yPos=None, reward=10):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("circle")
        self.head.color("blue")
        self.head.penup()
        if xPos is None:
            xPos = random.randint(-290, 290)
        if yPos is None:
            yPos = random.randint(-290, 290)
        self.head.goto(xPos, yPos)
        self.reward = reward

class powerPellet:
    def __init__(self, xPos=None, yPos=None, reward=20):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("arrow")
        self.head.color("green")
        self.head.penup()
        if xPos is None:
            xPos = random.randint(-290, 290)
        if yPos is None:
            yPos = random.randint(-290, 290)
        self.head.goto(xPos, yPos)
        self.reward = reward


class snake:
    def __init__(self, name, player=True):
        self.player = player
        self.name = name
        self.segments = []
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shapesize(1, 1)
        self.head.shape("square")
        self.head.color("grey")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.directions = []
        self.head.direction = "up"
        self.powered = False
        self.powerDuration = 0
        if self.player:
            self.head.color("#00FF00") # Green
            wn.listen()
            wn.onkeypress(self.addDirection("up"), "w")
            wn.onkeypress(self.addDirection("down"), "s")
            wn.onkeypress(self.addDirection("left"), "a")
            wn.onkeypress(self.addDirection("right"), "d")

    def addSegment(self):
        newSeg = turtle.Turtle()
        newSeg.speed(0)
        newSeg.shape("square")
        if self.player:
            newSeg.color("#80FF80") # Lighter green
        else:
            newSeg.color("#B4B4B4") # Lighter grey
        newSeg.penup()
        self.segments.append(newSeg)
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)


    def addDirection(self, direction):
        """
        if self.head.directions:
            if direction != reverseDirection(self.head.directions[-1]):
                self.head.directions.append(direction)
            else:
                self.head.directions.append(self.head.direction)
        else:
            self.head.directions.append(self.head.direction)
        """
        self.head.directions.append(direction)

    def move(self):
        self.head.direction = self.head.directions.pop(0)
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)
        if len(self.segments) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.segments[0].goto(x, y)
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + 20)
        if self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - 20)
        if self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - 20)
        if self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + 20)

    # state space,  (goalX, goalY)
    def dfs(self, ss, goal):
        visited = []
        queue = []
        startNode = searchNode(self.head.direction, posToTup(self.head), [], goal)

        queue.append(startNode)

        while queue:
            currentNode = queue.pop()
            print(f"Current direction: {currentNode.direction}")
            print(f"Current pos: {currentNode.pos}")
            print(f"Distance: {getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) }")
            if getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) < 20:
                currentNode.path.append(currentNode)
                return currentNode.path
            visited.append(currentNode)
            for i in currentNode.successorNodes(ss):
                if i not in visited:
                    visited.append(i)
                    i.path = currentNode.path.copy()
                    i.path.append(i)
                    queue.append(i)
        return None

    def bfs(self, ss, goal):
        visited = []
        queue = []
        startNode = searchNode(self.head.direction, posToTup(self.head), [], goal)

        queue.append(startNode)

        while queue:
            currentNode = queue.pop(0)
            #print(f"Current direction: {currentNode.direction}")
            #print(f"Current pos: {currentNode.pos}")
            #print(f"Distance: {getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) }")
            if getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) < 20:
                return currentNode.path
            visited.append(currentNode)
            for i in currentNode.successorNodes(ss):
                if i not in visited:
                    visited.append(i)
                    i.path = currentNode.path.copy()
                    i.path.append(i)
                    queue.append(i)
        return None

    def ucs(self, ss, goal):
        visited = []
        queue = []
        startNode = searchNode(self.head.direction, posToTup(self.head), [], goal)

        queue.append(startNode)

        while queue:
            queue.sort(key = lambda x: x.cost)
            currentNode = queue.pop(0)
            print(f"Current direction: {currentNode.direction}")
            print(f"Current pos: {currentNode.pos}")
            print(f"Distance: {getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) }")
            if getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) < 20:
                currentNode.path.append(currentNode)
                return currentNode.path
            visited.append(currentNode)
            for i in currentNode.successorNodes(ss):
                if i not in visited:
                    visited.append(i)
                    i.path = currentNode.path.copy()
                    i.path.append(i)
                    queue.append(i)
        return None

    def aStar(self, ss, goal):
        visited = []
        queue = []
        startNode = searchNode(self.head.direction, posToTup(self.head), [], goal)

        queue.append(startNode)

        while queue:
            queue.sort(key = heuristic)
            currentNode = queue.pop(0)
            print(f"Current direction: {currentNode.direction}")
            print(f"Current pos: {currentNode.pos}")
            print(f"Distance: {getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) }")
            if getDistance(goal[0], goal[1], currentNode.pos[0], currentNode.pos[1]) < 20:
                currentNode.path.append(currentNode)
                return currentNode.path
            visited.append(currentNode)
            for i in currentNode.successorNodes(ss):
                if i not in visited:
                    visited.append(i)
                    i.path = currentNode.path.copy()
                    i.path.append(i)
                    queue.append(i)
        return None




class searchNode:
    def __init__(self, direction, pos, path, goal, cost=False):
        self.direction = direction
        self.pos = pos
        self.path = path
        self.cost = cost
        self.goal = goal

    def __eq__(self, other):
        return self.direction == other.direction and self.pos == other.pos
    def __hash__(self):
        return hash(self.direction, self.pos)


    def successorNodes(self, ss):
        nodes = []
        if self.cost == False:
            # If the next space up is empty, add it to the successor nodes list
            nextObject = ss.getObject(self.pos[0], self.pos[1] + 20)[0]
            if nextObject == "empty" or nextObject == "trap" or nextObject == "food" or nextObject == "powerPellet":
                nodes.append(searchNode("up", (self.pos[0], self.pos[1] + 20), self.path, self.goal))

            nextObject = ss.getObject(self.pos[0], self.pos[1] - 20)[0]
            if nextObject == "empty" or nextObject == "trap" or nextObject == "food" or nextObject == "powerPellet":
                nodes.append(searchNode("down", (self.pos[0], self.pos[1] - 20), self.path, self.goal))

            nextObject = ss.getObject(self.pos[0] + 20, self.pos[1])[0]
            if nextObject == "empty" or nextObject == "trap" or nextObject == "food" or nextObject == "powerPellet":
                nodes.append(searchNode("right", (self.pos[0] + 20, self.pos[1]), self.path, self.goal))

            nextObject = ss.getObject(self.pos[0] - 20, self.pos[1])[0]
            if nextObject == "empty" or nextObject == "trap" or nextObject == "food" or nextObject == "powerPellet":
                nodes.append(searchNode("left", (self.pos[0] - 20, self.pos[1]), self.path, self.goal))

        else:
            nextObject = ss.getObject(self.pos[0], self.pos[1] + 20)[0]
            if nextObject == "wall":
                nodes.append(searchNode("up", (self.pos[0], self.pos[1] + 20), self.path, self.goal, nextObject.cost))
            else:
                nodes.append(searchNode("up", (self.pos[0], self.pos[1] + 20), self.path, self.goal, 1))

            nextObject = ss.getObject(self.pos[0], self.pos[1] - 20)[0]
            if nextObject == "wall":
                nodes.append(searchNode("down", (self.pos[0], self.pos[1] - 20), self.path, self.goal, nextObject.cost))
            else:
                nodes.append(searchNode("down", (self.pos[0], self.pos[1] - 20), self.path, self.goal, 1))

            nextObject = ss.getObject(self.pos[0] + 20, self.pos[1])[0]
            if nextObject == "wall":
                nodes.append(searchNode("right", (self.pos[0] + 20, self.pos[1]), self.path, self.goal, nextObject.cost))
            else:
                nodes.append(searchNode("right", (self.pos[0], self.pos[1] - 20), self.path, self.goal, 1))

            nextObject = ss.getObject(self.pos[0] - 20, self.pos[1])[0]
            if nextObject == "wall":
                nodes.append(searchNode("left", (self.pos[0] - 20, self.pos[1]), self.path, self.goal, nextObject.cost))
            else:
                nodes.append(searchNode("left", (self.pos[0], self.pos[1] - 20), self.path, self.goal, 1))


        if nodes:
            for i in nodes:
                if i.direction == reverseDirection(self.direction):
                    nodes.remove(i)
        return nodes






"""
playerPen = turtle.Turtle()
playerPen.speed(0)
playerPen.penup()
playerPen.hideturtle()
playerPen.goto(-280, 240)
playerPen.write(f"Player score: {playerScore}\nHigh score: {playerHighScore}", align = "left",
                font=("Courier", 16, "normal"))
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    algorithmGroup = parser.add_mutually_exclusive_group()
    algorithmGroup.add_argument("-a", "--algorithm",
                                type = str,
                                help = "Specify which search algorithm to use.",
                                choices = ["dfs", "bfs", "ucs", "astar"],
                                default = "astar"
                                )
    args = parser.parse_args()


    algorithm = args.algorithm

    agentPen = turtle.Turtle()
    agentPen.speed(0)
    agentPen.penup()
    agentPen.hideturtle()
    agentPen.goto(280, 240)
    agentPen.write(f"Agent score: {agentScore}\nHigh score: {agentHighScore}", align = "right",
                   font=("Courier", 16, "normal"))

    miscPen = turtle.Turtle()
    miscPen.speed(0)
    miscPen.penup()
    miscPen.hideturtle()
    miscPen.goto(0, 200)



    currentState = stateSpace()
    #currentState.addSnake("player")
    #currentState.addFood()
    currentState.addSnake("agent", False)
    currentState.addFood()
    currentState.addPowerPellet()
    currentState.addPowerPellet()
    currentState.addPowerPellet()
    currentState.addPowerPellet()


    wallX = random.randint(-12, 12) * 20
    wallY = random.randint(-12, 12) * 20
    for i in range(1, 10):
        currentState.addWall(wallX, wallY)
        wallX = wallX + 20 * random.choice([-1, 0, 1])
        wallY = wallY + 20 * random.choice([-1, 0, 1])
    wallX = random.randint(-12, 12) * 20
    wallY = random.randint(-12, 12) * 20
    for i in range(1, 10):
        currentState.addWall(wallX, wallY)
        wallX = wallX + 20 * random.choice([-1, 0, 1])
        wallY = wallY + 20 * random.choice([-1, 0, 1])

    currentState.addTrap(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)
    currentState.addTrap(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)
    currentState.addTrap(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)
    currentState.addTrap(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)


    searched = False

    wn.update()
    # Main game loop
    while True:
        wn.update()

        # Agent control
        for i in currentState.snakes:
            if not i.player:
                """
                rand = random.randint(1, 4)
                if rand == 1:
                    i.addDirection("up")
                elif rand == 2:
                    i.addDirection("down")
                elif rand == 3:
                    i.addDirection("left")
                else:
                    i.addDirection("right")
                """

                """
                # Run a search one time at the start and add the search path to the direction queue
                # Searches currently seem to have an issue with "switching directions" from the initial given direction
                if not searched:
                    i.head.direction = "down"
                    path = i.bfs(currentState, posToTup(currentState.food[0].head))
                    for j in path:
                        print(j.direction)
                        i.addDirection(j.direction)
                    searched = True
                """

                if len(i.head.directions) == 0:
                    path = []
                    match algorithm:
                        case "dfs":
                            path = i.dfs(currentState, posToTup(currentState.food[0].head))
                        case "bfs":
                            path = i.bfs(currentState, posToTup(currentState.food[0].head))
                        case "ucs":
                            path = i.ucs(currentState, posToTup(currentState.food[0].head))
                        case "astar":
                            path = i.aStar(currentState, posToTup(currentState.food[0].head))

                    if path is not None:
                        for j in path:
                            i.addDirection(j.direction)




        # Check for a collisions
        collision = [False]
        for i in currentState.snakes:

            # Single snake collision with the border
            if i.head.xcor() > 290 or i.head.xcor() < -290 or i.head.ycor() > 290 or i.head.ycor() < -290:
                collision[0] = True
                print("Snake collision with border")
                collision.append([i, "border"])

            # Snake collision with itself
            for segment in i.segments:
                if segment.distance(i.head) < 20:
                    collision[0] = True
                    print("Snake collision with itself")
                    collision.append([i, "self"])

            # Snake collision with other snake
            for j in currentState.snakes:
                for segment in j.segments:
                    if segment.distance(i.head) < 20:
                        print("Snake collision with other snake")
                        collision[0] = True
                        collision.append([i, "other", j])

            # Snake collision with food
            for j in currentState.food:
                if j.head.distance(i.head) < 20:
                    print("Snake collision with food")
                    newPos = currentState.getEmpty()
                    foodX = newPos[0]
                    foodY = newPos[1]
                    j.head.goto(foodX, foodY)

                    i.addSegment()
                    if i.player:
                        playerScore += j.reward
                        if playerScore > playerHighScore:
                            playerHighScore = playerScore
                    else:
                        agentScore += j.reward
                        if agentScore > agentHighScore:
                            agentHighScore = agentScore

            # Snake collision with power pellet
            for j in currentState.powerPellets:
                if j.head.distance(i.head) < 20:
                    print("Snake collision with power pellet")
                    i.powered = True
                    i.poweredDuration = powerPelletDuration
                    i.head.color("green")

            # Snake collision with wall
            for j in currentState.walls:
                if j.head.distance(i.head) < 20:
                    print("Snake collision with wall")
                    collision[0] = True
                    collision.append([i, "wall", j])

            # Snake collision with trap
            for j in currentState.traps:
                if j.head.distance(i.head) < 20:
                    print("Snake collision with trap")
                    if i.powered:
                        j.head.hideturtle()
                    else:
                        collision[0] = True
                        collision.append([i, "trap", j])


        if collision[0]:
            collision[1][0].head.directions.clear() # clear directions queue after a collision
            message = ""
            if collision[1][0].player:
                message += "Player collided with "
            else:
                message += "Agent collided with "
            if collision[1][1] == "border":
                message += "the border."
            elif collision[1][1] == "self":
                message += "themselves."
            elif collision[1][1] == "wall":
                message += "a wall"
            elif collision[1][1] == "trap":
                message += "a trap"
            elif collision[1][1] == "other":
                message += "another snake."
            miscPen.write(message, align="center", font=("Courier", 16, "normal"))


            collision[1][0].head.color("red")
            wn.update()
            time.sleep(2)
            collision[1][0].head.direction = "stop"
            collision[1][0].head.goto(0, 0)
            if collision[1][0].player:
                collision[1][0].head.color("#00FF00")
            else:
                collision[1][0].head.color("grey")
            for i in currentState.snakes:
                for j in i.segments:
                    j.goto(1000, 1000)
                i.segments.clear()
            playerScore = 50
            agentScore = 50
        """
        playerPen.clear()
        playerPen.write(f"Player score: {playerScore}\nHigh score: {playerHighScore}", align="left",
                        font=("Courier", 16, "normal"))
        """
        agentPen.clear()
        agentPen.write(f"Agent score: {agentScore}\nHigh score: {agentHighScore}", align="right",
                       font=("Courier", 16, "normal"))
        miscPen.clear()

        for i in currentState.snakes:
            if i.head.directions:
                i.move()
            if i.powered:
                i.poweredDuration = i.poweredDuration - delay
                if i.poweredDuration < delay:
                    i.powered = False
                    i.head.color("grey")
            if i.head.direction != "stop":
                if i.player:
                    playerScore -= 1
                else:
                    agentScore -= 1

        time.sleep(delay)

    wn.mainloop()

# Based on snake code by by @TokyoEdTech