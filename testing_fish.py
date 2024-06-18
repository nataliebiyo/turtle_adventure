import pygame
import random
from time import sleep

# pygame setup
pygame.init()
pygame.font.init()

# variables
RUN = True
FISH_SPRITES = ["cyan_fish_sprite.png", "orange_fish_sprite.png", "red_fish_sprite.png"]
FISH_SPEED = 0.3
SCORE_FONT = pygame.font.SysFont("Arial", 45, bold=True)
BG_COLOUR = (135, 206, 250)  # RGB value for lighter blue
TEXT_COLOUR = (31, 81, 120)  # RGB value for darker blue
TEXT_COLOUR_2 = (55, 180, 230) # RGB value for medium blue

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

    def go_to_start(self):
        self.position = [575, 630]
        self.rect.topleft = self.position

    def move_up(self):
        self.position[1] -= 20
        self.rect.y = self.position[1]

    def move_down(self):
        self.position[1] += 20
        self.rect.y = self.position[1]

        if self.position[1] > 630:
            self.go_to_start()

    def is_at_end_position(self):
        return self.rect.y <= 100

class Fish(GameObject):
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__(position, sprite_sheet, sprite_rect, scale)

    def update(self):
        self.position[0] -= 0.15  # Move fish left
        self.rect.x = self.position[0]
        if self.position[0] < -self.rect.width:  # Remove fish if it moves off screen
            self.kill()

def create_fish(fish_group):
    spawn_chance = random.randint(0, 600)
    if spawn_chance == 1:
        fish_sprite_choice = random.choice(FISH_SPRITES)
        fish_sprite = pygame.image.load(fish_sprite_choice).convert_alpha()
        fish_rect = (0, 0, 16, 16)  # Adjust sprite_rect as needed
        fish = Fish([1200, random.randint(100, 550)], fish_sprite, fish_rect, scale=4)  # Random y position
        fish_group.add(fish)

class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = SCORE_FONT
        self.position = (30, 30)

    def update_score(self):
        text = self.font.render(f"SCORE: {self.score}", True, TEXT_COLOUR)
        game_screen.screen.blit(text, self.position)

    def increase_score(self):
        self.score += 1

    def reset_score(self):
        text = self.font.render(f"A fish was hit! Resetting...", True, TEXT_COLOUR_2)
        game_screen.screen.blit(text, (500, 30))
        pygame.display.flip()
        sleep(2)
        self.score = 0

# Create the screen
game_screen = Screen(1200, 700)
game_screen.setup()

# Load the sprite sheet for the player

player_sprite = pygame.image.load("playerturtle.png").convert_alpha()
player = Player([575, 630], player_sprite, (0, 0, 16, 16), scale=5)  # Adjust sprite_rect as needed

# Create a group for fish
fish_group = pygame.sprite.Group()

scoreboard = Scoreboard()

# Main loop
while RUN:

    game_screen.screen.fill(BG_COLOUR)  # Clear the screen each frame
    scoreboard.update_score()


    player.draw_sprite(game_screen.screen)

    create_fish(fish_group)
    fish_group.update()
    fish_group.draw(game_screen.screen)

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            RUN = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                player.move_up()

            if event.key == pygame.K_DOWN:
                player.move_down()

        if player.is_at_end_position():
            player.go_to_start()
            scoreboard.increase_score()

    collision = pygame.sprite.spritecollide(player, fish_group, False, pygame.sprite.collide_mask)
    if collision:
        player.go_to_start()
        scoreboard.reset_score()

pygame.quit()