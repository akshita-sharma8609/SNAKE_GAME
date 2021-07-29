import pygame
import os
import random

pygame.init()
pygame.mixer.init()

screen_width=600
screen_height=500

gamewindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("SNAKE GAME")
pygame.display.update()

#colors
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
grey=(47,79,79)

bg_welcome_img=pygame.image.load("welcome.png")
bg_welcome_img=pygame.transform.scale(bg_welcome_img,(screen_width,screen_height)).convert_alpha()
bg_gameover_img=pygame.image.load("gameover.webp")
bg_gameover_img=pygame.transform.scale(bg_gameover_img,(screen_width,screen_height)).convert_alpha()

clock= pygame.time.Clock()
font=pygame.font.SysFont(None,30)


def text_screen(text,color,x,y):
    """This function displays the score on the screen"""
    screen_text= font.render(text,True,color)
    gamewindow.blit(screen_text,[x,y])


def plot_snake(gamewindow,color,snake_list,snake_size):
    """This function plots the snake"""
    for x,y in snake_list:
        pygame.draw.rect(gamewindow,color,[x,y,snake_size,snake_size])


def home_screen():
    exit_game=False
    while not exit_game:
        gamewindow.blit(bg_welcome_img,(0,0))
        text_screen("PRESS ENTER TO PLAY",red,230,270)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    pygame.mixer.music.load("bg_music.mp3")
                    pygame.mixer.music.play(-1)
                    Game_Loop()
        pygame.display.update()
        clock.tick(60)


#Game Loop
def Game_Loop():
    exit_game=False
    game_over=False
    snake_x= 45
    snake_y= 55
    snake_size= 20
    fps=60
    init_velocity= 3
    velocity_x= 0
    velocity_y= 0
    food_x= random.randint(0,screen_width-100)
    food_y= random.randint(0,screen_height-100)
    score=0

    if (not os.path.exists("highscore.txt")):
        with open ("highscore.txt",'w') as f:
            f.write("0")
    with open("highscore.txt","r")as f:
        highscore=f.read()

    initial_highscore=int(highscore)
    snake_list=[]
    snake_length=1

    while not exit_game:

        if game_over:
            with open("highscore.txt","w")as f:
                f.write(str(highscore))

            if int(score)>0 and int(score)>initial_highscore :
                gamewindow.blit(bg_gameover_img,(0,0))
                text_screen("GAME OVER",red,220,180)
                text_screen("CONGRATULATIONS!",white,180,220)
                text_screen(f"NEW HIGH SCORE: {score}",white,180,250)
            else:
                gamewindow.fill(black)
                text_screen("GAME OVER",white,220,180)
                text_screen(f"YOUR SCORE: {score}",white,200,240)
            text_screen("Press Enter to Continue",red,170,300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game=True
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        pygame.mixer.music.load("bg_music.mp3")
                        pygame.mixer.music.play(-1)
                        Game_Loop()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game=True

                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y=0
                    if event.key==pygame.K_RIGHT:
                        velocity_x= init_velocity
                        velocity_y=0
                    if event.key==pygame.K_UP:
                        velocity_x=0
                        velocity_y= -init_velocity
                    if event.key==pygame.K_DOWN:
                        velocity_x=0
                        velocity_y= init_velocity

            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y

            if(abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10):
                score += 10
                food_x= random.randint(0,screen_width/2)
                food_y= random.randint(0,screen_height/2)
                snake_length+=5

                if score>int(highscore):
                    highscore=score


            gamewindow.fill(grey)
            text_screen("SCORE: "+str(score) + "                                           HIGH SCORE: " + str(highscore),white,10,10)

            pygame.draw.rect(gamewindow,red,[food_x,food_y,snake_size,snake_size])
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if(len(snake_list)>snake_length):
                del snake_list[0]

            if head in snake_list[:-1]:
                pygame.mixer.music.load("GameOver.mp3")
                pygame.mixer.music.play()
                game_over = True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load("GameOver.mp3")
                pygame.mixer.music.play()
                game_over = True


            plot_snake(gamewindow,black,snake_list,snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()
home_screen()