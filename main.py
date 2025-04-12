import pygame
import math
import random
import time
from pygame import mixer

class PongGame:
    def __init__(self):
        pygame.init()
        
        # Game constants
        self.WIDTH, self.HEIGHT = 800, 700
        self.bar_width = 20
        self.bar_height = 100
        self.ball_radius = 10
        self.bar_speed = 4
        self.ball_speed = (((math.sqrt((self.HEIGHT ** 2) + (self.WIDTH ** 2))) / 
                          (self.HEIGHT - self.bar_height)) * self.bar_speed) * 1.5
        self.upper_boundary = 100
        self.lower_boundary = self.HEIGHT - 5
        
        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.purple = (128, 0, 128)
        
        # Game state
        self.score1 = 0
        self.score2 = 0
        self.ball_state = "rest"
        self.game_paused = False
        self.difficulty = "medium"  # easy, medium, hard
        
        # Setup display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Enhanced Pong Game")
        
        # Setup sound
        try:
            self.collide_sound = mixer.Sound("wall_collision.wav")
            self.beep_sound = mixer.Sound("beep.wav")
        except:
            # Create silent sounds if files not found
            self.collide_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytes(bytearray([0] * 44))))
            self.beep_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytes(bytearray([0] * 44))))
            print("Sound files not found. Using silent sounds.")
        
        # Setup fonts
        self.font = pygame.font.Font(None, 32)
        self.font2 = pygame.font.Font(None, 16)
        
        # Setup game objects
        self.setup_game_objects()
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
        # Trail effect for ball
        self.ball_trail = []
        self.max_trail_length = 10
        
    def setup_game_objects(self):
        # Score display area
        self.result = pygame.Surface((self.WIDTH, self.upper_boundary + 5))
        
        # Player paddles
        self.player1 = pygame.Surface((self.bar_width, self.bar_height))
        self.player2 = pygame.Surface((self.bar_width, self.bar_height))
        self.player1.fill(self.red)
        self.player2.fill(self.purple)
        self.rect1 = self.player1.get_rect()
        self.rect2 = self.player2.get_rect()
        self.rect1.topleft = (5, (self.HEIGHT - self.bar_height)/2)
        self.rect2.topleft = (self.WIDTH - self.bar_width - 5, (self.HEIGHT - self.bar_height)/2)
        self.y1_change = 0
        self.y2_change = 0
        
        # Ball
        self.ball_center = [(self.rect2.left - self.ball_radius - 5), self.rect2.center[1]]
        self.ball_x_change = 0
        self.ball_y_change = 0
        self.ball_color = self.blue
        
        # Text for instructions
        self.text = self.font2.render("Press SPACE to start, P to pause", True, self.white)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.WIDTH / 2, (self.HEIGHT + self.upper_boundary) / 2)
        
    def distance(self, c1, c2):
        return math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
    
    def reset_ball(self):
        self.ball_x_change = -(
                (random.random() * ((self.ball_speed / math.sqrt(2)) - (self.ball_speed * math.sqrt(3) / 2))) + (
                self.ball_speed * math.sqrt(3) / 2))
        self.ball_y_change = (math.sqrt((self.ball_speed ** 2) - (self.ball_x_change ** 2))) * (
                (-1) ** (int(random.random() * 2) + 1))
        self.rect1.topleft = (5, (self.HEIGHT - self.bar_height) / 2)
        self.rect2.topleft = (self.WIDTH - self.bar_width - 5, (self.HEIGHT - self.bar_height) / 2)
        self.ball_center = [(self.rect2.left - self.ball_radius - 5), self.rect2.center[1]]
        self.ball_trail = []
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.ball_state == "rest":
                    self.ball_state = "motion"
                    self.reset_ball()
                    
                if event.key == pygame.K_p:
                    self.game_paused = not self.game_paused
                    
                if event.key == pygame.K_1:
                    self.difficulty = "easy"
                if event.key == pygame.K_2:
                    self.difficulty = "medium"
                if event.key == pygame.K_3:
                    self.difficulty = "hard"
                    
                if event.key == pygame.K_UP:
                    self.y1_change = -self.bar_speed
                if event.key == pygame.K_DOWN:
                    self.y1_change = self.bar_speed
                    
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    self.y1_change = 0
                    
        return True
    
    def update_score_display(self):
        self.result.fill(self.black)
        pygame.draw.rect(self.result, self.white, (5, 5, self.WIDTH - 10, self.upper_boundary - 5), 1)
        
        score_text11 = self.font.render("PLAYER", True, self.white)
        score_text12 = self.font.render(f"SCORE: {self.score1}", True, self.white)
        score_text21 = self.font.render(f"AI ({self.difficulty.upper()})", True, self.white)
        score_text22 = self.font.render(f"SCORE: {self.score2}", True, self.white)
        
        self.result.blit(score_text11, (50, 13))
        self.result.blit(score_text12, (50, 55))
        self.result.blit(score_text21, (self.WIDTH - 200, 13))
        self.result.blit(score_text22, (self.WIDTH - 200, 55))
        self.screen.blit(self.result, (0, 0))
    
    def check_boundaries(self):
        # Paddle boundaries
        if self.rect1.top < self.upper_boundary:
            self.rect1.top = self.upper_boundary
        if self.rect1.bottom > self.lower_boundary:
            self.rect1.bottom = self.lower_boundary
        if self.rect2.top < self.upper_boundary:
            self.rect2.top = self.upper_boundary
        if self.rect2.bottom > self.lower_boundary:
            self.rect2.bottom = self.lower_boundary
            
        # Ball scoring
        if self.ball_center[0] < -(self.ball_radius / 2):
            self.score2 += 1
            self.ball_state = "rest"
            mixer.stop()
            self.beep_sound.play()
            time.sleep(0.2)
            self.reset_ball()
            return True
            
        elif self.ball_center[0] > self.WIDTH + (self.ball_radius / 2):
            self.score1 += 1
            self.ball_state = "rest"
            mixer.stop()
            self.beep_sound.play()
            time.sleep(0.2)
            self.reset_ball()
            return True
            
        return False
    
    def handle_ball_collision(self):
        if self.ball_state != "motion":
            return
            
        # Ball trail effect
        self.ball_trail.append(list(self.ball_center))
        if len(self.ball_trail) > self.max_trail_length:
            self.ball_trail.pop(0)
            
        # Top and bottom boundaries
        if abs(self.ball_center[1] - self.upper_boundary) <= self.ball_radius:
            self.ball_y_change *= (-1)
            self.ball_center[1] = self.upper_boundary + self.ball_radius  # Prevent sticking
            mixer.stop()
            self.collide_sound.play()
            self.ball_color = self.green  # Change color on collision
            
        if abs(self.ball_center[1] - self.lower_boundary) <= self.ball_radius:
            self.ball_y_change *= (-1)
            self.ball_center[1] = self.lower_boundary - self.ball_radius  # Prevent sticking
            mixer.stop()
            self.collide_sound.play()
            self.ball_color = self.yellow  # Change color on collision
            
        # Paddle collisions - simplified and improved
        # Left paddle (player)
        if (self.ball_center[0] - self.ball_radius <= self.rect1.right and 
            self.ball_center[0] + self.ball_radius >= self.rect1.left and
            self.ball_center[1] + self.ball_radius >= self.rect1.top and 
            self.ball_center[1] - self.ball_radius <= self.rect1.bottom):
            
            # Calculate angle based on where ball hits paddle
            relative_intersect_y = (self.rect1.centery - self.ball_center[1]) / (self.bar_height/2)
            bounce_angle = relative_intersect_y * (math.pi/4)  # Max 45 degrees
            
            # Ensure ball moves right after hitting left paddle
            self.ball_x_change = abs(self.ball_speed * math.cos(bounce_angle))
            self.ball_y_change = -self.ball_speed * math.sin(bounce_angle)
            
            # Move ball outside paddle to prevent multiple collisions
            self.ball_center[0] = self.rect1.right + self.ball_radius + 1
            
            mixer.stop()
            self.collide_sound.play()
            self.ball_color = self.red  # Change color to match paddle
            
        # Right paddle (AI)
        if (self.ball_center[0] + self.ball_radius >= self.rect2.left and 
            self.ball_center[0] - self.ball_radius <= self.rect2.right and
            self.ball_center[1] + self.ball_radius >= self.rect2.top and 
            self.ball_center[1] - self.ball_radius <= self.rect2.bottom):
            
            # Calculate angle based on where ball hits paddle
            relative_intersect_y = (self.rect2.centery - self.ball_center[1]) / (self.bar_height/2)
            bounce_angle = relative_intersect_y * (math.pi/4)  # Max 45 degrees
            
            # Ensure ball moves left after hitting right paddle
            self.ball_x_change = -abs(self.ball_speed * math.cos(bounce_angle))
            self.ball_y_change = -self.ball_speed * math.sin(bounce_angle)
            
            # Move ball outside paddle to prevent multiple collisions
            self.ball_center[0] = self.rect2.left - self.ball_radius - 1
            
            mixer.stop()
            self.collide_sound.play()
            self.ball_color = self.purple  # Change color to match paddle
    
    def update_ai(self):
        if self.ball_state != "motion":
            return
            
        # AI difficulty settings
        reaction_delay = 0
        error_margin = 0
        
        if self.difficulty == "easy":
            reaction_delay = 0.3
            error_margin = 30
        elif self.difficulty == "medium":
            reaction_delay = 0.1
            error_margin = 15
        else:  # hard
            reaction_delay = 0
            error_margin = 5
            
        # Only react if ball is moving toward AI
        if self.ball_x_change > 0:
            # Predict where ball will be
            time_to_reach = (self.rect2.left - self.ball_center[0]) / self.ball_x_change if self.ball_x_change != 0 else 0
            predicted_y = self.ball_center[1] + (self.ball_y_change * time_to_reach)
            
            # Add some randomness based on difficulty
            predicted_y += random.uniform(-error_margin, error_margin)
            
            # Add reaction delay
            if random.random() > reaction_delay:
                # Move toward predicted position
                if predicted_y > self.rect2.centery + 5:
                    self.y2_change = self.bar_speed
                elif predicted_y < self.rect2.centery - 5:
                    self.y2_change = -self.bar_speed
                else:
                    self.y2_change = 0
        else:
            # Return to center when ball moving away
            if abs(self.rect2.centery - self.HEIGHT/2) > 10:
                if self.rect2.centery > self.HEIGHT/2:
                    self.y2_change = -self.bar_speed/2
                else:
                    self.y2_change = self.bar_speed/2
            else:
                self.y2_change = 0
    
    def draw_game(self):
        self.screen.fill(self.black)
        self.update_score_display()
        
        # Draw paddles
        self.screen.blit(self.player1, self.rect1)
        self.screen.blit(self.player2, self.rect2)
        
        # Draw ball trail
        for i, pos in enumerate(self.ball_trail):
            alpha = int(255 * (i / len(self.ball_trail)))
            radius = int(self.ball_radius * (i / len(self.ball_trail)))
            if radius < 1:
                radius = 1
            s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.ball_color[:3], alpha), (radius, radius), radius)
            self.screen.blit(s, (pos[0]-radius, pos[1]-radius))
        
        # Draw ball
        pygame.draw.circle(self.screen, self.ball_color, 
                          (int(self.ball_center[0]), int(self.ball_center[1])), 
                          self.ball_radius)
        
        # Draw center line
        for y in range(self.upper_boundary, self.HEIGHT, 20):
            pygame.draw.rect(self.screen, self.white, 
                            (self.WIDTH//2 - 1, y, 2, 10))
        
        # Draw instructions
        if self.ball_state == "rest":
            self.screen.blit(self.text, self.text_rect)
            
        # Draw pause indicator
        if self.game_paused:
            pause_text = self.font.render("PAUSED", True, self.white)
            pause_rect = pause_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
            self.screen.blit(pause_text, pause_rect)
            
        # Draw difficulty indicator
        diff_text = self.font2.render(f"Difficulty: {self.difficulty.upper()} (Press 1-3 to change)", 
                                     True, self.white)
        self.screen.blit(diff_text, (10, self.HEIGHT - 20))
    
    def run(self):
        running = True
        first_run = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # First run setup
            if first_run:
                first_run = False
                self.ball_state = "rest"
                self.reset_ball()
            
            # Skip updates if paused
            if self.game_paused:
                self.draw_game()
                pygame.display.flip()
                self.clock.tick(60)
                continue
                
            # Check boundaries and update score
            score_changed = self.check_boundaries()
            
            # Update paddles
            self.rect1.top += self.y1_change
            self.rect2.top += self.y2_change
            
            # Handle ball movement and collisions
            self.handle_ball_collision()
            
            # Update AI
            self.update_ai()
            
            # Move ball if in motion
            if self.ball_state == "motion" and not score_changed:
                self.ball_center[0] += self.ball_x_change
                self.ball_center[1] += self.ball_y_change
            
            # Draw everything
            self.draw_game()
            
            # Update display and maintain frame rate
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

# Start the game
if __name__ == "__main__":
    game = PongGame()
    game.run()
