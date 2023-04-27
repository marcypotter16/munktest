import pymunk as pm
import pygame as pg
from UI.CheckBox import *
from munktest.States.State import State
from munktest.UI.Abstract import UICanvas
from munktest.UI.Label import Label


class ShapeCreator(State):
    def __init__(self, game):
        super().__init__(game)
        self.canvas = UICanvas(game=game)
        self.draw_poly_cb = CheckBox(self.canvas, x=45, y=25, width=50, height=50)
        self.draw_poly_label = Label(self.canvas, 25, 25, fg_color=pg.Color("white"), text="Draw")
        self.UI.extend([self.draw_poly_label, self.draw_poly_cb])

    def update(self, dt: float):
        super().update(dt)
        pass

    def render(self, surface: pg.Surface):
        super().render(surface)
        pass
