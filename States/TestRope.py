import os

from Entities.Rope import Rope
from Entities.World import World
from Game import Game
from pygame import Vector2, Surface, Rect
from States.State import State
from Utils import Map


class TestRope(State):
    def __init__(self, game: Game):
        super().__init__(game)
        gss = game.screen_size
        tilesize = (round(float(gss[0]) / 20), round(float(gss[1]) / 20))
        self.world, self.player = Map.read_map_simple(os.path.join(game.base_dir, 'Test/RopeTestMap.txt'), game, Rect((0, 0), gss), tilesize=tilesize)
        # self.rope = Rope(game, self.world, Vector2(100, 100), Vector2(400, 100), b_fixed=False, num_punti=50)
        self.rope = None

    def update(self, delta_time):
        if self.game.clicked_sx == 1:
            self.rope = Rope(self.game, self.world, Vector2(self.player.rect.center), Vector2(self.game.mousepos), a_fixed=False, num_punti=50)
            self.player.roped = True

        if self.game.clicked_dx == -1:
            self.rope = None
            self.player.roped = False

        self.player.update(delta_time)

        if self.player.roped:
            self.rope.update(delta_time)
            self.player.rect.center = self.rope.a.pos

        # self.rope.a.pos = Vector2(self.player.rect.center)


    def render(self, surface: Surface):
        super().render(surface)
        self.world.render(surface)
        if self.player.roped:
            self.rope.render(surface)
        self.player.render(surface)

if __name__ == '__main__':
    # g = Game('C:\\Users\\marcy\\PycharmProjects\\CHOMP\\')
    g = Game('/home/marcello/PycharmProjects/Platformer')
    g.state_stack.push(TestRope(g))
    g.slomo_factor = 1

    g.game_loop()

