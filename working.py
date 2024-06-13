import pygame
import random
import os

# pygame setup
pygame.init()

# variables
RUN = True
BG_COLOUR = (135, 206, 250)  # RGB value for light blue
FISH_SPRITES = ["cyan_fish_sprite.png", "orange_fish_sprite.png", "red_fish_sprite.png"]

# Debug: Print current working directory
print("Current working directory:", os.getcwd())

# Debug: Check if sprite files exist
for sprite in ["playerturtle.png"] + FISH_SPRITES:
    if not os.path.exists(sprite):
        print(f"Sprite file not found: {sprite}")
    else:
        print(f"Sprite file found: {sprite}")

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

class GameObject(pygame.sprite.Sprite):
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__()
        self.position = position
        self.sprite_sheet = sprite_sheet
        self.sprite_rect = sprite_rect
        self.scale = scale
        self.image = pygame.transform.scale(
            self.sprite_sheet.subsurface(self.sprite_rect),
            (int(self.sprite_rect[2] * self.scale), int(self.sprite_rect[3] * self.scale))
        )
        self.rect = self.image.get_rect(topleft=position)

    def draw_sprite(self, screen):
        screen.blit(self.image, self.position)

class Player(GameObject):
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__(position, sprite_sheet, sprite_rect, scale)

    def move_up(self):
        self.position[1] -= 20
        self.rect.y = self.position[1]

    def go_to_start(self):
        self.position = [600, 630]
        self.rect.topleft = self.position

class Fish(GameObject):
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__(position, sprite_sheet, sprite_rect, scale)

    def update(self):
        self.position[0] -= 5  # Move fish left
        self.rect.x = self.position[0]
        if self.position[0] < -self.rect.width:  # Remove fish if it moves off screen
            self.kill()

def create_fish(fish_group):
    fish_sprite_choice = random.choice(FISH_SPRITES)
    try:
        fish_sprite = pygame.image.load(fish_sprite_choice).convert_alpha()
        fish_rect = (0, 0, 16, 16)  # Adjust sprite_rect as needed
        fish = Fish([1200, random.randint(0, 684)], fish_sprite, fish_rect, scale=5)  # Random y position
        fish_group.add(fish)
        print(f"Created fish at position {fish.position} with sprite {fish_sprite_choice}")  # Debugging
    except pygame.error as e:
        print(f"Error loading fish sprite: {fish_sprite_choice}, {e}")

# Create the screen
game_screen = Screen(1200, 700)
game_screen.setup()

# Load the sprite sheet for the player
try:
    player_sprite = pygame.image.load("playerturtle.png").convert_alpha()
    player = Player([600, 630], player_sprite, (0, 0, 16, 16), scale=5)  # Adjust sprite_rect as needed
except pygame.error as e:
    print(f"Error loading player sprite: {e}")

# Create a group for fish
fish_group = pygame.sprite.Group()

# Main loop
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
                create_fish(fish_group)

    game_screen.screen.fill(BG_COLOUR)  # Clear the screen each frame
    player.draw_sprite(game_screen.screen)
    fish_group.update()
    fish_group.draw(game_screen.screen)

    pygame.display.flip()

pygame.quit()
