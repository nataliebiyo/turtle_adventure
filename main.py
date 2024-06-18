import pygame

# pygame setup
pygame.init()

# variables
RUN = True
BG_COLOUR = (135, 206, 250)  # RGB value for light blue

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = None

    def setup(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TURTLE ADVENTURE")
        self.screen.fill(BG_COLOUR)
        pygame.display.flip()

class Scoreboard:
    pass

class GameObject:
    def __init__(self, position, sprite_sheet, sprite_rect):
        self.position = position
        self.sprite_sheet = sprite_sheet
        self.sprite_rect = sprite_rect

    def draw_sprite(self, screen):
        screen.blit(self.sprite_sheet, self.position, self.sprite_rect)

class Fish(GameObject):
    def __init__(self, position, sprite_sheet, sprite_rect):
        super().__init__(position, sprite_sheet, sprite_rect)
        self.speed = 1  # Adjust speed as needed
        self.direction = (1, 0)  # Initial direction (right)
        self.all_fish = []
    
    def create_fish(self):
        fish = GameObject(self.position, self.sprite_sheet, self.sprite_rect)
        self.all_fish.append(fish)

    def update_position(self):
        # Update position based on speed and direction
        self.position = (self.position[0] + self.speed * self.direction[0],
                         self.position[1] + self.speed * self.direction[1])


# Create the screen
game_screen = Screen(1200, 700)
game_screen.setup()

# Load the sprite sheet
sprite_sheet = pygame.image.load("ta_sprite.png").convert_alpha()

# Define sprite rectangles for each object on the sprite sheet
# (x, y, width, height)

turtle_rect = (0, 0, 16, 64)
orange_fish_rect = (16, 0, 16, 64)
cyan_fish_rect = (32, 0, 16, 64)
red_fish_rect = (48, 0, 16, 64)


# Create and load the different game objects at different positions
objects = [
    GameObject((100, 100), sprite_sheet, turtle_rect),
    GameObject((200, 200), sprite_sheet, orange_fish_rect),
    GameObject((300, 300), sprite_sheet, cyan_fish_rect),
    GameObject((400, 400), sprite_sheet, red_fish_rect)
]

# Create multiple instances of fishes
fish_instances = [
    Fish((100, 100), sprite_sheet, orange_fish_rect),
    Fish((200, 200), sprite_sheet, cyan_fish_rect),
    Fish((300, 300), sprite_sheet, red_fish_rect),
    # Add more fish instances as needed
]

# Add fish instances to the objects list
objects.extend(fish_instances)

# Main loop
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    game_screen.screen.fill(BG_COLOUR)  # Clear the screen each frame

    for obj in objects:
        obj.draw_sprite(game_screen.screen)

    pygame.display.flip()

pygame.quit()
