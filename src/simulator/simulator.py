import pygame
import numpy as np

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

NORTH_LINE = np.array([0,1,0])
EAST_LINE = np.array([1,0,-6])
WEST_LINE = np.array([1,0,0])
SOUTH_LINE = np.array([0,1,-6])

WORLD_WIDTH_OFFSET = 50
WORLD_HEIGHT_OFFSET = 50
WORLD_WIDTH = 106
WORLD_HEIGHT = 106

def coord_to_screen_coord(x, y):
    return [(x + WORLD_WIDTH_OFFSET) / WORLD_WIDTH * SCREEN_WIDTH, (y + WORLD_HEIGHT_OFFSET) / WORLD_HEIGHT * SCREEN_HEIGHT]

def run_simulation():
    # cars = []
    # cars.append(Car([-50,4.5],[15,0],[0,0], Direction.EAST_BOUND))
    # cars.append(Car([1.5,-50],[0,15],[0,0], Direction.SOUTH_BOUND))
    # # cars.append(Car([4.5,50],[0,-15],[0,0], Direction.NORTH_BOUND))

    # # calculate distances and sort cars by it.
    # for car in cars:
    #     update_distance_to_intersection(car)
    # cars = sorted(cars, key=lambda x: x.distance_to_intersection)

    # calculate collisions with first car


    pygame.init()
    screen = pygame.display.set_mode((560, 560))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        # # render cars
        # for car in cars:
        #     car_screen_x, car_screen_y = coord_to_screen_coord(car.pos[0], car.pos[1])
        #     print(car_screen_x)
        #     print(car_screen_y)
        #     # pygame.draw.circle(screen, "red", pygame.Vector2(car_screen_x, car_screen_y), 40)
        #     car_rect = pygame.Rect(car_screen_x, car_screen_y, 30, 30)
        #     pygame.draw.rect(screen, "red", car_rect, 0)

        # # update cars
        # for car in cars:
        #     car.pos[0] = car.pos[0] + car.vel[0] * dt
        #     car.pos[1] = car.pos[1] + car.vel[1] * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()