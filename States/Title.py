import math
import os.path
import random

import pygame

from Entities.Player import Player
from States.GameSettings import GameSettings
from States.State import State
from States.TestLevel import TestLevel
from UI.Button import TextButton, ImageButton
from UI.Label import Label
from UI.Abstract import UICanvas
from Utils import Map


class Title(State):
    def __init__(self, game):
        super().__init__(game)
        # self.is_static_ui = False
        # self.is_non_static_ui = True
        # self.needs_text_entry = False
        self.settings_button_animation = None
        self.bg_image = None
        self._last_played_piece_name = None
        self._menu_sound_dir = None
        self.final_boss_piece = None
        self.title_label: Label = None
        self.__title_original_y_position: float = 0
        self.load_sounds()
        self.load_necessary_sprites()
        self.load_background()
        self.load_ui()
        self.__omega = 2  # Angular speed
        self.__t = 0  # Time
        self.__vertical_oscillation = 10

    def update(self, delta_time):
        super().update(delta_time)
        self.title_label.y = self.__title_original_y_position + math.sin(
            self.__omega * self.__t) * self.__vertical_oscillation
        self.title_label.rect.y = self.title_label.y
        self.__t += delta_time
        if self.__t >= math.tau:
            self.__t = 0

    def render(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
        surface.blit(self.bg_image, self.bg_image.get_rect())
        # rect = self.girl_image.get_rect()
        # rect.topleft = (100, self.game.GAME_H - 250)
        # surface.blit(self.girl_image, rect)
        for ui_element in self.UI:
            ui_element.render(surface)

    def load_ui(self):
        canvas = UICanvas(self.game)
        # gh, gw = self.game.GAME_H, self.game.GAME_W
        gw, gh = self.game.screen_size
        white = (255, 255, 255)
        hc = (77, 209, 26, 150)
        print(self.game.screen_size)
        self.title_label = Label(parent=canvas, x=500, y=100, width=400, height=50, fg_color=white,
                                 text="Title")
        self.__title_original_y_position = self.title_label.y
        self.UI.append(canvas)
        switch_piece_button = TextButton(parent=canvas, x=600, y=gh - 60, width=300, height=40, text="Cambia pezzo",
                                         bg_color="transparent", fg_color=white, command=self.switch_piece,
                                         hover_color=hc)
        settings_btn = ImageButton(parent=canvas, x=.965 * gw, y=.02 * gh, width=40, height=40, bg_color="transparent",
                                   command=self.goto_settings, hover_color=hc,
                                   animation=self.settings_button_animation, animation_fps=60)
        map_dimension = pygame.Rect(round(.5*(gw-23*64)), round(.5*(gh-10*64)), 23*64, 10*64)
        print(map_dimension)
        world, player = Map.read_map(os.path.join(self.game.base_dir, 'Assets/map/map.txt'), self.game, frame_rect=map_dimension, tilesize=(64, 64))

        play_btn = TextButton(parent=canvas, x=600, y=gh - 120, width=300, height=40, text="Gioca",
                              bg_color="transparent", fg_color=white, command=lambda: self.game.state_stack.push(TestLevel(self.game, world, player)),
                              hover_color=hc)

    def switch_piece(self):
        pygame.mixer.music.fadeout(3000)

        def get_next_piece() -> str:
            files = os.listdir(self._menu_sound_dir)
            index = files.index(self.last_played_piece_name)
            new_index = (index + 1) % len(files)
            self.last_played_piece_name = files[new_index]
            return files[new_index]

        pygame.mixer.music.load(os.path.join(self._menu_sound_dir, get_next_piece()))
        pygame.mixer.music.play()

    def goto_settings(self):
        print("HASDHUASDH")
        self.game.state_stack.push(GameSettings(self.game))

    def load_sounds(self):
        # self.main_menu_piece = pygame.mixer.Sound(os.path.join(self.game.base_dir, 'Assets/sound/main menu.wav'))
        # self.final_boss_piece = pygame.mixer.Sound(os.path.join(self.game.base_dir, 'Assets/sound/final boss.wav'))
        pygame.mixer.music.load(os.path.join(self.game.base_dir, 'Assets/sound/main menu.wav'))
        pygame.mixer.music.set_volume(float(self.game.settings['music_volume']) / 100)
        self._menu_sound_dir = os.path.join(self.game.base_dir, 'Assets/sound')
        self.last_played_piece_name = "main menu.wav"
        pygame.mixer.music.play()

    def load_background(self):
        image = pygame.image.load(os.path.join(self.game.base_dir, 'Assets/art/title/sunset.png')).convert_alpha()
        self.bg_image = pygame.transform.smoothscale(image, self.game.screen_size)
        # self.girl_image = pygame.image.load(os.path.join(self.game.base_dir, 'Assets/art/title/black girl.png'))

    def load_necessary_sprites(self):
        path = os.path.join(self.game.sprite_dir, 'ui', 'settings_button')
        settings_button_dir = os.listdir(path)
        settings_button_filenames = [os.path.join(path, filename) for
                                     filename in settings_button_dir]
        self.settings_button_animation = [pygame.image.load(img) for img in settings_button_filenames]
