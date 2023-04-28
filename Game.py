import os
import pygame as p
import time

from Generic.Stack import Stack

clock = p.time.Clock()


class Game:
    def __init__(self, basedir=None):
        self.need_key_event_handling = True
        self.events = None
        self.base_dir = os.getcwd() if not basedir else basedir
        self.font_dir = None
        self.assets_dir = None
        self.font = None  # This has to be set!
        self.title_screen = None
        p.init()
        p.mixer.init()
        # self.GAME_W, self.GAME_H = 640, 320
        self.GAME_W, self.GAME_H = 1600, 800
        self.game_canvas = p.Surface((self.GAME_W, self.GAME_H))
        p.display.set_caption('CHOMP')

        ### World ###

        ### --- ###

        ### Actions ###
        self.running, self.playing = True, True
        self.actions: dict[str, int] = {'left': 0, 'right': 0, 'up': 0, 'jump': 0, 'down': 0, 'action1': 0,
                                        'glide': 0, 'start': 0, 'mouse_sx': 0, 'mouse_dx': 0, 'shift': 0}
        self.jumped: int = 0
        self.clicked_sx: int = 0
        self.clicked_dx: int = 0
        ### --- ###self.on_ground = True

        ### Settings ###
        self.settings: dict[str, int] = {'fps': 30, 'music_volume': 50, 'sfx_volume': 30, 'screen_h': 800,
                                         'screen_w': 1600, 'fullscreen': 0}
        self.screen_size = (self.settings['screen_w'], self.settings['screen_h'])
        if self.settings['fullscreen']:
            self.screen = p.display.set_mode(self.screen_size, p.FULLSCREEN)
        else:
            self.screen = p.display.set_mode(self.screen_size)
        ### --- ###

        self.slomo_factor: float = 1.0 # if > 1 game accelerates
        self.dt, self.prev_time = 0, time.time()
        self.now: float = 0
        self.state_stack = Stack()
        self.mousepos = None
        self.load_assets()

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
            clock.tick(self.settings['fps'])

    def get_events(self):
        # if self.state_stack.top().is_static_ui:
        #     p.event.wait()

        self.events = p.event.get()
        aux_prev_jump_action = self.actions['jump']
        aux_prev_mouse_sx = self.actions['mouse_sx']
        aux_prev_mouse_dx = self.actions['mouse_dx']
        aux_prev_d = self.actions['right']
        aux_prev_a = self.actions['left']
        aux_shift = self.actions['shift']
        for event in self.events:
            if event.type == p.QUIT:
                self.playing, self.running = False, False

            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.actions['mouse_sx'] = 1
                    self.actions['shift'] = 1
                if event.button == 3:
                    self.actions['mouse_dx'] = 1

            if event.type == p.MOUSEBUTTONUP:
                if event.button == 1:
                    self.actions['mouse_sx'] = 0
                    self.actions['shift'] = 0
                if event.button == 3:
                    self.actions['mouse_dx'] = 0

            if self.need_key_event_handling:
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        self.playing, self.running = False, False
                    if event.key == p.K_a:
                        self.actions['left'] = 1
                    if event.key == p.K_d:
                        print('RIGHT!!')
                        self.actions['right'] = 1
                    if event.key == p.K_s:
                        self.actions['down'] = 1
                    if event.key == p.K_w:
                        self.actions['up'] = 1
                        self.actions['jump'] = 1
                    if event.key == p.K_LSHIFT:
                        self.actions['shift'] = 1
                    if event.key == p.K_1:
                        self.actions['action1'] = 1
                    if event.key == p.K_SPACE:
                        self.actions['glide'] = 1
                    if event.key == p.K_3:
                        self.actions['start'] = 1
                if event.type == p.KEYUP:
                    if event.key == p.K_a:
                        self.actions['left'] = 0
                    if event.key == p.K_d:
                        self.actions['right'] = 0
                    if event.key == p.K_s:
                        self.actions['down'] = 0
                    if event.key == p.K_w:
                        self.actions['up'] = 0
                        self.actions['jump'] = 0
                        self.actions['down'] = 0
                    if event.key == p.K_1:
                        self.actions['action1'] = 0
                    if event.key == p.K_SPACE:
                        self.actions['glide'] = 0
                    if event.key == p.K_LSHIFT:
                        self.actions['shift'] = 0
                    if event.key == p.K_3:
                        self.actions['start'] = 0
        self.jumped = self.actions['jump'] - aux_prev_jump_action
        self.clicked_sx = self.actions['mouse_sx'] - aux_prev_mouse_sx
        self.clicked_dx = self.actions['mouse_dx'] - aux_prev_mouse_dx
        self.pushed_d = self.actions['right'] - aux_prev_d
        self.pushed_a = self.actions['left'] - aux_prev_a
        self.pushed_shift = self.actions['shift'] - aux_shift
        # print(self.jumped)

    def update(self):
        # self.mousepos = (
        #     p.mouse.get_pos()[0] * self.GAME_W / self.settings['screen_w'],
        #     p.mouse.get_pos()[1] * self.GAME_H / self.settings['screen_h'])
        self.mousepos = p.mouse.get_pos()
        # self.state_stack.top().update(self.dt, self.actions)
        self.state_stack.top().update(self.dt)

    def render(self):
        self.state_stack.top().render(self.game_canvas)
        self.screen.blit(p.transform.scale(self.game_canvas, self.screen_size), (0, 0))
        p.display.flip()  # ??

    def get_dt(self):
        self.now = time.time()
        self.dt = (self.now - self.prev_time) * self.slomo_factor
        self.prev_time = self.now

    def load_assets(self):
        self.assets_dir = os.path.join(self.base_dir, "Assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "font")
        # self.font = p.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20)
        self.font = p.font.SysFont("Roboto", 15, bold=True)


    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.game_loop()
