import pygame
import sys
import random

# Game constants
FPS = 60                # Frames per second - controls game smoothness
MAX_WIDTH = 800         # Game window width in pixels
MAX_HEIGHT = 500        # Game window height in pixels
GRAVITY = 0.8           # Downward acceleration applied each frame 
JUMP_STRENGTH = 15      # Initial upward velocity when jumping
GROUND_Y = MAX_HEIGHT - 60  # Y-coordinate of the ground (60px from bottom)
INITIAL_ENEMY_SPEED = 5     # Starting speed of enemies moving across screen
SPEED_INCREMENT = 0.001     # How much enemy speed increases per frame (currently unused)
PLAYER_SPEED = 5            # Horizontal movement speed of the player
DOUBLE_JUMP_ALLOWED = True  # Whether the player can jump again while in the air

# Color definitions in RGB format
WHITE = (255, 255, 255)  # Background color
BLUE = (0, 100, 255)     # Player color
RED = (255, 50, 50)      # Enemy color
GREEN = (50, 200, 50)    # Ground color
BLACK = (0, 0, 0)        # Text color and player eye
GRAY = (200, 200, 200)   # Unused but available
YELLOW = (255, 215, 0)   # Coin color

# Initialize pygame and create game window
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()  # Used to control game timing
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))  # Create game window
pygame.display.set_caption("Jumping Game Enhanced")  # Set window title

# Font initialization for displaying text
font = pygame.font.SysFont('Arial', 24)       # Regular text font
large_font = pygame.font.SysFont('Arial', 48) # Larger font for game over/title

class Player:
    """
    The Player class represents the character controlled by the user.
    It handles movement, jumping, and rendering of the player character.
    """
    def __init__(self, x, y):
        """
        Initialize a new player at position (x,y)
        
        Args:
            x (int): Initial x-coordinate
            y (int): Initial y-coordinate
        """
        self.x = x
        self.y = y
        self.width = 40         # Player width in pixels
        self.height = 60        # Player height in pixels
        self.vel_y = 0          # Vertical velocity (negative = upward)
        self.is_jumping = False # Whether player is currently in the air
        self.can_double_jump = DOUBLE_JUMP_ALLOWED  # Whether mid-air jump is available

    def draw(self):
        """
        Draw the player character on the screen
        
        Returns:
            pygame.Rect: The rectangle representing player's position for collision detection
        """
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, BLUE, player_rect)  # Draw blue rectangle for body
        # Draw a simple eye (white circle with black pupil)
        pygame.draw.circle(screen, WHITE, (self.x + 25, self.y + 15), 8)
        pygame.draw.circle(screen, BLACK, (self.x + 25, self.y + 15), 4)
        return player_rect

    def jump(self):
        """
        Make the player jump if conditions allow.
        First jump is from the ground, second jump (double jump) is available mid-air.
        """
        if not self.is_jumping:
            # First jump (from ground)
            self.vel_y = -JUMP_STRENGTH  # Set upward velocity
            self.is_jumping = True       # Mark player as in the air
        elif self.can_double_jump:
            # Double jump (while already in the air)
            self.vel_y = -JUMP_STRENGTH  # Provide second upward boost
            self.can_double_jump = False # Prevent additional jumps

    def update(self):
        """
        Update player's position based on physics (gravity)
        and handle collision with the ground.
        """
        # Apply gravity to vertical velocity
        self.vel_y += GRAVITY
        # Update vertical position based on velocity
        self.y += self.vel_y

        # Check if player has reached or passed through the ground
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height  # Place player exactly on ground
            self.vel_y = 0                   # Stop vertical movement
            self.is_jumping = False          # Reset jumping state
            self.can_double_jump = DOUBLE_JUMP_ALLOWED  # Reset double jump ability

class Coin:
    """
    The Coin class represents collectible items that give points to the player.
    """
    def __init__(self, x, y):
        """
        Initialize a new coin at position (x,y)
        
        Args:
            x (int): X-coordinate of the coin
            y (int): Y-coordinate of the coin
        """
        self.x = x
        self.y = y
        self.radius = 10         # Size of the coin
        self.collected = False   # Whether this coin has been collected
    
    def draw(self):
        """Draw the coin on the screen if it hasn't been collected yet"""
        if not self.collected:
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)
    
    def collect(self, player_rect):
        """
        Check if player has collected this coin
        
        Args:
            player_rect (pygame.Rect): Rectangle representing player's position
            
        Returns:
            bool: True if coin was just collected, False otherwise
        """
        # Create a rectangle around the coin for collision detection
        coin_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                self.radius * 2, self.radius * 2)
        # Check for collision between player and coin
        if player_rect.colliderect(coin_rect):
            self.collected = True
            return True
        return False

