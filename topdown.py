import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

# Player movement
def move_player():
  keys = pygame.key.get_pressed()
  x_change, y_change = 0, 0
  if keys[pygame.K_a]:
      x_change -= player_speed
  if keys[pygame.K_d]:
      x_change += player_speed
  if keys[pygame.K_w]:
      y_change -= player_speed
  if keys[pygame.K_s]:
      y_change += player_speed

  # Check if new position collides with the wall
  new_rect = pygame.Rect(player_pos[0] + x_change, player_pos[1] + y_change, 50, 50)
  if not wall.colliderect(new_rect):
      player_pos[0] += x_change
      player_pos[1] += y_change

# Draw player
def draw_player():
  pygame.draw.rect(screen, (0, 128, 255), (*player_pos, 50, 50))

# Player Stats
bullets = []
bullet_speed = 10
player_health = 100
player_max_health = 100

def take_player_damage(amount):
    global player_health
    player_health -= amount
    if player_health <= 0:
        print("Game Over!")
        pygame.quit()
        sys.exit()


# Flag to toggle editor mode
editor_mode = True

# Shoot bullets
def shoot_bullet():
  if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      dx = mouse_x - (player_pos[0] + 25)
      dy = mouse_y - (player_pos[1] + 25)
      distance = (dx**2 + dy**2)**0.5
      bullet_velocity = [dx / distance * bullet_speed, dy / distance * bullet_speed]
      # Adjust bullet spawn position
      bullets.append([player_pos[0] + 25, player_pos[1] + 25, *bullet_velocity]) 

def move_bullets():
  for bullet in bullets[:]:
      bullet[0] += bullet[2]  # X-coordinate update
      bullet[1] += bullet[3]  # Y-coordinate update
      if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH or bullet[1] < 0 or bullet[1] > SCREEN_HEIGHT:
          bullets.remove(bullet)

def draw_bullets():
  for bullet in bullets:
      pygame.draw.rect(screen, (255, 0, 0), (*bullet[:2], 10, 10)) # Draw bullets as small red squares


# Wall settings
wall = pygame.Rect(300, 200, 200, 50)  # Position and size


def draw_wall():
  pygame.draw.rect(screen, (255, 255, 255), wall)  # Draw wall as white


# Check for bullet collisions with the wall
def bullet_wall_collision():
  global bullets
  bullets = [
      bullet for bullet in bullets
      if not wall.collidepoint(bullet[0] + 5, bullet[1] + 5)
  ]

class Zombie:
  def __init__(self, x, y, health=100, speed=2, damage=10):
      self.rect = pygame.Rect(x, y, 40, 40)  # Zombies are 40x40 pixels
      self.health = health
      self.speed = speed
      self.damage = damage
      self.color = (0, 255, 0)

  def move_towards_player(self, player_position):
      dx = player_position[0] - self.rect.x
      dy = player_position[1] - self.rect.y
      distance = (dx**2 + dy**2)**0.5
      if distance != 0:
          self.rect.x += int(dx / distance * self.speed)
          self.rect.y += int(dy / distance * self.speed)

  def draw(self, screen):
      pygame.draw.rect(screen, self.color, self.rect)

  def take_damage(self, amount):
      self.health -= amount
      if self.health <= 0:
          return True  # Zombie is dead
      return False

# Functions for zombie collisions
def handle_bullet_zombie_collisions():
  global bullets, zombies
  for bullet in bullets[:]:
      bullet_rect = pygame.Rect(*bullet[:2], 10, 10)
      for zombie in zombies[:]:
          if zombie.rect.colliderect(bullet_rect):
              if zombie.take_damage(20):  # Assume each bullet does 20 damage
                  zombies.remove(zombie)
              bullets.remove(bullet)
              break

def handle_zombie_player_collisions():
  for zombie in zombies:
      if zombie.rect.colliderect(pygame.Rect(*player_pos, 50, 50)):
          take_player_damage(zombie.damage)

zombies = [Zombie(100, 100), Zombie(700, 500)]

# Main game loop
while True:
  for event in pygame.event.get():
    shoot_bullet()

    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  # Movement
  move_player()
  move_bullets()

  for zombie in zombies:
    zombie.move_towards_player(player_pos)

  handle_bullet_zombie_collisions()
  handle_zombie_player_collisions()


  # Drawing
  screen.fill((0, 0, 0)) # Fill screen with a color to clear it.
  draw_wall()
  draw_player()
  draw_bullets()
  for zombie in zombies:
    zombie.draw(screen)

  # Update display
  pygame.display.flip()

  # Cap framerate
  clock.tick(FPS)