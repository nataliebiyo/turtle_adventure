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
    def __init__(self, position, sprite_path, width, height):
        self.position = position
        self.sprite_path = sprite_path
        self.sprite_width = width
        self.sprite_height = height
        self.sprite_sheet = None

    def load_sprite(self):
        self.sprite_sheet = pygame.image.load(self.sprite_path).convert_alpha()

    def draw_sprite(self, screen):
        screen.blit(self.sprite_sheet, self.position)

    def get_image(self):
        image = pygame.Surface((self.sprite_width, self.sprite_height)).convert_alpha()
        return image

class Fish(GameObject):
    pass

class Player(GameObject):
    pass

# Create the screen
game_screen = Screen(1200, 700)
game_screen.setup()

# Create and load the test object
test_object = GameObject((0, 0), "ta_sprite.png", 100, 100)
test_object.load_sprite()  # Load the sprite after setting up the screen

# Main loop
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    game_screen.screen.fill(BG_COLOUR)  # Clear the screen each frame
    test_object.draw_sprite(game_screen.screen)

    pygame.display.flip()

pygame.quit()
