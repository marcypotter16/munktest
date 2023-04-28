from math import sin, cos, pi

import pymunk as pm
import pygame as pg
from UI.CheckBox import *
from munktest.States.State import State
from munktest.UI.Abstract import UICanvas
from munktest.UI.Label import Label
from munktest.UI.Slider import Slider

space = pm.Space()
space.gravity = pm.Vec2d(0, 900)


def add_fixed_ball(x, y, radius=10) -> (pm.Body, pm.Shape):
    particle = pm.Body(body_type=pm.Body.KINEMATIC)
    particle.position = pm.Vec2d(x, y)
    mass = 1
    shape = pm.Circle(particle, radius)
    shape.mass = mass
    shape.friction = 1
    space.add(particle, shape)
    return particle, shape


def add_ball(x, y, radius=10) -> (pm.Body, pm.Shape):
    particle = pm.Body()
    particle.position = pm.Vec2d(x, y)
    mass = 1
    shape = pm.Circle(particle, radius)
    shape.mass = mass
    shape.friction = 1
    space.add(particle, shape)
    return particle, shape


def add_wall(rect) -> pg.Rect:
    wall = pm.Body(body_type=pm.Body.STATIC)
    vs = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
    wallpoly = pm.Poly(wall, vs)
    wallpoly.friction = 2
    space.add(wall, wallpoly)
    return rect


def add_spring(a: pm.Body, b: pm.Body, stiffness) -> pm.DampedSpring:
    if a != b:
        spring = pm.DampedSpring(a, b, (0, 0), (0, 0), a.position.get_distance(b.position), stiffness, 1)
        space.add(spring)
        return spring


def pentagon(x, y, r):
    pt = pi/10
    A = (x + r * cos(pt), y + r * sin(pt))
    B = (x, y + r)
    C = (x - r * cos(pt), y + r * sin(pt))
    D = (x - r * cos(3 * pt), y - r * sin(3 * pt))
    E = (x + r * cos(3 * pt), y - r * sin(3 * pt))
    vertices = [A, B, C, D, E]
    bodies = [pm.Body() for i in range(5)]
    shapes = [pm.Circle(body, 10) for body in bodies]
    springs = []
    for i, body in enumerate(bodies):
        body.position = vertices[i]
    for i, body in enumerate(bodies):
        if i != len(bodies):
            for j in range(i + 1, len(bodies)):
                if body != bodies[j]:
                    springs.append(pm.DampedSpring(body, bodies[j], (0, 0), (0, 0), body.position.get_distance(bodies[j].position), 100, 1))
    for shape in shapes:
        shape.mass = 1
        shape.friction = 1.5
    for i, body in enumerate(bodies):
        space.add(body, shapes[i])
    for spring in springs:
        space.add(spring)
    return vertices, bodies, shapes, springs


