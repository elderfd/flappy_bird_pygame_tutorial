import pygame

# Sets up the PyGame internals
pygame.init()

# Size of the window
screen_width = 288
screen_height = 512

# Initialise a game window
screen = pygame.display.set_mode((screen_width, screen_height))

# Sets the window title
pygame.display.set_caption("My Flappy Bird")

keep_game_running = True

images = {}

# Load the background sprite
images["background"] = pygame.image.load("assets/sprites/background-day.png").convert()
images["bird"] = pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()

# Initial position of the bird
# Bird starts 20% of the way across the screen
# and halfway up the screen
bird_x = int(screen_width * 0.2)
bird_y = int((screen_width - images["bird"].get_height()) / 2)

# How much the bird accelerate directly after flap
# Negative because it accelerates toward the top of the screen
bird_flap_acceleration = -15

# Current bird velocity
bird_velocity = 0

acceleration_due_to_gravity = 1

# For stopping the game from rendering too quickly
fps_clock = pygame.time.Clock()

# Max rate of frames
fps = 30

while keep_game_running:
    bird_acceleration = acceleration_due_to_gravity

    # Checks all pending game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_game_running = False
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
            bird_velocity = bird_flap_acceleration             

    bird_velocity += bird_acceleration

    # Change the y position according to speed
    bird_y += bird_velocity

    # Draw the background
    screen.blit(
        images["background"],
        (0, 0)
    )

    screen.blit(
        images["bird"],
        (bird_x, bird_y)
    )

    # Update the display
    pygame.display.update()
    fps_clock.tick(fps)
