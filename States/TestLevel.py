import os.path

import pygame

from Entities.Player import Player
from Entities.World import World
from Game import Game
from States.State import State
from UI.Abstract import UICanvas, UIContainer
from UI.Button import TextButton


class TestLevel(State):
    def __init__(self, game: Game, world: World, player: Player):
        super().__init__(game=game)
        self.player = player
        # todo: To be modified
        # anim_dir = os.path.join(self.game.base_dir, 'Assets/sprites/player/')
        # idle_animations_names = [name for name in os.listdir(anim_dir) if 'front' in name]
        # idle_animations = []
        # for an in idle_animations_names:
        #     sprite = pygame.image.load(os.path.join(anim_dir, an))
        #     idle_animations.append(pygame.transform.smoothscale(sprite, (60, 60)))
        # anim_dict = {'idle': idle_animations}
        # self.player.animations['idle'] = idle_animations
        # self.player.set_current_animation_frame(idle_animations[0])


        self.world = world
        self.load_ui()

    def update(self, delta_time):
        for ui in self.UI:
            ui.update(delta_time)
        self.player.update(delta_time)

    def render(self, surface: pygame.Surface):
        for el in self.UI:
            el.render(surface)
        self.world.render(surface)
        self.player.render(surface)

    def load_ui(self):
        canvas = UICanvas(self.game)
        gw, gh = self.game.screen_size
        container = UIContainer(parent=canvas, width=gw, height=gh, bg_color=(0, 0, 0, 200), corner_radius=0)

        ### Colors ###
        white = (255, 255, 255)
        hc = (77, 209, 26, 150)

        back_btn = TextButton(parent=container, x=10, y=10, width=50, height=30, bg_color='transparent',
                              fg_color=white, text='<-', command=lambda: self.game.state_stack.pop(), hover_color=hc)

        self.UI.append(canvas)
