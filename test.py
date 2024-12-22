import pygame
import sys
import math

FPS = 60
WIDTH, HEIGHT = 1280, 720

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fast Seamless Scrolling Background")
clock = pygame.time.Clock()

# Load background layers
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"assets/background_image/plx-{i}.png").convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

# Initialize scroll positions for each layer
scroll_positions = [0] * len(bg_images)


def draw_bg():
    for i, image in enumerate(bg_images):
        # Faster speed for each layer
        speed = 1.4 * (i + 1)  # Much faster speed multiplier

        # Update scroll position for this layer
        scroll_positions[i] = (scroll_positions[i] + speed) % bg_width

        # Draw the layer with tiles
        for x in range(-1, math.ceil(WIDTH / bg_width) + 2):
            pos_x = x * bg_width - scroll_positions[i]
            screen.blit(image, (pos_x, 0))


running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the background
    draw_bg()

    # Update the display
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()