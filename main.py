from math import trunc
import pygame
from pygame.constants import MOUSEBUTTONDOWN 
from constants import *
import random

#Just some stuff pygame needs
def pygame_init():
    #Initialize all of the pygame modules
    pygame.init()
    #Setting caption for the game's window
    pygame.display.set_caption('Snake !')
    #Initialize a clock that we can use later
    clock = pygame.time.Clock()
    #Initialize the screen with its size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    #Setting the Surface of the game screen according to the screen screen we've created
    game_screen = pygame.Surface(screen.get_size())
    #Converting the game screen into pixels
    game_screen.convert()

    return clock, screen, game_screen

#Tile - Constructs the body
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.textures = SNAKE_BODY_IMAGE
    def change_pos(self,newx,newy):
        self.x = newx
        self.y = newy

#Head-Tile - Controls the movement of the body
class Head(Tile):
    def __init__(self, x, y, movement_x, movement_y, textures):
        super().__init__(x, y)
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.textures = textures

    def set_movement(self,new_movement_x, new_movement_y):
        self.movement_y = new_movement_y
        self.movement_x = new_movement_x
    
    def move(self):
        self.x += self.movement_x
        self.y += self.movement_y

#Fruit - Basic score mechanism component
class Fruit:
    def __init__(self, x, y, size, texture):
        self.x = x
        self.y = y
        self.size = size
        self.texture = texture
        draw_fruit(self)
    
    #----------------------------------------Shatzky-work----------------------------------------
    def regenerate(self, body, head, texture):
        x = random.randint(1, (int(PLAYING_AREA_X/GRID_SIZE) - 1)) * GRID_SIZE 
        y = random.randint(1, (int(PLAYING_AREA_Y/GRID_SIZE) - 1)) * GRID_SIZE
        while (check_collision_head(x,y,head)) or (check_collision_body(x, y, body)):
            x = random.randint(1, (int(PLAYING_AREA_X/GRID_SIZE) - 1)) * GRID_SIZE
            y = random.randint(1, (int(PLAYING_AREA_Y/GRID_SIZE) - 1)) * GRID_SIZE
        self.x = x
        self.y = y
        self.Set_Texture(texture)
    #----------------------------------------Shatzky-work-End----------------------------------------
    
    def Consumed(self, body, head, texture):
        body.append(Tile(body[len(body) - 1].x, body[len(body) - 1].y))
        self.regenerate(body, head, texture)

    def Set_Texture(self, texture):
        self.texture = texture

#Lawn Mower - Enemy that can harm the snake
class LawnMower:
    def __init__(self, cooldown, texture):
        self.cooldown = cooldown
        self.state = False
        self.texture = texture
    
    def attack(self, attacking_pointint):
        self.state = [attacking_pointint, SCREEN_HEIGHT]

    def set_state(self, state):
        self.state = state
        if not state:
            self.cooldown = LAWN_MOWER_COOLDOWN
    
    def tick(self):
        self.cooldown -= 1

#Draws the snake head
def draw_head(head, direction, happy):
    head.move()
    texture = ""
    if happy < 0:
        texture = pygame.image.load(head.textures[0])
        if direction == "right":
            texture = pygame.transform.rotate(texture, -90)
        elif direction == "down":
            texture = texture = pygame.transform.rotate(texture, 180)
        elif direction == "left":
            texture = pygame.transform.rotate(texture, 90)
        return (pygame.transform.scale(texture, (SNEAK_HEAD_SIZE_X, SNEAK_HEAD_SIZE_Y)))
    else:
        texture = pygame.image.load(head.textures[1])
        if direction == "right":
            texture = pygame.transform.rotate(texture, -90)
        elif direction == "down":
            texture = pygame.transform.rotate(texture, 180)
        elif direction == "left":
            texture = pygame.transform.rotate(texture, 90)
        return (pygame.transform.scale(texture, (HAPPY_SNEAK_HEAD_SIZE_X, HAPPY_SNEAK_HEAD_SIZE_Y)))

#Draws a tile for each snake's square
def draw_body(screen, body, last_x, last_y, direction):
    for tile in body:
        tempx = tile.x
        tempy = tile.y
        tile.change_pos(last_x,last_y)
        last_x = tempx
        last_y = tempy
    for tile in body:
        texture = pygame.image.load(tile.textures)
        if direction == "up" or direction == "down":
            texture = pygame.transform.rotate(texture, 90)
        body_asset = (pygame.transform.scale(texture, (SNEAK_BODY_SIZE, SNEAK_BODY_SIZE - 5)))
        screen.blit(body_asset, (tile.x, tile.y))

#Draws the Fruit
def draw_fruit(fruit):
    return (pygame.transform.scale(fruit.texture, (FRUIT_SIZE, FRUIT_SIZE)))

#Draws the lawn mower
def draw_lawn_mower(Lawn_Mower):
    asset = (pygame.transform.scale(Lawn_Mower.texture, (LAWN_MOWER_SIZE_X, LAWN_MOWER_SIZE_Y + 2)))
    Lawn_Mower.set_state([Lawn_Mower.state[0], Lawn_Mower.state[1] - MOVEMENT_SPEED/2])
    return asset

#Draws warning for lawn mower
def draw_warning():
    warning = (pygame.transform.scale(pygame.image.load(LAWN_MOWER_WARNING_IMAGE), (LAWN_MOWER_WARNING_SIZE, LAWN_MOWER_WARNING_SIZE)))
    return warning

