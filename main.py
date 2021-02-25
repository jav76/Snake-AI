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

class stateSpace:
    def __init__(self):
        self.snakes = []
        self.food = []
    def addSnake(self, player=True):
        self.snakes.append(snake(player))
    def addFood(self):
        self.food.append(food())


class food:
    def __init__(self, xPos=None, yPos=None):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("circle")
        self.head.color("red")
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
        self.head.color("black")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"
        if self.player:
            self.head.color("#00FF00") # Green
            wn.listen()
            wn.onkeypress(self.goUp, "w")
            wn.onkeypress(self.goDown, "s")
            wn.onkeypress(self.goLeft, "a")
            wn.onkeypress(self.goRight, "d")

    def addSegment(self):
        newSeg = turtle.Turtle()
        newSeg.speed(0)
        newSeg.shape("square")
        if self.player:
            newSeg.color("#80FF80") # Lighter green
        else:
            newSeg.color("grey")
        newSeg.penup()
        self.segments.append(newSeg)

    def goUp(self):
        if self.head.direction != "down":
            self.head.direction = "up"
    def goDown(self):
        if self.head.direction != "up":
            self.head.direction = "down"
    def goLeft(self):
        if self.head.direction != "right":
            self.head.direction = "left"
    def goRight(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move(self):
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


playerPen = turtle.Turtle()
playerPen.speed(0)
playerPen.penup()
playerPen.hideturtle()
playerPen.goto(-280, 240)
playerPen.write(f"Player score: {playerScore}\nHigh score: {playerHighScore}", align = "left",
                font=("Courier", 16, "normal"))

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
currentState.addSnake("player")
currentState.addFood()
wn.update()
# Main game loop
while True:
    wn.update()

    # Check for a collisions
    collision = False
    collisions = []
    for i in currentState.snakes:

        # Single snake collision with the border
        if i.head.xcor() > 290 or i.head.xcor() < -290 or i.head.ycor() > 290 or i.head.ycor() < -290:
            collision = True
            print("Snake collision with border")
            if i not in collisions:
                collisions.append(i)

        # Snake collision with itself
        for segment in i.segments:
            if segment.distance(i.head) < 20:
                collision = True
                print("Snake collision with itself")
                if i not in collisions:
                    collisions.append(i)

        # Snake collision with other snake
        for j in currentState.snakes:
            for segment in j.segments:
                if segment.distance(i.head) < 20:
                    print("Snake collision with other snake")
                    collision = True
                    if i not in collisions:
                        collisions.append(i)

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

    if collision:
        for i in collisions:
            i.head.color("red")
        wn.update()
        time.sleep(2)
        for i in collisions:
            i.head.direction = "stop"
            i.head.goto(0, 0)
            if i.player:
                i.head.color("#00FF00")
            else:
                i.head.color("black")
        for i in currentState.snakes:
            for j in i.segments:
                j.goto(1000, 1000)
            i.segments.clear()
        playerScore = 50
        agentScore = 50
    playerPen.clear()
    playerPen.write(f"Player score: {playerScore}\nHigh score: {playerHighScore}", align="left",
                    font=("Courier", 16, "normal"))
    agentPen.clear()
    agentPen.write(f"Agent score: {agentScore}\nHigh score: {agentHighScore}", align="right",
                   font=("Courier", 16, "normal"))

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