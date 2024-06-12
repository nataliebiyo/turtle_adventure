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
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        self.position = position
        self.sprite_sheet = sprite_sheet
        self.sprite_rect = sprite_rect
        self.scale = scale

    def draw_sprite(self, screen):
        scaled_width = int(self.sprite_rect[2] * self.scale)
        scaled_height = int(self.sprite_rect[3] * self.scale)
        scaled_sprite = pygame.transform.scale(self.sprite_sheet.subsurface(self.sprite_rect), (scaled_width, scaled_height))
        screen.blit(scaled_sprite, self.position)
    
class Player(GameObject):
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__(position, sprite_sheet, sprite_rect, scale)

    def move_up(self):
        self.position[1] -= 20

    def go_to_start(self):
        self.position = [600, 630]


# Create the screen
game_screen = Screen(1200, 700)
game_screen.setup()

# Load the sprite sheet
sprite_sheet = pygame.image.load("playerturtle.png").convert_alpha()
player = Player([600, 630], sprite_sheet, (0, 0, 16, 16), scale=5)  # Adjust sprite_rect as needed


# Main loop
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()

    game_screen.screen.fill(BG_COLOUR)  # Clear the screen each frame
    player.draw_sprite(game_screen.screen)
    pygame.display.flip()

pygame.quit()
