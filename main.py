# IMPORTING MODULES
import pygame
import random
from time import sleep

pygame.init() # PYGAME SETUP

# CONSTANT VARIABLES
RUN = True # Game loop
FISH_SPRITES = ["cyan_fish_sprite.png", "orange_fish_sprite.png", "red_fish_sprite.png"] # List of fish sprite file names
FISH_SPEED = 0.15 
SCORE_FONT = pygame.font.SysFont("Arial", 45, bold=True) 
BG_COLOUR = (135, 206, 250)  # RGB value for lighter blue
TEXT_COLOUR = (31, 81, 120)  # RGB value for darker blue
TEXT_COLOUR_2 = (55, 180, 230) # RGB value for medium blue

class Screen:
    """Class to create the game screen"""
    def __init__(self, width, height):
        self.width = width # Width of the screen
        self.height = height # Height of the screen
        self.screen = None # Screen object

    def setup(self):
        self.screen = pygame.display.set_mode((self.width, self.height)) # Create the screen
        pygame.display.set_caption("TURTLE ADVENTURE") # Set the title of the screen
        self.screen.fill(BG_COLOUR) # Fill the screen with the background colour (blue)
        pygame.display.flip() # Update the screen

class GameObject(pygame.sprite.Sprite):
    """Class to create game objects (fish and player)"""
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__()
        self.position = position # Position of the object
        self.sprite_sheet = sprite_sheet # Sprite sheet of the object
        self.sprite_rect = sprite_rect # Rectangle of the sprite, bounds of the sprite
        self.scale = scale # Resizing factor
        self.image = pygame.transform.scale(
            self.sprite_sheet.subsurface(self.sprite_rect),
            (int(self.sprite_rect[2] * self.scale), int(self.sprite_rect[3] * self.scale))
        ) # Resizing the sprite
        self.rect = self.image.get_rect(topleft=position) # Rectangle of the sprite

    def draw_sprite(self, screen):
        screen.blit(self.image, self.position) # Puts the sprite on the screen

class Player(GameObject):
    """Class to create the player object"""
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__(position, sprite_sheet, sprite_rect, scale) # Calls the parent class

    def go_to_start(self):
        self.position = [575, 630] # Starting position of the player, x and y coordinates
        self.rect.topleft = self.position # Update the rectangle

    def move_up(self):
        self.position[1] -= 20 # Move player up
        self.rect.y = self.position[1] # Update the y coordinate of the rectangle

    def move_down(self):
        self.position[1] += 20 # Move player down
        self.rect.y = self.position[1] 

        if self.position[1] > 630:
            self.go_to_start() # If player reaches the bottom of the screen, go to the start position

    def is_at_end_position(self):
        return self.rect.y <= 0 # Check if player is at the end position

class Fish(GameObject):
    """Class to create the fish object"""
    def __init__(self, position, sprite_sheet, sprite_rect, scale):
        super().__init__(position, sprite_sheet, sprite_rect, scale) # Calls the parent class

    def update(self):
        self.position[0] -= FISH_SPEED  # Move fish left
        self.rect.x = self.position[0] # Update the x coordinate of the rectangle
        if self.position[0] < -self.rect.width:  # Remove fish if it moves off screen
            self.kill()

def create_fish(fish_group):
    """Function to create fish objects"""
    spawn_chance = random.randint(0, 600) # Random number to determine if fish should spawn
    if spawn_chance == 1: # If random number is 1, create a fish
        fish_sprite_choice = random.choice(FISH_SPRITES) # Randomly choose a coloured fish sprite from the list
        fish_sprite = pygame.image.load(fish_sprite_choice).convert_alpha() # Load the fish sprite
        fish_rect = (0, 0, 16, 16)  # Adjust sprite_rect as needed
        fish = Fish([1200, random.randint(100, 550)], fish_sprite, fish_rect, scale=4)  # Random y position
        fish_group.add(fish) # Add fish to the group

class Scoreboard:
    """Class to create the scoreboard"""
    def __init__(self):
        self.score = 0 # Initial score
        self.font = SCORE_FONT # Font for the score

    def update_score(self):
        text = self.font.render(f"SCORE: {self.score}", True, TEXT_COLOUR) # Render the score
        game_screen.screen.blit(text, (30, 30)) # Display the score on the screen

    def increase_score(self):
        self.score += 1 # Increase the score

    def reset_score(self):
        text = self.font.render("A fish was hit! Resetting...", True, TEXT_COLOUR_2) # Render the text
        game_screen.screen.blit(text, (30, 80)) # Display the text on the screen at a specific position (30, 80)
        pygame.display.flip() # Update the screen
        sleep(2) # Delay for 2 seconds
        self.score = 0 # Reset the score

game_screen = Screen(1200, 700) # Width and height of the screen
game_screen.setup() # Create the screen

player_sprite = pygame.image.load("playerturtle.png").convert_alpha() # Load the sprite sheet for the player
player = Player([575, 630], player_sprite, (0, 0, 16, 16), scale=5)  # Adjust sprite_rect as needed

fish_group = pygame.sprite.Group() # Create a group for fish
scoreboard = Scoreboard() # Create a scoreboard

while RUN: # Main loop
    game_screen.screen.fill(BG_COLOUR)  # Clear the screen each frame
    scoreboard.update_score() # Update the score display
    player.draw_sprite(game_screen.screen) # Draw the player (turtle)
    create_fish(fish_group) # Create fish
    fish_group.update() # Update fish
    fish_group.draw(game_screen.screen) # Draw fish
    pygame.display.flip() # Update the screen

    for event in pygame.event.get(): # Event loop
        if event.type == pygame.QUIT: # If the user closes the window
            RUN = False

        elif event.type == pygame.KEYDOWN: # If a key is pressed

            if event.key == pygame.K_UP: # If the up arrow key is pressed
                player.move_up() # Move the player up

            if event.key == pygame.K_DOWN: # If the down arrow key is pressed
                player.move_down() # Move the player down

        if player.is_at_end_position(): # If the player reaches the end position
            player.go_to_start()
            scoreboard.increase_score()
            FISH_SPEED += 0.05

    collision = pygame.sprite.spritecollide(player, fish_group, False, pygame.sprite.collide_mask) # Check for collision
    if collision: # If there is a collision, player goes to start and game resets
        player.go_to_start()
        scoreboard.reset_score()
        FISH_SPEED = 0.15

pygame.quit() # Quit the game when the loop ends