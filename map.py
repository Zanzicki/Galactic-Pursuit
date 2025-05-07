import pygame, sys, random
# Made by: Erik 
pygame.init()

screen_width = 800
screen_height = 600

text = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galactic Map")

# setting up ship image and position 
ship_image = pygame.image.load("spaceship_01.png")
ship_image = pygame.transform.scale(ship_image, (100, 100)) # scale the image to fit the circles
ship_pos = [screen_width // 2, screen_height // 2] # center the ship in the middle of the screen
ship_speed = 0.1 # speed of the ship

colors =[
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 0, 255), # Magenta    
]
# list of chances for each color to be chosen
# the sum of the weights should be 1.0, so they are normalized to 1.0
weights = [0.6, 0.1, 0.2,0.1]

planet_names = [
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "Eris"]

used_names = []

def does_overLap(new_pos, new_radius, existing_circles):
    for _, circle_radius, circle_pos, _ in existing_circles: #_ is used to ignore the color and name of the circle
        distance = ((new_pos[0] - circle_pos[0]) ** 2 + (new_pos[1] - circle_pos[1]) ** 2) ** 0.5
        if distance < new_radius + circle_radius +5 :
            return True
    return False

# circles = planets on the map 
cicles = []
attempts = 0
while len(cicles) < 10 and attempts < 1000:
    circle_color = random.choices(colors, weights=weights)[0]
    circle_radius = random.randint(35, 50)
    buffer = 10
    circle_pos = (
        random.randint(circle_radius + buffer, screen_width - circle_radius - buffer),
        random.randint(circle_radius + buffer, screen_height - circle_radius - buffer)
        
    )
     
    if not does_overLap(circle_pos, circle_radius, cicles): 
        
        available_names = [name for name in planet_names if name not in used_names]
        if available_names:
            planet_name = random.choice(available_names)
            used_names.append(planet_name)
            planet_names.remove(planet_name) 
            cicles.append((circle_color, circle_radius, circle_pos, planet_name))  # nu tilføjes cirklen korrekt

    attempts += 1


def is_mouse_over_circle(circle_pos, circle_radius):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    distance = ((mouse_x - circle_pos[0]) ** 2 + (mouse_y - circle_pos[1]) ** 2) ** 0.5
    return distance <= circle_radius

running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ship_pos[0] -= ship_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ship_pos[0] += ship_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        ship_pos[1] -= ship_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        ship_pos[1] += ship_speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for circle_color, circle_radius, circle_pos, planet_name in cicles:
                    dx = ship_pos[0] - circle_pos[0]
                    dy = ship_pos[1] - circle_pos[1]
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    if distance <= circle_radius + 20:
                        if circle_color == (255, 0, 0):
                            print(f"{planet_name} (Red): Start kamp!") # indsæt logik til at starte kamp her
                        elif circle_color == (0, 255, 0):
                            print(f"{planet_name} (Green): Artifact menu!") # indsæt logik til at åbne artefakt menu her
                        elif circle_color == (0, 0, 255):
                            print(f"{planet_name} (Blue): Shop åbnes!") # indsæt logik til at åbne shop her
                        elif circle_color == (255, 0, 255):
                            print(f"{planet_name} (Magenta): Mystery event!") # indsæt logik til at åbne mystisk event her

    screen.fill((0, 0, 0))

    # Draw the map here
    pygame.draw.circle(screen, (255, 223, 0), (400, 300), 100)  # sun in the midelle of the screen 

    for circle_color, circle_radius, circle_pos, planet_name in cicles:
        pygame.draw.circle(screen, circle_color, circle_pos, circle_radius)

        # check the distance between the ship and the planet      
        dx = ship_pos[0] - circle_pos[0]
        dy = ship_pos[1] - circle_pos[1]
        ship_distance = (dx ** 2 + dy ** 2) ** 0.5
        # check the distance between the mouse and the planet
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_dist = ((mouse_x - circle_pos[0]) ** 2 + (mouse_y - circle_pos[1]) ** 2) ** 0.5

    # if the ship is close to the planet or the mouse is over the planet, draw a white circle around it
    # and show the planet name
        if ship_distance <= circle_radius + 20 or mouse_dist <= circle_radius:
    # white circle around the planet
            pygame.draw.circle(screen, (255, 255, 255), circle_pos, circle_radius + 5, 2)
    # show planet name
            text_surface = text.render(planet_name, True, (255, 255, 255))
            text_x = max(0, min(circle_pos[0] - circle_radius, screen_width - text_surface.get_width()))
            text_y = max(0, circle_pos[1] - circle_radius - 30)
            screen.blit(text_surface, (text_x, text_y))



    # draw the ship
    screen.blit(ship_image, (ship_pos[0] - ship_image.get_width() // 2, ship_pos[1] - ship_image.get_height() // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
