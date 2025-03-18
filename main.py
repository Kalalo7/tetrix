import pygame
import random
from piece import Piece

class TetrixGame:
    def __init__(self):
        pygame.init()
        self.width = 400
        self.height = 700
        self.grid_size = 30
        self.grid_width = 10
        self.grid_height = 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetrix - Custom Tetris")
        
        # Calculate grid offset to center it
        self.grid_offset_x = (self.width - (self.grid_width * self.grid_size)) // 2
        self.grid_offset_y = 50
        
        # Initialize font
        self.font = pygame.font.Font(None, 36)
        
        # Game grid (0 = empty, other numbers = piece colors)
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Game states
        self.current_piece = None
        self.next_piece = None  # Add this line
        self.game_over = False
        self.score = 0

        # Add movement timing variables
        self.move_delay = 0.15  # Initial delay before continuous movement
        self.move_interval = 0.05  # Time between continuous movements
        self.left_time = 0
        self.right_time = 0
        self.down_time = 0
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False

    def draw_next_piece(self):
        if not self.next_piece:
            return
            
        # Draw "Next Piece" text
        next_text = self.font.render("Next:", True, (255, 255, 255))
        self.screen.blit(next_text, (self.width - 120, 50))
        
        # Draw the next piece preview
        preview_offset_x = self.width - 100
        preview_offset_y = 100
        
        for row in range(len(self.next_piece.shape)):
            for col in range(len(self.next_piece.shape[row])):
                if self.next_piece.shape[row][col]:
                    pygame.draw.rect(
                        self.screen,
                        self.next_piece.color,
                        (preview_offset_x + col * self.grid_size,
                         preview_offset_y + row * self.grid_size,
                         self.grid_size - 1,
                         self.grid_size - 1)
                    )

    def check_collision(self, x_offset=0, y_offset=0):
        if not self.current_piece:
            return False
        
        for row in range(len(self.current_piece.shape)):
            for col in range(len(self.current_piece.shape[row])):
                if self.current_piece.shape[row][col]:
                    new_x = self.current_piece.x + col + x_offset
                    new_y = self.current_piece.y + row + y_offset
                    
                    # Check boundaries
                    if (new_x < 0 or new_x >= self.grid_width or 
                        new_y >= self.grid_height or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False

    def lock_piece(self):
        if not self.current_piece:
            return
        for row in range(len(self.current_piece.shape)):
            for col in range(len(self.current_piece.shape[row])):
                if self.current_piece.shape[row][col]:
                    y = self.current_piece.y + row
                    x = self.current_piece.x + col
                    if y >= 0:
                        self.grid[int(y)][int(x)] = self.current_piece.color
        self.current_piece = None
        self.clear_lines()

    def clear_lines(self):
        lines_cleared = 0
        y = self.grid_height - 1
        while y >= 0:
            if all(cell != 0 for cell in self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(self.grid_width)])
            else:
                y -= 1
        self.score += lines_cleared * 100

    def draw_grid(self):
        # Draw background grid
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                pygame.draw.rect(
                    self.screen,
                    (50, 50, 50),
                    (self.grid_offset_x + x * self.grid_size,
                     self.grid_offset_y + y * self.grid_size,
                     self.grid_size - 1,
                     self.grid_size - 1)
                )
                # Draw locked pieces
                if self.grid[y][x] != 0:
                    pygame.draw.rect(
                        self.screen,
                        self.grid[y][x],
                        (self.grid_offset_x + x * self.grid_size,
                         self.grid_offset_y + y * self.grid_size,
                         self.grid_size - 1,
                         self.grid_size - 1)
                    )

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        # Game Over text
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 40))
        self.screen.blit(game_over_text, text_rect)
        
        # Score text
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(score_text, score_rect)

        # Restart button
        restart_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 40, 200, 40)
        pygame.draw.rect(self.screen, (0, 255, 0), restart_button)
        restart_text = self.font.render("Play Again", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)

        # Quit button
        quit_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 90, 200, 40)
        pygame.draw.rect(self.screen, (255, 0, 0), quit_button)
        quit_text = self.font.render("Quit", True, (0, 0, 0))
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        self.screen.blit(quit_text, quit_text_rect)

        return restart_button, quit_button

    def hard_drop(self):
        if not self.current_piece:
            return
        while not self.check_collision(y_offset=1):
            self.current_piece.move_down()
        self.lock_piece()

    def run(self):
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.5

        shapes = ['L_Shape', 'J_Shape', 'S_Shape', 'Z_Shape', 'O_Shape', 'I_Shape',
                 'Cross', 'Diamond', 'U_Shape', 'Plus', 'H_Shape', 'Line_3']
        
        # Initialize next piece at start
        self.next_piece = Piece(random.choice(shapes))
        
        while True:
            delta_time = clock.tick(60) / 1000.0
            fall_time += delta_time
            
            # Update movement timers
            if self.moving_left:
                self.left_time += delta_time
            if self.moving_right:
                self.right_time += delta_time
            if self.moving_down:
                self.down_time += delta_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                # Handle game over state
                if self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        restart_button, quit_button = self.draw_game_over()
                        
                        if restart_button.collidepoint(mouse_pos):
                            self.__init__()
                            self.next_piece = Piece(random.choice(shapes))
                            continue
                        elif quit_button.collidepoint(mouse_pos):
                            pygame.quit()
                            return
                    continue  # Skip other game logic when game over
                
                # Handle gameplay controls
                if event.type == pygame.KEYDOWN and self.current_piece:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                        if not self.check_collision(x_offset=-1):
                            self.current_piece.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                        if not self.check_collision(x_offset=1):
                            self.current_piece.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.moving_down = True
                        if not self.check_collision(y_offset=1):
                            self.current_piece.move_down()
                    elif event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if self.check_collision():
                            for _ in range(3):
                                self.current_piece.rotate()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = False
                        self.left_time = 0
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = False
                        self.right_time = 0
                    elif event.key == pygame.K_DOWN:
                        self.moving_down = False
                        self.down_time = 0

            # Handle continuous movement
            if self.current_piece:
                if self.moving_left and self.left_time >= self.move_delay:
                    if not self.check_collision(x_offset=-1):
                        self.current_piece.move_left()
                    self.left_time = self.move_delay - self.move_interval
                
                if self.moving_right and self.right_time >= self.move_delay:
                    if not self.check_collision(x_offset=1):
                        self.current_piece.move_right()
                    self.right_time = self.move_delay - self.move_interval
                
                if self.moving_down and self.down_time >= self.move_delay:
                    if not self.check_collision(y_offset=1):
                        self.current_piece.move_down()
                    self.down_time = self.move_delay - self.move_interval

            # Handle piece falling
            if not self.game_over:
                if fall_time >= fall_speed:
                    if self.current_piece:
                        if not self.check_collision(y_offset=1):
                            self.current_piece.move_down()
                        else:
                            self.lock_piece()
                    else:
                        self.current_piece = self.next_piece
                        self.current_piece.x = self.grid_width // 2 - len(self.current_piece.shape[0]) // 2
                        self.next_piece = Piece(random.choice(shapes))
                        if self.check_collision():
                            self.game_over = True
                    fall_time = 0
            
            # Draw game state
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_score()
            self.draw_next_piece()
            
            if self.current_piece and not self.game_over:
                for row in range(len(self.current_piece.shape)):
                    for col in range(len(self.current_piece.shape[row])):
                        if self.current_piece.shape[row][col]:
                            pygame.draw.rect(
                                self.screen,
                                self.current_piece.color,
                                (self.grid_offset_x + (self.current_piece.x + col) * self.grid_size,
                                 self.grid_offset_y + (self.current_piece.y + row) * self.grid_size,
                                 self.grid_size - 1,
                                 self.grid_size - 1)
                            )
            
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.flip()

if __name__ == "__main__":
    game = TetrixGame()
    game.run()