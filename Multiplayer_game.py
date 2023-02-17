import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH,HIGHT =  900,500
WIN = pygame.display.set_mode( (WIDTH, HIGHT) )
pygame.display.set_caption("OUR INTERNSHIP PROJECT  [ ``MULTIPLAYER 2D Game`` ] ")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon((icon))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
PURPLE = (255,0,255)
YELLOW = (255,255,0)
BORDER = pygame.Rect(WIDTH//2, 0 , 1 , HIGHT)
BACKGROUND_SOUND = pygame.mixer.Sound('music.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

FPS = 120
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH = 61 
SPACE_HEIGHT = 50

BACKROUND_DISPLAY = pygame.image.load("Display1.jpg")
BACKROUND_DISPLAY2 = pygame.image.load("Display2.jpg")

YELLOW_SPACESHIP_IMAGE = pygame.image.load("spaceship(2).png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACE_HEIGHT)), 270) 
RED_SPACESHIP_IMAGE = pygame.image.load("spaceship(1).png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACE_HEIGHT)), 90)



def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(BACKROUND_DISPLAY,(0,0))
    BACKGROUND_SOUND.play()
    pygame.draw.rect(WIN,WHITE,BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x , yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x , red.y))
    
    red_health_text = HEALTH_FONT.render("HEALTH:" + str(red_health),1, RED )
    yellow_health_text = HEALTH_FONT.render("HEALTH:" + str(yellow_health),1, YELLOW )
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10 , 10))
    WIN.blit(yellow_health_text, (10 , 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED , bullet )
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW , bullet )
    pygame.display.update()

def red_handle_movements(keys_pressed,red):
    if keys_pressed[pygame.K_RIGHT] and red.x + 5 < WIDTH - 50 :
            red.x += 5
    if keys_pressed[pygame.K_DOWN] and red.y + 5 < HIGHT - 50:
            red.y += 5
    if keys_pressed[pygame.K_UP] and red.y + 5 > 0:
            red.y -= 5
    if keys_pressed[pygame.K_LEFT] and red.x + 5 >  HIGHT - 40:
            red.x -= 5 

def yellow_handle_movements(keys_pressed,yellow):  
            
    if keys_pressed[pygame.K_a] and yellow.x - 5 > 0:
            yellow.x -= 5
    if keys_pressed[pygame.K_d] and yellow.x + 5 < BORDER.x - 45:
            yellow.x += 5
    if keys_pressed[pygame.K_w] and yellow.y + 5 > 0:
            yellow.y -= 5
    if keys_pressed[pygame.K_x] and yellow.y +5 < HIGHT - 50:
            yellow.y += 5


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PURPLE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(600, 200, SPACESHIP_WIDTH, SPACE_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACE_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2 , 10 , 5)
                    yellow_bullets.append(bullet)   
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2 , 10 , 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                    red_health -= 1
                    

            if event.type == YELLOW_HIT:
                    yellow_health -= 1
               

        winner_text = ""
        if red_health <= 0:
            winner_text = "Player 1 Wins!"
            WIN.blit(BACKROUND_DISPLAY2, (0,0))

        if yellow_health <= 0:
            winner_text = "Player 2 Wins!"
            WIN.blit(BACKROUND_DISPLAY2, (0,0))

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movements(keys_pressed,yellow)
        red_handle_movements(keys_pressed,red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
         
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            
    main()

main()