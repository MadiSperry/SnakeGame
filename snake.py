'''This code makes the game snake in a window. The constant variables defined first can be changed to adjust the game settings. 
Snake is a game where you eat food objects to grow the body by 1 square every time.
Input: Turning via 'arrow keys' or 'WASD'. 
Output: A window that can play the game snake
Author: MadiSperry
'''

# Organize imports
from tkinter import Tk, Canvas, Button, Label
from random import randint

# CONSTANT VARIABLES
GAME_WIDTH = 1000 # Default:  1000
GAME_HEIGHT = 800 # Default:  800
SPEED = 50 # Default:  50
SPACE_SIZE = 25 # Default:  25
BODY_PARTS = 3 # Default: 3 
SNAKE_COLOR = "#00FF00" # Default:  "#00FF00"
FOOD_COLOR = "#FF0000" # Default:  "#FF0000"
BACKGROUND_COLOR = "#000000" # Default:  "#000000"

# Define Starting Variables
score = 0
direction = 'DOWN'

class Snake():
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')
            self.squares.append(square)

class Food():
    def __init__(self):
        x = randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        y = randint(0, (GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x,y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tag='food')

# Each turn is 1 movement of the snake by 1 sqare in the direction set. Also checks if the snake is on a food item.
def next_turn(snake, food):
    x,y = snake.coordinates[0]
    if direction == 'UP':
        y -= SPACE_SIZE
    elif direction == 'DOWN':
        y += SPACE_SIZE
    elif direction == 'LEFT':
        x -= SPACE_SIZE
    elif direction == 'RIGHT':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        score_label.config(text = "Score: {}".format(score))
        canvas.delete('food')
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

# Called to change direction of snake(Cannot turn 180 degrees).
def change_direction(new_direction):
    global direction
    if new_direction == 'UP' and not direction == 'DOWN':
        direction = new_direction
    elif new_direction == 'DOWN' and not direction == 'UP':
        direction = new_direction
    elif new_direction == 'LEFT' and not direction == 'RIGHT':
        direction = new_direction
    elif new_direction == 'RIGHT' and not direction == 'LEFT':
        direction = new_direction

# Check for collisions with walls or snake body.
def check_collisions(snake):
    x,y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH-SPACE_SIZE+1:
        return True
    elif y < 0 or y >= GAME_HEIGHT-SPACE_SIZE+1:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

# Called when snake there is a collision.
def game_over():
    canvas.delete("all")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font = ("arial", 70), text = "GAME OVER", fill = "red", tag='game_over')

# Create window for entire game
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Create label that displays the score.
score_label = Label(window, text="Score: {}".format(score), font=('arial', 40))
score_label.pack()

# Create the game canvas.
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

# Create the start button.
start_button = Button(window, text='Start', font=('arial', 20), command=lambda: next_turn(snake, food))
start_button.pack()

# Update the window to display everything that has been create above.
window.update()

# Gets the size of window and screen.
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Center the window on the screen.
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Take keybinds and change direction of snake(Valid Inputs:  Arrow Keys or WASD).
window.bind('<Up>', lambda event: change_direction('UP'))
window.bind('<Down>', lambda event: change_direction('DOWN'))
window.bind('<Left>', lambda event: change_direction('LEFT'))
window.bind('<Right>', lambda event: change_direction('RIGHT'))
window.bind('<w>', lambda event: change_direction('UP'))
window.bind('<s>', lambda event: change_direction('DOWN'))
window.bind('<a>', lambda event: change_direction('LEFT'))
window.bind('<d>', lambda event: change_direction('RIGHT'))

# Create the snake and food objects.
snake = Snake()
food = Food()

# Required to keep the window open till closed.
window.mainloop()
