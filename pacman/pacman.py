import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game settings
CELL_SIZE = 30

# Maze layout (1 = wall, 0 = path, 2 = dot, 3 = power pellet)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Pacman:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = 1 * CELL_SIZE
        self.y = 1 * CELL_SIZE
        self.direction = 'STOP'
        self.next_direction = 'STOP'
        self.speed = 3
        self.score = 0
        self.lives = 3
        self.power_mode = False
        self.power_timer = 0
        
    def move(self):
        # Try to change to next direction
        if self.next_direction != 'STOP':
            if self.can_move(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = 'STOP'
        
        if self.can_move(self.direction):
            if self.direction == 'UP':
                self.y -= self.speed
            elif self.direction == 'DOWN':
                self.y += self.speed
            elif self.direction == 'LEFT':
                self.x -= self.speed
            elif self.direction == 'RIGHT':
                self.x += self.speed
        
        # Handle tunnel
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
        elif self.x > SCREEN_WIDTH - CELL_SIZE:
            self.x = 0
            
    def can_move(self, direction):
        new_x, new_y = self.x, self.y
        if direction == 'UP':
            new_y -= self.speed
        elif direction == 'DOWN':
            new_y += self.speed
        elif direction == 'LEFT':
            new_x -= self.speed
        elif direction == 'RIGHT':
            new_x += self.speed
        else:
            return True
            
        # Check collision with walls
        corners = [
            (new_x, new_y),
            (new_x + CELL_SIZE - 1, new_y),
            (new_x, new_y + CELL_SIZE - 1),
            (new_x + CELL_SIZE - 1, new_y + CELL_SIZE - 1)
        ]
        
        for cx, cy in corners:
            col = cx // CELL_SIZE
            row = cy // CELL_SIZE
            if 0 <= row < len(MAZE) and 0 <= col < len(MAZE[row]):
                if MAZE[row][col] == 1:
                    return False
        return True
        
    def draw(self, screen):
        # Draw Pacman body
        pygame.draw.circle(screen, YELLOW, 
                          (self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2), 
                          CELL_SIZE // 2 - 2)
        
        # Draw mouth
        mouth_angle = 0
        if self.direction == 'RIGHT':
            mouth_angle = 0
        elif self.direction == 'LEFT':
            mouth_angle = 180
        elif self.direction == 'UP':
            mouth_angle = 90
        elif self.direction == 'DOWN':
            mouth_angle = 270
            
        if self.direction != 'STOP':
            start_angle = mouth_angle + 30
            end_angle = mouth_angle - 30
            pygame.draw.polygon(screen, BLACK, [
                (self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2),
                (self.x + CELL_SIZE // 2 + (CELL_SIZE // 2 - 2) * pygame.math.Vector2(1, 0).rotate(start_angle).x,
                 self.y + CELL_SIZE // 2 + (CELL_SIZE // 2 - 2) * pygame.math.Vector2(1, 0).rotate(start_angle).y),
                (self.x + CELL_SIZE // 2 + (CELL_SIZE // 2 - 2) * pygame.math.Vector2(1, 0).rotate(end_angle).x,
                 self.y + CELL_SIZE // 2 + (CELL_SIZE // 2 - 2) * pygame.math.Vector2(1, 0).rotate(end_angle).y)
            ])

class Ghost:
    def __init__(self, color, start_x, start_y):
        self.color = color
        self.start_x = start_x
        self.start_y = start_y
        self.reset()
        
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.speed = 2
        self.scared = False
        
    def move(self, pacman):
        possible_directions = []
        
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            # Don't reverse direction
            if (direction == 'UP' and self.direction == 'DOWN') or \
               (direction == 'DOWN' and self.direction == 'UP') or \
               (direction == 'LEFT' and self.direction == 'RIGHT') or \
               (direction == 'RIGHT' and self.direction == 'LEFT'):
                continue
                
            if self.can_move(direction):
                possible_directions.append(direction)
        
        if possible_directions:
            if self.scared:
                # Run away from pacman
                best_direction = possible_directions[0]
                max_dist = 0
                for direction in possible_directions:
                    temp_x, temp_y = self.x, self.y
                    if direction == 'UP':
                        temp_y -= self.speed
                    elif direction == 'DOWN':
                        temp_y += self.speed
                    elif direction == 'LEFT':
                        temp_x -= self.speed
                    elif direction == 'RIGHT':
                        temp_x += self.speed
                    dist = ((temp_x - pacman.x) ** 2 + (temp_y - pacman.y) ** 2) ** 0.5
                    if dist > max_dist:
                        max_dist = dist
                        best_direction = direction
                self.direction = best_direction
            else:
                # Chase pacman with some randomness
                if random.random() < 0.7:
                    best_direction = possible_directions[0]
                    min_dist = float('inf')
                    for direction in possible_directions:
                        temp_x, temp_y = self.x, self.y
                        if direction == 'UP':
                            temp_y -= self.speed
                        elif direction == 'DOWN':
                            temp_y += self.speed
                        elif direction == 'LEFT':
                            temp_x -= self.speed
                        elif direction == 'RIGHT':
                            temp_x += self.speed
                        dist = ((temp_x - pacman.x) ** 2 + (temp_y - pacman.y) ** 2) ** 0.5
                        if dist < min_dist:
                            min_dist = dist
                            best_direction = direction
                    self.direction = best_direction
                else:
                    self.direction = random.choice(possible_directions)
        
        if self.can_move(self.direction):
            if self.direction == 'UP':
                self.y -= self.speed
            elif self.direction == 'DOWN':
                self.y += self.speed
            elif self.direction == 'LEFT':
                self.x -= self.speed
            elif self.direction == 'RIGHT':
                self.x += self.speed
        
        # Handle tunnel
        if self.x < 0:
            self.x = SCREEN_WIDTH - CELL_SIZE
        elif self.x > SCREEN_WIDTH - CELL_SIZE:
            self.x = 0
            
    def can_move(self, direction):
        new_x, new_y = self.x, self.y
        if direction == 'UP':
            new_y -= self.speed
        elif direction == 'DOWN':
            new_y += self.speed
        elif direction == 'LEFT':
            new_x -= self.speed
        elif direction == 'RIGHT':
            new_x += self.speed
            
        corners = [
            (new_x, new_y),
            (new_x + CELL_SIZE - 1, new_y),
            (new_x, new_y + CELL_SIZE - 1),
            (new_x + CELL_SIZE - 1, new_y + CELL_SIZE - 1)
        ]
        
        for cx, cy in corners:
            col = cx // CELL_SIZE
            row = cy // CELL_SIZE
            if 0 <= row < len(MAZE) and 0 <= col < len(MAZE[row]):
                if MAZE[row][col] == 1:
                    return False
        return True
        
    def draw(self, screen):
        color = BLUE if self.scared else self.color
        # Draw ghost body
        pygame.draw.circle(screen, color, 
                          (self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2 - 2), 
                          CELL_SIZE // 2 - 2)
        pygame.draw.rect(screen, color,
                        (self.x + 2, self.y + CELL_SIZE // 2, CELL_SIZE - 4, CELL_SIZE // 2 - 2))
        
        # Draw eyes
        eye_color = WHITE if not self.scared else WHITE
        pygame.draw.circle(screen, eye_color, 
                          (self.x + CELL_SIZE // 3, self.y + CELL_SIZE // 3), 4)
        pygame.draw.circle(screen, eye_color, 
                          (self.x + 2 * CELL_SIZE // 3, self.y + CELL_SIZE // 3), 4)
        pygame.draw.circle(screen, BLACK, 
                          (self.x + CELL_SIZE // 3, self.y + CELL_SIZE // 3), 2)
        pygame.draw.circle(screen, BLACK, 
                          (self.x + 2 * CELL_SIZE // 3, self.y + CELL_SIZE // 3), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.pacman = Pacman()
        self.ghosts = [
            Ghost(RED, 9 * CELL_SIZE, 9 * CELL_SIZE),
            Ghost(PINK, 8 * CELL_SIZE, 9 * CELL_SIZE),
            Ghost(CYAN, 10 * CELL_SIZE, 9 * CELL_SIZE),
            Ghost(ORANGE, 9 * CELL_SIZE, 10 * CELL_SIZE)
        ]
        
        self.dots = []
        self.power_pellets = []
        self.game_over = False
        self.won = False
        self.setup_maze()
        
    def setup_maze(self):
        self.dots = []
        self.power_pellets = []
        for row in range(len(MAZE)):
            for col in range(len(MAZE[row])):
                if MAZE[row][col] == 2:
                    self.dots.append((col * CELL_SIZE + CELL_SIZE // 2, 
                                    row * CELL_SIZE + CELL_SIZE // 2))
                elif MAZE[row][col] == 3:
                    self.power_pellets.append((col * CELL_SIZE + CELL_SIZE // 2, 
                                             row * CELL_SIZE + CELL_SIZE // 2))
                    
    def reset_positions(self):
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = 'RIGHT'
                elif event.key == pygame.K_r and (self.game_over or self.won):
                    self.restart_game()
                    
    def update(self):
        if self.game_over or self.won:
            return
            
        self.pacman.move()
        
        # Update power mode
        if self.pacman.power_mode:
            self.pacman.power_timer -= 1
            if self.pacman.power_timer <= 0:
                self.pacman.power_mode = False
                for ghost in self.ghosts:
                    ghost.scared = False
        
        # Move ghosts
        for ghost in self.ghosts:
            ghost.move(self.pacman)
            
        # Check dot collision
        pac_center = (self.pacman.x + CELL_SIZE // 2, self.pacman.y + CELL_SIZE // 2)
        for dot in self.dots[:]:
            if ((dot[0] - pac_center[0]) ** 2 + (dot[1] - pac_center[1]) ** 2) ** 0.5 < CELL_SIZE // 2:
                self.dots.remove(dot)
                self.pacman.score += 10
                
        # Check power pellet collision
        for pellet in self.power_pellets[:]:
            if ((pellet[0] - pac_center[0]) ** 2 + (pellet[1] - pac_center[1]) ** 2) ** 0.5 < CELL_SIZE // 2:
                self.power_pellets.remove(pellet)
                self.pacman.score += 50
                self.pacman.power_mode = True
                self.pacman.power_timer = 300  # 5 seconds at 60 FPS
                for ghost in self.ghosts:
                    ghost.scared = True
                    
        # Check ghost collision
        for ghost in self.ghosts:
            if ((ghost.x - self.pacman.x) ** 2 + (ghost.y - self.pacman.y) ** 2) ** 0.5 < CELL_SIZE:
                if ghost.scared:
                    # Eat ghost
                    ghost.reset()
                    self.pacman.score += 200
                else:
                    # Pacman dies
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.game_over = True
                    else:
                        self.reset_positions()
                        
        # Check win condition
        if not self.dots and not self.power_pellets:
            self.won = True
            
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw maze
        for row in range(len(MAZE)):
            for col in range(len(MAZE[row])):
                if MAZE[row][col] == 1:
                    pygame.draw.rect(self.screen, BLUE, 
                                   (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, BLACK, 
                                   (col * CELL_SIZE + 2, row * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        
        # Draw dots
        for dot in self.dots:
            pygame.draw.circle(self.screen, WHITE, dot, 3)
            
        # Draw power pellets
        for pellet in self.power_pellets:
            pygame.draw.circle(self.screen, WHITE, pellet, 8)
            
        # Draw pacman
        self.pacman.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
            
        # Draw HUD
        score_text = self.font.render(f"Score: {self.pacman.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.pacman.lives}", True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))
        
        # Draw game over or win message
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                            SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                          SCREEN_HEIGHT // 2 + 20))
        elif self.won:
            win_text = self.big_font.render("YOU WIN!", True, YELLOW)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 
                                       SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                          SCREEN_HEIGHT // 2 + 20))
            
        pygame.display.flip()
        
    def restart_game(self):
        self.pacman = Pacman()
        self.ghosts = [
            Ghost(RED, 9 * CELL_SIZE, 9 * CELL_SIZE),
            Ghost(PINK, 8 * CELL_SIZE, 9 * CELL_SIZE),
            Ghost(CYAN, 10 * CELL_SIZE, 9 * CELL_SIZE),
            Ghost(ORANGE, 9 * CELL_SIZE, 10 * CELL_SIZE)
        ]
        self.setup_maze()
        self.game_over = False
        self.won = False
        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
