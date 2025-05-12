import pygame
import random
import sys
import pygame_gui
import pygame_gui.ui_manager


#Made by Erik
# This code is a simple game map with planets and a spaceship.
# The player can move the spaceship around the map and interact with planets.
class GameWorld:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Galactic Map")
        self._running = True
        self._state = "map"

class Map:
    def __init__(self, game_world):
        self.game_world = game_world
        self.screen = game_world.screen
        self.ship_image = pygame.image.load("Assets/spaceship_01.png")  # Load the ship image
        self.ship_image = pygame.transform.scale(self.ship_image, (100, 100))  # Scale the ship image
        self.ship_pos = [self.game_world.width // 2, self.game_world.height // 2]  # Center the ship
        self.ship_speed = 0.5  # Speed of the ship
        self.planets = self.generate_planets()
        self.font = pygame.font.Font(None, 36)
        
        self.ui_manager = pygame_gui.UIManager((self.game_world.width, self.game_world.height))
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Back',
            manager=self.ui_manager
        )
        
        

    def generate_planets(self):
        """Generate planets with random positions, colors, and names."""
        colors = [
            (255, 0, 0),   # Red (Fight)
            (0, 255, 0),   # Green (Artifact)
            (0, 0, 255),   # Blue (Shop)
            (255, 0, 255), # Magenta (Mystery)
        ]
        weights = [0.6, 0.1, 0.2, 0.1]  # Probabilities for each color
        planet_names = [
            "Mercury", "Venus", "Earth", "Mars", "Jupiter",
            "Saturn", "Uranus", "Neptune", "Pluto", "Eris"
        ]
        used_names = []
        planets = []

        for _ in range(10):  # Generate 10 planets
            color = random.choices(colors, weights=weights)[0]
            radius = random.randint(35, 50)
            buffer = 10
            pos = (
                random.randint(radius + buffer, self.game_world.width - radius - buffer),
                random.randint(radius + buffer, self.game_world.height - radius - buffer)
            )

            # Ensure no overlap with existing planets
            if not self.does_overlap(pos, radius, planets):
                available_names = [name for name in planet_names if name not in used_names]
                if available_names:
                    name = random.choice(available_names)
                    used_names.append(name)
                    planet_names.remove(name)
                    planets.append({"color": color, "radius": radius, "pos": pos, "name": name})

        return planets

    def does_overlap(self, new_pos, new_radius, existing_planets):
        """Check if a new planet overlaps with existing planets."""
        for planet in existing_planets:
            distance = ((new_pos[0] - planet["pos"][0]) ** 2 + (new_pos[1] - planet["pos"][1]) ** 2) ** 0.5
            if distance < new_radius + planet["radius"] + 5:
                return True
        return False

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            time_delta = clock.tick(60) / 1000.0  # For pygame_gui timing

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_world._running = False
                    running = False
                
                self.ui_manager.process_events(event)  #  required for GUI

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_button:
                        print("Back button pressed")
                        self.game_world._state = "menu"
                        return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for planet in self.planets:
                        dx = self.ship_pos[0] - planet["pos"][0]
                        dy = self.ship_pos[1] - planet["pos"][1]
                        distance = (dx ** 2 + dy ** 2) ** 0.5
                        if distance <= planet["radius"] + 20:
                            if planet["color"] == (0, 0, 255):  # Blue (Shop)
                                print(f"{planet['name']} (Blue): Entering shop!")
                                self.game_world._state = "shop"  # Transition to shop state
                                return
                            elif planet["color"] == (255, 0, 0):  # Red (Fight)
                                print(f"{planet['name']} (Red): Entering fight!")
                                self.game_world._state = "game"  # Transition to game state
                                return
            self.ui_manager.update(time_delta)  # 👈 updates GUI state
            # Handle ship movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.ship_pos[0] -= self.ship_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.ship_pos[0] += self.ship_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.ship_pos[1] -= self.ship_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.ship_pos[1] += self.ship_speed

            # Draw the map
            self.screen.fill((0, 0, 0))
            pygame.draw.circle(self.screen, (255, 223, 0), (400, 300), 100)  # Sun in the center

            for planet in self.planets:
                pygame.draw.circle(self.screen, planet["color"], planet["pos"], planet["radius"])

                # Highlight planet if ship or mouse is close
                dx = self.ship_pos[0] - planet["pos"][0]
                dy = self.ship_pos[1] - planet["pos"][1]
                ship_distance = (dx ** 2 + dy ** 2) ** 0.5
                if ship_distance <= planet["radius"] + 20:
                    pygame.draw.circle(self.screen, (255, 255, 255), planet["pos"], planet["radius"] + 5, 2)
                    text_surface = self.font.render(planet["name"], True, (255, 255, 255))
                    self.screen.blit(text_surface, (planet["pos"][0] - 20, planet["pos"][1] - 40))

            # Draw the ship
            self.screen.blit(
                self.ship_image,
                (self.ship_pos[0] - self.ship_image.get_width() // 2, self.ship_pos[1] - self.ship_image.get_height() // 2)
            )
            # Draw the back button
            self.ui_manager.draw_ui(self.screen)  # Draw the GUI elements

            pygame.display.flip()