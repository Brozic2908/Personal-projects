import pygame
import sys
import random

# update high score in game
def update_score(score, high_score):
    if (score > high_score):
        high_score = score
    return high_score

# make infinite loop floor movement
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650)) # draw the floor image
    screen.blit(floor, (floor_x_pos + 432, 650)) # draw the floor image

# create a new pipe
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 750))
    return bottom_pipe, top_pipe

# move pipe to left
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# draw pipe into screen
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600: # if the pipe is on the bottom of the screen
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# bird collision
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            die_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        die_sound.play()
        return False
    return True

# bird animation
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, bird_movement * -3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect 

# display score
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)

    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)  

        high_score_surface = game_font.render(f'High Score: {str(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 620))
        screen.blit(high_score_surface, high_score_rect)

pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512) # reduce the delay of sound
pygame.init()
screen = pygame.display.set_mode((432, 768)) # 432x768 is the resolution of the game
 
# Set fps to game resolution
clock = pygame.time.Clock() 

# font display
game_font = pygame.font.Font('PlappyBird/04B_19.TTF', 40)

# variables
gravity = 0.15
bird_movement = 0
game_active = True # game is running
score = 0
high_score = 0

# Load the background image
bg = pygame.image.load('PlappyBird/assets/background-night.png').convert()
bg = pygame.transform.scale(bg, (432, 768)) 

# Load the floor image
floor = pygame.image.load('PlappyBird/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor) 
floor_x_pos = 0

# Create a bird object
bird_up = pygame.transform.scale(pygame.image.load('PlappyBird/assets/yellowbird-upflap.png').convert_alpha(), (58, 41))
bird_mid = pygame.transform.scale(pygame.image.load('PlappyBird/assets/yellowbird-midflap.png').convert_alpha(), (58, 41))
bird_down = pygame.transform.scale(pygame.image.load('PlappyBird/assets/yellowbird-downflap.png').convert_alpha(), (58, 41))
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))

# Create timer for bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

# Create a pipe object 
pipe_surface = pygame.image.load('PlappyBird/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# create timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)
pipe_height = [300, 400, 500]

# end screen
end_screen = pygame.image.load('PlappyBird/assets/message.png').convert_alpha()
end_screen = pygame.transform.scale2x(end_screen)
game_over_rect = end_screen.get_rect(center = (216, 364)) 

# insert sound
flap_sound = pygame.mixer.Sound('PlappyBird/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('PlappyBird/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('PlappyBird/sound/sfx_point.wav')
die_sound = pygame.mixer.Sound('PlappyBird/sound/sfx_die.wav')
swoosh_sound = pygame.mixer.Sound('PlappyBird/sound/sfx_swooshing.wav')
score_sound_countdown = 100

# while loop of game
while True:
    for event in pygame.event.get():    # get event from pygame
        if event.type == pygame.QUIT:   # button quits the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                score = 0
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                bird_movement = -6
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()


    screen.blit(bg, (0, 0)) # draw the background image
    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect) # draw the bird image
        game_active = check_collision(pipe_list) # IF LOSE
        
        # pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        # display score within the game
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if (score_sound_countdown <= 0):
            score_sound_countdown = 100
            score_sound.play()
    else:
        high_score = update_score(score, high_score)
        screen.blit(end_screen, game_over_rect)
        score_display('game_over')

    #  floor
    floor_x_pos -= 1 # move the floor to the left
    draw_floor() # draw the floor image
    if floor_x_pos <= -432: # if the floor image is out of the screen
        floor_x_pos = 0 # reset the floor image position    
    
    pygame.display.update()
    clock.tick(120) # 120 fps