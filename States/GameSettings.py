import json
import os.path

import pygame

from Game import Game
from States.State import State
from UI.Button import TextButton
from UI.Label import Label
from UI.Menu import Menu
from UI.Abstract import UICanvas, UIContainer
from UI.Slider import Slider
from UI.TabsFrame import TabsFrame
from UI.CheckBox import CheckBox


class GameSettings(State):
    def __init__(self, game):
        super().__init__(game=game)
        self.is_static_ui = True
        self.is_non_static_ui = False
        self.needs_text_entry = False
        self.load_ui()

    def load_ui(self):
        canvas = UICanvas(self.game)
        gw, gh = self.game.screen_size
        container = UIContainer(parent=canvas, width=gw, height=gh, bg_color=(0, 0, 0, 50), corner_radius=0)
        general_tab = UIContainer(parent=container)
        sound_tab = UIContainer(parent=container)
        tabs = {'general': general_tab, 'sound': sound_tab}

        ### Colors ###
        white = (255, 255, 255)
        hc = (77, 209, 26, 150)

        ### Save and Back buttons ###
        save_btn = TextButton(parent=container, x=600, y=gh - 60, width=300, height=50, bg_color='transparent',
                              fg_color=white, text="Save", command=self.save_settings, hover_color=hc)
        back_btn = TextButton(parent=container, x=10, y=10, width=50, height=30, bg_color='transparent',
                              fg_color=white, text='<-', command=lambda: self.game.state_stack.pop(), hover_color=hc)

        frame = TabsFrame(parent=container, x=50, y=50, width=gw - 100, height=gh - 100, bg_color=(0, 0, 0, 50),
                          fg_color=(255, 255, 255), button_hover_color=hc, corner_radius=20, tabs=tabs)
        ### --- ###

        ### General settings tab ###
        fps_label = Label(parent=general_tab, x=100, y=150, width=300, height=50, fg_color=(255, 255, 255), text="FPS")
        self.fps_menu = Menu(parent=general_tab, x=100, y=200, width=300, height=50, default=str(self.game.settings['fps']),
                             options=['30', '60', '120', '144', '360'], bg_color=(200, 200, 200))
        screen_size_label = Label(parent=general_tab, x=600, y=150, width=300, height=50, fg_color=(255, 255, 255), text="Screen Size")
        screen_size = f"{gw}x{gh}"
        self.screen_size_menu = Menu(parent=general_tab, x=600, y=200, width=300, height=50, default=screen_size,
                             options=['800x600', '1024x768', '1280x720', '1600x800', '1600x900', '1920x1080'], bg_color=(200, 200, 200))
        fullscreen_label = Label(parent=general_tab, x=1000, y=150, width=300, height=50, fg_color=(255, 255, 255), text='Fullscreen')
        self.fullscreen_checkbox = CheckBox(parent=general_tab, x=1300, y=140, width=100, height=80, default=self.game.settings['fullscreen'])
        ### --- ###

        ### Sound settings tab ###
        self.music_volume_slider = Slider(parent=sound_tab, x=500, y=150, width=400, height=50,
                                          bg_color='transparent', fg_color=(255, 255, 255),
                                          default=self.game.settings['music_volume'])
        music_volume_label = Label(parent=sound_tab, x=100,
                                   y=self.music_volume_slider.y - .5 * self.music_volume_slider.height, width=350,
                                   fg_color=(255, 255, 255), text='Music Volume:')
        self.sfx_volume_slider = Slider(parent=sound_tab, x=500, y=250, width=400, height=50,
                                        bg_color='transparent', fg_color=(255, 255, 255),
                                        default=self.game.settings['sfx_volume'])
        sfx_volume_label = Label(parent=sound_tab, x=100,
                                 y=self.sfx_volume_slider.y - .5 * self.music_volume_slider.height,
                                 width=350,
                                 fg_color=(255, 255, 255), text='Sfx Volume:')
        ### --- ###

        self.UI.append(canvas)

    def save_settings(self):
        self.game.settings['fps'] = int(self.fps_menu.selected_option)
        self.game.settings['music_volume'] = round(self.music_volume_slider.value)
        self.game.settings['screen_w'] = int(self.screen_size_menu.selected_option.split('x')[0])
        self.game.settings['screen_h'] = int(self.screen_size_menu.selected_option.split('x')[1])
        self.game.screen_size = (self.game.settings['screen_w'], self.game.settings['screen_h'])
        self.game.settings['fullscreen'] = 1 if self.fullscreen_checkbox.ticked else 0
        if self.game.settings['fullscreen']:
            self.game.screen = pygame.display.set_mode(self.game.screen_size, pygame.FULLSCREEN)
        else:
            self.game.screen = pygame.display.set_mode(self.game.screen_size)
        print('saving...')
        with open(os.path.join(self.game.base_dir, 'settings.txt'), 'w') as f:
            json.dump(self.game.settings, f)

    def render(self, surface: pygame.Surface):
        for ui_element in self.UI:
            ui_element.render(surface)

    def update(self, delta_time):
        pygame.mixer.music.set_volume(.01 * self.music_volume_slider.value)
        for ui_element in self.UI:
            ui_element.update(delta_time)


if __name__ == '__main__':
    g = Game()
    g.state_stack.push(GameSettings(g))