class Enemy:
    """
    The Enemy class represents obstacles that the player must avoid.
    Enemies move from right to left across the screen.
    """
    def __init__(self, x, y, width=20, height=40):
        """
        Initialize a new enemy at position (x,y) with specified dimensions
        
        Args:
            x (int): X-coordinate of the enemy
            y (int): Y-coordinate of the enemy
            width (int): Width of the enemy
            height (int): Height of the enemy
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        """
        Draw the enemy on the screen
        
        Returns:
            pygame.Rect: Rectangle representing enemy's position for collision detection
        """
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, enemy_rect)
        return enemy_rect

    def move(self, speed):
        """
        Move the enemy from right to left and reset position when off-screen
        
        Args:
            speed (float): Speed at which the enemy moves
        """
        # Move enemy to the left
        self.x -= speed
        # If enemy has moved completely off the left edge of the screen
        if self.x <= -self.width:
            # Randomize enemy dimensions for variety
            self.width = random.randint(20, 50)
            self.height = random.randint(30, 60)
            # Position at the bottom right of the screen
            self.y = GROUND_Y - self.height
            self.x = MAX_WIDTH

class Game:
    """
    The Game class manages the overall game state, including player, enemies,
    coins, score, and game loop.
    """
    def __init__(self):
        """Initialize a new game with starting objects and state"""
        # Create player at starting position
        self.player = Player(80, GROUND_Y - 60)
        # Create initial enemy at right edge of screen
        self.enemies = [Enemy(MAX_WIDTH, GROUND_Y - 40)]
        # Create initial coin at random position
        self.coins = [Coin(random.randint(200, 700), GROUND_Y - 30)]
        self.score = 0              # Player's score
        self.high_score = 0         # Highest score achieved (unused currently)
        self.speed = INITIAL_ENEMY_SPEED  # Current enemy movement speed
        self.game_over = False      # Whether the game has ended
    
    def handle_events(self):
        """Process user input for player movement and game control"""
        # Get current state of all keyboard keys
        keys = pygame.key.get_pressed()
        # Handle continuous left/right movement
        if keys[pygame.K_LEFT]:
            # Move left but don't go off screen
            self.player.x = max(0, self.player.x - PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            # Move right but don't go off screen
            self.player.x = min(MAX_WIDTH - self.player.width, self.player.x + PLAYER_SPEED)
        
        # Process pygame events (key presses, quit button, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit game if window is closed
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Jump when spacebar is pressed
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):
        """Update game state for all game objects"""
        # Update player physics
        self.player.update()
        # Move all enemies
        for enemy in self.enemies:
            enemy.move(self.speed)
        # Check for coin collections
        for coin in self.coins:
            if coin.collect(pygame.Rect(self.player.x, self.player.y, 
                                      self.player.width, self.player.height)):
                # Add points when coin is collected
                self.score += 5
                # Remove collected coin
                self.coins.remove(coin)
                # Add a new coin at random position
                self.coins.append(Coin(random.randint(200, 700), GROUND_Y - 30))
        
    def check_collisions(self):
        """Check for collisions between player and enemies"""
        # Create rectangle representing player's position
        player_rect = pygame.Rect(self.player.x, self.player.y, 
                                self.player.width, self.player.height)
        # Check collision with each enemy
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                # Set game_over flag if player hits an enemy
                self.game_over = True

    def draw(self):
        """Draw all game elements on the screen"""
        # Fill background with white
        screen.fill(WHITE)
        # Draw green ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_Y, MAX_WIDTH, MAX_HEIGHT - GROUND_Y))
        # Draw player
        self.player.draw()
        # Draw all enemies
        for enemy in self.enemies:
            enemy.draw()
        # Draw all coins
        for coin in self.coins:
            coin.draw()
        # Display current score
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        # Update the display to show all drawn elements
        pygame.display.update()

def main():
    """Main function to run the game"""
    # Create new game instance
    game = Game()
    # Main game loop
    while True:
        # Process player input
        game.handle_events()
        # Only update gameplay if game is not over
        if not game.game_over:
            game.update()
            game.check_collisions()
        # Always draw the current state
        game.draw()
        # Maintain consistent frame rate
        clock.tick(FPS)

# Run the game when this script is executed directly
if __name__ == '__main__':
    main()