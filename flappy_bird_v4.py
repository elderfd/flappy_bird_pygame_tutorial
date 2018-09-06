import pygame

class Bird:
    """Holds data about the player bird"""
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

# Sets up the PyGame internals
pygame.init()

# Size of the window
screen_width = 288
screen_height = 512

# How high up the screen the ground extends
ground_height = int(screen_height * 0.79)

def has_crashed(bird):
    """Detects if the bird has crashed"""
    return bird.y >= ground_height

# Initialise a game window
screen = pygame.display.set_mode((screen_width, screen_height))

# Sets the window title
pygame.display.set_caption("My Flappy Bird")

keep_game_running = True

images = {}

# Load the background sprite
images["background"] = pygame.image.load("assets/sprites/background-day.png").convert()
images["bird"] = pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
images["ground"] = pygame.image.load('assets/sprites/base.png').convert_alpha()
images["game_over"] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()

# Initial position of the bird
# Bird starts 20% of the way across the screen
# and halfway up the screen
bird = Bird(
    x = int(screen_width * 0.2),
    y = int((screen_width - images["bird"].get_height()) / 2)
)

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

game_over = False

while keep_game_running:
    bird_acceleration = acceleration_due_to_gravity

    # Checks all pending game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_game_running = False
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE) and not game_over:
            bird_velocity = bird_flap_acceleration             

    if not game_over:
        bird_velocity += bird_acceleration

        # Change the y position according to speed
        bird.y += bird_velocity

        game_over = has_crashed(bird)

    # Draw the background
    screen.blit(
        images["background"],
        (0, 0)
    )

    # Draw the ground
    screen.blit(
        images["ground"],
        (0, ground_height)
    )

    screen.blit(
        images["bird"],
        (
            bird.x - images["bird"].get_width() // 2,
            bird.y - images["bird"].get_height() // 2
        )
    )

    if game_over:
        screen.blit(
            images["game_over"],
            (
                (screen_width - images["game_over"].get_width()) // 2,
                (screen_height - images["game_over"].get_height()) // 2,
            )
        )

    # Update the display
    pygame.display.update()
    fps_clock.tick(fps)
