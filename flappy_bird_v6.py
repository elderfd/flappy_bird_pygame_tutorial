import pygame
import random
from enum import Enum


class Bird:
    """Holds data about the player bird"""
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Pipe:
    """Holds info about an obstacle pipe"""
    class Direction(Enum):
        UP = 0
        DOWN = 1

    def __init__(self, x = 0, y = 0, direction = Direction.UP):
        self.x = x
        self.y = y
        self.direction = direction

    @staticmethod
    def generate_random_pair(initial_x):
        gap_size = 125

        start_of_gap = random.randrange(
            int(screen_height * 0.2),
            int(screen_height * 0.8 - gap_size)
        )

        pipe_height = images["pipe_down"].get_height()

        # Return a pair of pipes to match the generated gap
        return (
            Pipe(initial_x, start_of_gap + gap_size, Pipe.Direction.UP),
            Pipe(initial_x, start_of_gap - pipe_height, Pipe.Direction.DOWN)
        )

class Collider:
    def __init__(self, image):
        self.rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        self.mask = [
            [bool(image.get_at((j, i))[3]) for j in range(image.get_width())]
            for i in range(image.get_height())
        ] 

    def set_coords(self, x, y):
        """Moves the collider to the coordinates"""
        self.rect.x = x
        self.rect.y = y

    def collides_with(self, other):
        """Checks if two colliders collide"""
        # Get the intersection of the two rects
        intersect_rect = self.rect.clip(other.rect)

        # If no intersection then definitely do not collide
        if intersect_rect.width == 0 or intersect_rect.height == 0:
            return False

        # Get offsets for two rects
        x1, y1 = intersect_rect.x - self.rect.x, intersect_rect.y - self.rect.y
        x2, y2 = intersect_rect.x - other.rect.x, intersect_rect.y - other.rect.y

        # Check if masks overlap
        for i in range(intersect_rect.width):
            for j in range(intersect_rect.height):
                if self.mask[j + y1][i + x1] and other.mask[j + y2][i + x2]:
                    return True
        
        return False

# Sets up the PyGame internals
pygame.init()

# Size of the window
screen_width = 288
screen_height = 512

# How high up the screen the ground extends
ground_height = int(screen_height * 0.79)

def has_crashed(bird, pipes):
    """Detects if the bird has crashed"""
    # Check if bird has hit the ground    
    if bird.y >= ground_height:
        return True

    # Check collision between pipes and bird
    bird_collider = colliders["bird"]

    # Use offset to account for the fact that the bird
    # x and y are at the centre of the image
    bird_collider.set_coords(
        bird.x - images["bird"].get_width() // 2,
        bird.y - images["bird"].get_height() // 2
    )

    for pipe in pipes:
        pipe_collider = colliders["pipe_up"] if pipe.direction == Pipe.Direction.UP else colliders["pipe_down"]

        pipe_collider.set_coords(pipe.x, pipe.y)
        
        if pipe_collider.collides_with(bird_collider):
            return True

    return False

# Initialise a game window
screen = pygame.display.set_mode((screen_width, screen_height))

# Sets the window title
pygame.display.set_caption("My Flappy Bird")

keep_game_running = True

images = {}

# Load the background sprite
images["background"] = pygame.image.load("assets/sprites/background-day.png").convert()
images["bird"] = pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
images["ground"] = pygame.image.load("assets/sprites/base.png").convert_alpha()
images["game_over"] = pygame.image.load("assets/sprites/gameover.png").convert_alpha()

# Load in pretty digits
for digit in range(10):
    images[digit] = pygame.image.load(
        "assets/sprites/{}.png".format(digit)
    ).convert_alpha()

# Load pipe image twice, the second time invert it
images["pipe_up"] = pygame.image.load("assets/sprites/pipe-green.png").convert_alpha()
images["pipe_down"] = pygame.transform.rotate(
    pygame.image.load("assets/sprites/pipe-green.png").convert_alpha(),
    180
)

# Colliders for obstacles and player
colliders = {
    "bird": Collider(images["bird"]),
    "pipe_up": Collider(images["pipe_up"]),
    "pipe_down": Collider(images["pipe_down"])
}

# Initial position of the bird
# Bird starts 20% of the way across the screen
# and halfway up the screen
bird = Bird(
    x = int(screen_width * 0.2),
    y = int((screen_width - images["bird"].get_height()) / 2)
)

# How fast the bird is flying directly after flap
# Negative because it accelerates toward the top of the screen
bird_flap_velocity = -15

# Current bird velocity
bird_velocity = 0

acceleration_due_to_gravity = 1

# How quickly the pipes move across the screen
pipe_velocity = -5

# For stopping the game from rendering too quickly
fps_clock = pygame.time.Clock()

# Max rate of frames
fps = 30

game_over = False

# Stores info about all currently existing pipes
pipes = []

# Generate some initial pipes just off the screen
pipes += list(Pipe.generate_random_pair(screen_width + 10))

score = 0

while keep_game_running:
    bird_acceleration = acceleration_due_to_gravity

    # Checks all pending game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_game_running = False
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
            if game_over:
                pipes = list(Pipe.generate_random_pair(screen_width + 10))
                bird = Bird(
                    x = int(screen_width * 0.2),
                    y = int((screen_width - images["bird"].get_height()) / 2)
                )
                bird_velocity = 0
                score = 0

                game_over = False
            else:
                bird_velocity = bird_flap_velocity             

    if not game_over:
        bird_velocity += bird_acceleration

        # Change the y position according to speed
        bird.y += bird_velocity

        pipes_to_remove = []

        for pipe_index, pipe in enumerate(pipes):
            pipe.x += pipe_velocity

            # If pipes are almost off the screen generate some more
            # Only check the up pipes to avoid duplication
            if pipe.x < 100 and pipe.x > 95 and pipe.direction == Pipe.Direction.UP:
                pipes += list(Pipe.generate_random_pair(screen_width + 10))

            pipe_width = images["pipe_up"].get_width()

            # If the pipe is off the screen, mark it for removal
            if pipe.x < -pipe_width:
                pipes_to_remove.append(pipe_index)

        # Remove excess pipes
        for pipe_index in reversed(pipes_to_remove):
            pipes = pipes[:pipe_index] + pipes[pipe_index:]

        game_over = has_crashed(bird, pipes)

        if not game_over:
            # Check for scoring
            for pipe in pipes:
                # Only check one direction
                if pipe.direction == Pipe.Direction.UP and pipe.x < 25 and pipe.x > 20:
                    score += 1

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

    for pipe in pipes:
        screen.blit(
            images["pipe_up"] if pipe.direction == Pipe.Direction.UP else images["pipe_down"],
            (pipe.x, pipe.y)
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

    # Draw the score
    score_string = str(score)

    # Where to draw the digits
    digit_y = screen_height * 0.1

    # Get total width of digits
    total_digit_width = sum(images[int(digit)].get_width() for digit in score_string)

    # Start drawing digits here
    digit_x = (screen_width - total_digit_width) // 2

    # Draw all digits
    for digit in score_string:
        screen.blit(
            images[int(digit)],
            (digit_x, digit_y)
        )

        # Position next digit
        digit_x += images[int(digit)].get_width()

    # Update the display
    pygame.display.update()
    fps_clock.tick(fps)