class ShapeCreator(State):
    def __init__(self, game):
        super().__init__(game)
        self.pentagon = None
        self.walls = []
        self.balls = []
        self.springs = []
        self._poly = []
        self._stop_poly = False
        self.load_geometry()
        self.canvas = UICanvas(game=game)
        self.draw_points_cb = CheckBox(self.canvas, x=135, y=25, width=50, height=50)
        self.draw_points_label = Label(self.canvas, 25, 0, fg_color=pg.Color("white"), text="Draw Points")
        self.draw_joints_label = Label(self.canvas, 350, 0, fg_color=pg.Color("white"),
                                       text="Draw springs, click with right button to stop")
        self.use_fixed_points_cb = CheckBox(self.canvas, x=135, y=125, width=50, height=50)
        self.use_fixed_points_label = Label(self.canvas, 25, 100, fg_color=pg.Color("white"), text="Fix point")
        self.start_simulation = CheckBox(self.canvas, x=135, y=75, width=50, height=50)
        self.start_simulation_label = Label(self.canvas, 25, 50, fg_color=pg.Color("white"), text="Start simulation")
        self.info_label1 = Label(self.canvas, x=750, y=100, fg_color=pg.Color("green"),
                                 text="tip: 'Fix point' makes a ball ignore gravity (and any other force), press W to spawn a pentagon!")
        self.stiffness_slider = Slider(self.canvas, center=(1000, 25), width=400, height=20, bg_color=(0, 0, 0),
                                       fg_color=pg.Color("white"), start=10, end=110, default=100)
        self.stiffness_text1 = Label(self.canvas, x=715, y=13, height=20, fg_color=pg.Color("white"), text="Springy")
        self.stiffness_text2 = Label(self.canvas, x=1175, y=13, height=20, fg_color=pg.Color("white"), text="Stiff")
        self.stiffness_text3 = Label(self.canvas, x=950, y=25, height=20, fg_color=pg.Color("white"),
                                     text="Spring stiffness")

        self.UI.extend([self.draw_points_label, self.draw_points_cb, self.draw_joints_label,
                        self.start_simulation_label, self.start_simulation, self.use_fixed_points_cb,
                        self.use_fixed_points_label, self.info_label1, self.stiffness_slider,
                        self.stiffness_text1, self.stiffness_text2, self.stiffness_text3])

    def update(self, dt: float):
        """
        The update function simulates the 'dt' time step progression. It thus updates the physics of the space and
        all the UI elements.
        :param dt: the time step
        :return: None
        """
        super().update(dt)
        print([spring.rest_length for spring in self.springs])
        if self.game.jumped == -1:
            vertices, bodies, shapes, springs = pentagon(self.game.mousepos[0], self.game.mousepos[1], 200)
            self.springs.extend(springs)
            for i in range(len(bodies)):
                self.balls.append((bodies[i], shapes[i]))
        if self.draw_points_cb.ticked:
            # SX click handling
            # not any(...) is made to prevent unintentional ball placings on UI elements.
            if self.game.clicked_sx == -1 and not any(
                    uielement.rect.collidepoint(self.game.mousepos) for uielement in self.UI):
                x, y = self.game.mousepos
                if self.use_fixed_points_cb.ticked:
                    self.balls.append(add_fixed_ball(x, y))
                else:
                    self.balls.append(add_ball(x, y))
        else:
            if self.game.clicked_sx == -1:
                for ball, circle in self.balls:
                    if ball.position.get_dist_sqrd(self.game.mousepos) <= circle.radius ** 2:
                        self._stop_poly = False
                        self._poly.append(ball)
                    print(self._poly)
                    if len(self._poly) > 1:
                        self.springs.append(
                            add_spring(self._poly[-2], self._poly[-1], stiffness=self.stiffness_slider.value))
            if self.game.clicked_dx == -1:
                self._stop_poly = True
                self._poly = []
        if self.start_simulation.ticked:
            space.step(dt)

    def render(self, surface: pg.Surface):
        super().render(surface)
        for wall in self.walls:
            pg.draw.rect(surface, pg.Color("white"), wall)
        for ball in self.balls:
            if ball[0].body_type == pm.Body.DYNAMIC:
                pg.draw.circle(surface, pg.Color("white"), ball[0].position, ball[1].radius)
            else:
                pg.draw.circle(surface, pg.Color("red"), ball[0].position, ball[1].radius)
        if len(self.springs) > 0:
            for spring in self.springs:
                pg.draw.line(surface, pg.Color("red"), spring.a.position, spring.b.position)
        if not self._stop_poly and len(self._poly) > 0:
            pg.draw.line(surface, pg.Color("red"), self._poly[-1].position, self.game.mousepos)

    def load_geometry(self):
        self.walls = [add_wall(pg.Rect((25, 750), (1550, 50))),
                      add_wall(pg.Rect((25, 450), (25, 300))),
                      add_wall(pg.Rect((1550, 450), (25, 300)))]
