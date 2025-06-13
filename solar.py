import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Solar System with Planets")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("Arial", 16)

def calculate_gravity(mass, radius):
    G = 6.67430e-11
    return G * mass / (radius ** 2)

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.5, 2.0)
        self.direction = 1

    def update(self):
        self.brightness += self.direction * self.twinkle_speed
        if self.brightness >= 255:
            self.brightness = 255
            self.direction = -1
        elif self.brightness <= 100:
            self.brightness = 100
            self.direction = 1

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (self.x, self.y), 1)

class Planet:
    def __init__(self, name, image_file, orbit_radius, orbit_speed, scale=1.0):
        self.name = name
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed / 2
        self.angle = random.uniform(0, math.pi * 2)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.original_image = self.image
        self.scale = scale * 1.5
        self.x = 0
        self.y = 0

        planet_data = {
            "Mercury": {"mass": 3.3011e23, "radius": 2439.7},
            "Venus": {"mass": 4.8675e24, "radius": 6051.8},
            "Earth": {"mass": 5.972e24, "radius": 6371},
            "Mars": {"mass": 6.4171e23, "radius": 3389.5},
            "Jupiter": {"mass": 1.8982e27, "radius": 69911},
            "Saturn": {"mass": 5.6834e26, "radius": 58232},
            "Uranus": {"mass": 8.6810e25, "radius": 25362},
            "Neptune": {"mass": 1.02413e26, "radius": 24622},
            "Sun": {"mass": 1.989e30, "radius": 696340},
        }
        self.mass = planet_data[self.name]["mass"]
        self.radius = planet_data[self.name]["radius"]
        self.gravity = calculate_gravity(self.mass, self.radius)

    def draw(self, screen, center, zoom, paused):
        orbit = self.orbit_radius * zoom
        self.x = center[0] + orbit * math.cos(self.angle)
        self.y = center[1] + orbit * math.sin(self.angle)
        pygame.draw.circle(screen, (80, 80, 80), center, int(orbit), 1)

        size = max(10, int(20 * zoom * self.scale))
        self.image = pygame.transform.scale(self.original_image, (size, size))
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, rect)

        if not paused:
            self.angle += self.orbit_speed

    def is_hovered(self, mouse_pos):
        return math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y) < 15

stars = [Star(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(200)]

planets = [
    Planet("Mercury", "mercury.png", 60, 0.02, 0.4),
    Planet("Venus", "venus.png", 90, 0.015, 0.6),
    Planet("Earth", "earth.png", 120, 0.012, 0.7),
    Planet("Mars", "mars.png", 160, 0.01, 0.6),
    Planet("Jupiter", "jupiter.png", 220, 0.007, 1.4),
    Planet("Saturn", "saturn.png", 280, 0.005, 1.3),
    Planet("Uranus", "uranus.png", 340, 0.003, 1.0),
    Planet("Neptune", "neptune.png", 400, 0.002, 1.0),
]
sun = Planet("Sun", "sun.png", 0, 0, 2.0)

scale = 1.0
center = (WIDTH // 2, HEIGHT // 2)
paused = False

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scale *= 1.1
            elif event.button == 5:
                scale /= 1.1

    SCREEN.fill((0, 0, 0))

    for star in stars:
        star.update()
        star.draw(SCREEN)

    sun.draw(SCREEN, center, scale, paused)

    mouse_pos = pygame.mouse.get_pos()
    for planet in planets:
        planet.draw(SCREEN, center, scale, paused)

    if sun.is_hovered(mouse_pos):
        info = FONT.render(
            f"{sun.name} - Gravity: {sun.gravity:.2e} m/s² - Radius: {sun.radius} km", True, WHITE
        )
        SCREEN.blit(info, (mouse_pos[0] + 10, mouse_pos[1] + 10))
    for planet in planets:
        if planet.is_hovered(mouse_pos):
            info = FONT.render(
                f"{planet.name} - Gravity: {planet.gravity:.2e} m/s² - Radius: {planet.radius} km",
                True,
                WHITE,
            )
            SCREEN.blit(info, (mouse_pos[0] + 10, mouse_pos[1] + 10))

    pygame.display.flip()
