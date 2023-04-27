import sys

import pygame as pg
import pymunk as pm
import pymunk.pygame_util, pymunk.constraints


def add_ball(x, y):
    particle = pm.Body()
    particle.position = pm.Vec2d(x, y)
    mass = 1
    radius = 25
    shape = pm.Circle(particle, radius)  # 3
    shape.mass = mass  # 4
    shape.friction = 1
    space.add(particle, shape)  # 5


def add_wall(rect):
    wall = pm.Body(body_type=pm.Body.STATIC)
    # vertices = [(-400, 300), (400, 300), (400, -300), (-400, -300)]
    vs = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
    wallpoly = pm.Poly(wall, vs)
    wallpoly.friction = 2
    space.add(wall, wallpoly)


def triangle():
    b1 = pm.Body(mass=1)
    b1.position = pm.Vec2d(375, 100)
    b2 = pm.Body(mass=1)
    b2.position = pm.Vec2d(425, 100)
    b3 = pm.Body(mass=1)
    b3.position = pm.Vec2d(400, 125)
    pj1 = pm.PinJoint(b1, b2)
    pj2 = pm.PinJoint(b2, b3)
    pj3 = pm.PinJoint(b1, b3)
    shape1 = pm.Circle(b1, 10)
    shape1.mass = b1.mass
    shape2 = pm.Circle(b2, 10)
    shape2.mass = b2.mass
    shape3 = pm.Circle(b3, 10)
    shape3.mass = b3.mass
    space.add(b1, b2, b3, shape1, shape2, shape3)
    space.add(pj3, pj2, pj1)


space = pm.Space()
space.gravity = pm.Vec2d(0, 900)

add_ball(400, 100)

add_wall(pg.Rect((25, 575), (750, 25)))
add_wall(pg.Rect((25, 275), (25, 300)))
add_wall(pg.Rect((750, 275), (25, 300)))


canvas = pg.Surface((800, 600))
draw_options = pm.pygame_util.DrawOptions(canvas)

screen = pg.display.set_mode((800, 600))
fps = 60
clock = pg.time.Clock()


def update(dt: float):
    space.step(dt)
    manage_events()


def draw():
    # pg.draw.circle(canvas, pg.Color('white'), particle.position, 10)
    space.debug_draw(draw_options)


def base_draw():
    canvas.fill(0)
    draw()
    screen.blit(canvas, (0, 0))
    pg.display.flip()
    clock.tick(fps)


def manage_events():
    quit_events = pg.event.get(pg.QUIT)
    click_events = pg.event.get(pg.MOUSEBUTTONUP)
    if len(quit_events) > 0:
        sys.exit(1)
    if len(click_events) > 0:
        x, y = pg.mouse.get_pos()
        # add_ball(x, y)
        triangle()


while True:
    update(dt=1.0/fps)
    # print(particle.position)
    base_draw()