#----------------------------------------Shatzky-work----------------------------------------
#Checks for collision with snake body
def check_collision_body(x, y, body):
    for tile in body:
        if tile.x == x and tile.y == y:
            return True
    return False
#----------------------------------------Shatzky-work-End----------------------------------------

#----------------------------------------Shatzky-work----------------------------------------
#Checks for collision with snake's head
def check_collision_head(x, y, head):
    if (head.x == x) and (head.y == y):
        return True
    return False 
#----------------------------------------Shatzky-work-End----------------------------------------

#Checks if snake tries to cross a border and teleport accordingly
def check_border(head):
    newy =  head.y
    newx = head.x
    if (head.x >= SCREEN_WIDTH):
        newx = -GRID_SIZE
    elif (head.x < -GRID_SIZE):
        newx = SCREEN_WIDTH
    elif (head.y >= SCREEN_HEIGHT):
        newy = -GRID_SIZE
    elif (head.y < -GRID_SIZE):
        newy = SCREEN_HEIGHT
    head.change_pos(newx,newy)

#Handle lawn mower state:
def handle_lawn_mower(screen, Lawn_Mower):
    if Lawn_Mower.state != False:
        if Lawn_Mower.state[1] <= -LAWN_MOWER_SIZE_Y:
            Lawn_Mower.set_state(False)
        else:
            screen.blit(draw_lawn_mower(Lawn_Mower), (Lawn_Mower.state[0], Lawn_Mower.state[1]))
    elif Lawn_Mower.cooldown <= int(LAWN_MOWER_COOLDOWN/3):
        screen.blit(draw_warning(), (PLAYING_AREA_X - 10, ((SCREEN_HEIGHT - PLAYING_AREA_Y)/2) - 15))

#Renders current score on given screen
def render_score(screen, score):
    score_text = pygame.font.Font(SCORE_FONT, 32)
    score_text = score_text.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (5,5))

def main():
    clock, screen, game_screen = pygame_init()
    #Basic game vars \ objects (fruit, snake, score etc..)
    Snake_Head = Head(30, 30, MOVEMENT_SPEED, 0, SNAKE_IMAGE_ARRAY)
    body = [Tile(0,30)]
    fruit = Fruit(30, 30, GRID_SIZE, pygame.image.load(FRUIT_IMAGE_ARRAY[random.randint(0,len(FRUIT_IMAGE_ARRAY) - 1)]))
    Lawn_Mower = LawnMower(LAWN_MOWER_COOLDOWN, pygame.image.load(LAWN_MOWER_IMAGE))
    bush_asset = pygame.image.load(BUSH_IMAGE)
    score = 0
    last_key = "right"
    happy = 0


    #main game loop
    while True:
        #Checking if game is not over
        if check_collision_body(Snake_Head.x , Snake_Head.y, body):
            pygame.quit()
        #input handling
    #----------------------------------------Shatzky-work----------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_UP:
                    if last_key != "down":
                        last_key = "up"
                        Snake_Head.set_movement(0,-MOVEMENT_SPEED)
                elif event.key == pygame.K_DOWN:
                    if last_key != "up":
                        last_key = "down"
                        Snake_Head.set_movement(0,MOVEMENT_SPEED)
                elif event.key == pygame.K_LEFT:
                    if last_key != "right":
                        last_key = "left"
                        Snake_Head.set_movement(-MOVEMENT_SPEED,0)
                elif event.key == pygame.K_RIGHT:
                    if last_key != "left":
                        last_key = "right"
                        Snake_Head.set_movement(MOVEMENT_SPEED,0)
    #----------------------------------------Shatzky-work-End----------------------------------------
        
        #--for each frame:
        
        #-checking for borders (head w/ game-borders \ head w/ body \ head w/ fruit)
        check_border(Snake_Head)
        if check_collision_head(fruit.x, fruit.y, Snake_Head):
            texture = pygame.image.load(FRUIT_IMAGE_ARRAY[random.randint(0,len(FRUIT_IMAGE_ARRAY) - 1)])
            fruit.Consumed(body,Snake_Head, texture)
            happy = 10
            score += 1
        else:
            happy -= 1
        if Lawn_Mower.state == False:
            if Lawn_Mower.cooldown <= 0:
                Lawn_Mower.attack(random.randint(1,(int(PLAYING_AREA_X/MOVEMENT_SPEED) - 1)) * MOVEMENT_SPEED)
            else:
                Lawn_Mower.tick()

        #-redrawing game assets according to movement
        oldx = Snake_Head.x
        oldy = Snake_Head.y
        head_asset = draw_head(Snake_Head, last_key, happy)
        draw_body(game_screen,body, oldx, oldy, last_key)
        fruit_asset = draw_fruit(fruit)
        
        #-screen blitting, background filling and score rendering
        screen.blit(game_screen, (0,0))
        screen.blit(fruit_asset, (fruit.x, fruit.y))
        screen.blit(head_asset, (Snake_Head.x - 2, Snake_Head.y - 3))
        handle_lawn_mower(screen, Lawn_Mower)
        game_screen.fill(BACKGROUND_COLOR)
        screen.blit(bush_asset, (0,0))
        render_score(screen, score)

        #-general game stuff
        clock.tick(GAME_SPEED) #next-frame
        pygame.display.update() #update display                    

main()
#unInitialize all of the pygame modules