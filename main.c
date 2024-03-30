#include <stdio.h>
#include <stdlib.h>
#include "car.h"

void update_cars(Car *cars, int num_cars, float time) {
    for (int i = 0; i < num_cars; i++) {
        cars[i].posx = cars[i].posx + (cars[i].velx * time) + (0.5 * cars[i].accx * time * time); // position equation
        cars[i].posy = cars[i].posy + (cars[i].vely * time) + (0.5 * cars[i].accy * time * time);
        cars[i].velx = cars[i].velx + (cars[i].accx * time); // velocity equation
        cars[i].vely = cars[i].vely + (cars[i].accy * time);
        printf("car %d: posx: %f, posy: %f ", i, cars[i].posx, cars[i].posy);
    }
    printf("\n");
}

int will_collide(Car *cars, int car_a, int car_b) {
    return 1;
}

int main() {

    Car *cars; // support up to 10 cars. each car has posx (m), posy (m), velx (m/s), vely (m/s), accx (m/s^2), accy (m/s^2)
    int num_cars = 2; // number of cars
    cars = (Car *) malloc(sizeof(Car) * num_cars);

    // initialize problem set
    // intersection:
    // - each lane is 3 meters wide. this creates 6mx6m intersection zone.
    // - cars enter proximity of concurrent traffic 50m before the intersection zone on all four sides.
    // - this creates 106mx106m plane.
    // - to simplify, the top left of the intersection zone is (0,0).
    // - this makes minimum xy (-50,-50) and maximum xy (56,56)
    cars[0].posx = -50;
    cars[0].posy = 4.5;
    cars[0].velx = 15;
    cars[0].vely = 0;
    cars[0].accx = 0;
    cars[0].accy = 0;

    cars[1].posx = 1.5;
    cars[1].posy = -50;
    cars[1].velx = 0;
    cars[1].vely = 15;
    cars[1].accx = 0;
    cars[1].accy = 0;

    float simulation_time = 5;  // seconds
    float update_interval = 0.1; // seconds
    float time_elapsed = 0;      // seconds

    // print starting position
    printf("start:\n");
    for (int i = 0; i < num_cars; i++) {
        printf("car %d: posx: %f, posy: %f ", i, cars[i].posx, cars[i].posy);
    }
    printf("\n");

    Collision *collisions;
    int num_collisions = 0;

    // calculate collisions
    for (int a = 0; a < num_cars; a++) {
        
    }

    while (time_elapsed <= simulation_time) {
        update_cars(cars, num_cars, update_interval);
        time_elapsed += update_interval;
    }

    free(cars);
    return 0;
}