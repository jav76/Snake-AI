import turtle
import time
import random

random.seed()
delay = 0.1

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
        self.walls = []
        self.traps = []
    def addSnake(self, name, player=True):
        newSnake = snake(name, player)
        newSnake.head.goto(random.randint(-200, 200), random.randint(-200, 200))
        self.snakes.append(newSnake)
    def addFood(self, xPos=None, yPos=None):
        if self.isEmpty(xPos, yPos):
            newFood = food(xPos, yPos)
            self.food.append(newFood)
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
        if self.getObject(xPos, yPos)[1] == None:
            return True
        else:
            return False

    def getObject(self, xPos, yPos):

        # snakes
        for i in self.snakes:
            pos = posToTup(i.head)
            if pos == (xPos, yPos):
                return ["head", i]
            for j in i.segments:
                pos = posToTup(j.head)
                if pos == (xPos, yPos):
                    return ["segment", j]

        # food
        for i in self.food:
            pos = posToTup(i.head)
            if pos == (xPos, yPos):
                return ["food", i]

        # walls
        for i in self.walls:
            pos = posToTup(i.head)
            if pos == (xPos, yPos):
                return ["wall", i]

        # traps
        for i in self.traps:
            pos = posToTup(i.head)
            if pos == (xPos, yPos):
                return ["trap", i]
        return ["empty", None]


class wall:
    def __init__(self, xPos, yPos):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.color("black")
        self.head.shape("square")
        self.head.penup()
        self.head.goto(xPos, yPos)

class trap:
    def __init__(self, xPos, yPos):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.color("red")
        self.head.shape("triangle")
        self.head.penup()
        self.head.goto(xPos, yPos)


class food:
    def __init__(self, xPos=None, yPos=None):
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
        self.head.direction = "stop"
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


    def addDirection(self, direction):
        if direction != reverseDirection(self.head.direction):
            self.head.directions.append(direction)
        else:
            self.head.directions.append(self.head.direction)

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

class searchNode:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos

    def successorNodes(self, ss):
        nodes = []
        # If the next space up is empty, add it to the successor nodes list
        if ss.isEmpty(self.pos[0], self.pos[1] + 20):
            nodes.append(searchNode("up", (self.pos[0], self.pos[1] + 20)))
        if ss.isEmpty(self.pos[0], self.pos[1] - 20):
            nodes.append(searchNode("down", (self.pos[0], self.pos[1] - 20)))
        if ss.isEmpty(self.pos[0] + 20, self.pos[1]):
            nodes.append(searchNode("right", (self.pos[0], self.pos[1] - 20)))
        if ss.isEmpty(self.pos[0] - 20, self.pos[1]):
            nodes.append(searchNode("left", (self.pos[0], self.pos[1] - 20)))






"""
playerPen = turtle.Turtle()
playerPen.speed(0)
playerPen.penup()
playerPen.hideturtle()
playerPen.goto(-280, 240)
playerPen.write(f"Player score: {playerScore}\nHigh score: {playerHighScore}", align = "left",
                font=("Courier", 16, "normal"))
"""
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

wallX = 50
wallY = 50
for i in range(1, 5):
    currentState.addWall(wallX, wallY)
    wallX = wallX + 20 * random.choice([-1, 0, 1])
    wallY = wallY + 20 * random.choice([-1, 0, 1])

currentState.addTrap(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)

wn.update()
# Main game loop
while True:
    wn.update()

    # Agent control
    for i in currentState.snakes:
        if not i.player:
            rand = random.randint(1, 4)
            if rand == 1:
                i.addDirection("up")
            elif rand == 2:
                i.addDirection("down")
            elif rand == 3:
                i.addDirection("left")
            else:
                i.addDirection("right")


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
                    collision.append([i, "other"])

        # Snake collision with food
        for j in currentState.food:
            if j.head.distance(i.head) < 20:
                print("Snake collision with food")
                foodX = random.randint(-270, 270)
                foodY = random.randint(-270, 270)
                j.head.goto(foodX, foodY)

                i.addSegment()
                if i.player:
                    playerScore += 25
                    if playerScore > playerHighScore:
                        playerHighScore = playerScore
                else:
                    agentScore += 25
                    if agentScore > agentHighScore:
                        agentHighScore = agentScore

        # Snake collision with wall
        for j in currentState.walls:
            if j.head.distance(i.head) < 20:
                print("Snake collision with wall")
                collision[0] = True
                collision.append([i, "wall"])

        # Snake collision with trap
        for j in currentState.traps:
            if j.head.distance(i.head) < 20:
                print("Snake collision with trap")
                collision[0] = True
                collision.append([i, "trap"])

    if collision[0]:
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
        i.move()
        if i.head.direction != "stop":
            if i.player:
                playerScore -= 1
            else:
                agentScore -= 1

    time.sleep(delay)

wn.mainloop()

# Based on snake code by by @TokyoEdTech