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

while keep_game_running:
    # Checks all pending game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_game_running = False

    # TODO: Make changes to game

    # Draw the background
    screen.blit(
        images["background"],
        (0, 0)
    )

    # Update the display
    pygame.display.update()
