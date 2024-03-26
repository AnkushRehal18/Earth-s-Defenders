import pygame 
import random
import math

pygame.init() # initializing pygame

#creating a window
display = pygame.display.set_mode((700,600))
#background image 
background = pygame.image.load("space_background.jpg")
#name of the game 
pygame.display.set_caption("Earth's Defenders")
#logo of the image 
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#player rocket image 
playerImg = pygame.image.load("players_rocket.png")
player_on_xaxis = 320
player_on_yaxis = 480
player_position_change = 0

def player_rocket(x,y):
    display.blit(playerImg , (x , y))

#enemy image and enemy functions 
alien_image = []
alien_xaxis = []
alien_yaxis = [] 
enemy_position_changeX = []
enemy_position_changeY = []

number_of_aliens = 6 

for i in range(number_of_aliens):

    alien_image.append(pygame.image.load("alien.png"))
    alien_xaxis.append(random.randint(0, 620))
    alien_yaxis.append(random.randint(50, 100))
    enemy_position_changeX.append(0.2)
    enemy_position_changeY.append(0)

def enemy(x, y, i):
    display.blit(alien_image[i] , (x, y))

#bullet image 
bullet_image = pygame.image.load("bullets.png")
bullet_xaxis = 0
bullet_yaxis = 480
bullet_position_changeX = 0
bullet_position_changeY = 0.8
bullet_state = "ready"  #ready means we cant see the bullet on screen and fire means we can see it
#score 
score_value = 0 
font = pygame.font.Font("freesansbold.ttf",32)

text_X = 10 
text_Y = 10

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    display.blit(score ,( x , y) )

def fire_bullet(x,y):
    global bullet_state 
    bullet_state = "fire"
    display.blit(bullet_image ,(x+16,y+10))

#game variable
exit_game = False

def iscollision(alien_xaxis,alien_yaxis,bullet_xaxis,bullet_yaxis):
    distance = math.sqrt((math.pow(alien_xaxis-bullet_xaxis,2))+(math.pow(alien_yaxis - bullet_yaxis,2)))
    if distance < 27:
        return True
    else:
        return False

while not exit_game: #game loop which continuously shows the window
    display.fill((0,0,0))
    display.blit(background ,(0,0))
    for event in pygame.event.get():  #getting the events 
        if event.type == pygame.QUIT: #if event == quit then close the game
            exit_game = True

        #checking keystrokes for the moving 
        if event.type == pygame.KEYDOWN: #checks if a key has been pressed
            if event.key == pygame.K_LEFT:
                player_position_change = -0.2
            if event.key == pygame.K_RIGHT:
                player_position_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # Ensure only one bullet is fired at a time
                    bullet_xaxis = player_on_xaxis  # Set bullet's initial x-position to player's x-position
                    fire_bullet(bullet_xaxis, bullet_yaxis)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_position_change = 0

    player_on_xaxis += player_position_change
    #restrict the spaceship from leaving the window 
    if player_on_xaxis <= 0:
        player_on_xaxis = 0
    elif player_on_xaxis >= 630:
        player_on_xaxis = 630

    # Move the alien and handle boundary bouncing
    for i in range(number_of_aliens):
        alien_xaxis[i] += enemy_position_changeX[i]
        if alien_xaxis[i] <= 0:
            enemy_position_changeX[i] = 0.2  # Change direction to right
            alien_yaxis[i] += 50  # Move down
        elif alien_xaxis[i] >= 630:
            enemy_position_changeX[i] = -0.2  # Change direction to left
            alien_yaxis[i] += 50  # Move down
        #collision detection 
        collision = iscollision(alien_xaxis[i] , alien_yaxis[i] , bullet_xaxis , bullet_yaxis)
        if collision:
            bullet_yaxis = 480
            bullet_state = "ready"
            score_value +=1
            print(score_value)
            alien_xaxis[i] = random.randint(0, 620)
            alien_yaxis[i] = random.randint(50, 100)

        enemy(alien_xaxis[i] , alien_yaxis[i] , i)

    #bullet movement 
    if bullet_yaxis <=0:
        bullet_yaxis = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_xaxis, bullet_yaxis)
        bullet_yaxis -= bullet_position_changeY

    player_rocket(player_on_xaxis, player_on_yaxis)
    
    show_score(text_X , text_Y)

    
    pygame.display.update()
    
pygame.quit()
