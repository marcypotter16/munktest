import os.path

import pygame

from Entities.Entity import StaticEntity
from Entities.Player import Player, TestPlayer
from Entities.World import World
from Game import Game


def read_map(path: str, game: Game, frame_rect: pygame.Rect, tilesize: tuple[int, int]) -> tuple[
    World, Player]:
    with open(path, 'r') as f:
        lines = f.readlines()
        d = {}
        world = World()
        for y, line in enumerate(lines):
            for x, char in enumerate(line.split()):
                if int(char) == 1:
                    rect = pygame.Rect((frame_rect.x + x * tilesize[0], frame_rect.y + y * tilesize[0]), tilesize)
                    ent = StaticEntity(game, rect, layer=World.BLOCKING, type='blocking')
                    image = pygame.image.load(os.path.join(game.base_dir, 'Assets/map/erbafunghi.png')).convert()
                    ent.image = pygame.transform.smoothscale(image, tilesize)
                    d[(x, y)] = ent
                    world.add(ent)
                if int(char) == 2:
                    rect = pygame.Rect((frame_rect.x + x * tilesize[0], frame_rect.y + y * tilesize[0]), tilesize)
                    ent = StaticEntity(game, rect, layer=World.BLOCKING, type='blocking')
                    image = pygame.image.load(os.path.join(game.base_dir, 'Assets/map/terra.png')).convert()
                    ent.image = pygame.transform.smoothscale(image, tilesize)
                    d[(x, y)] = ent
                    world.add(ent)
                if int(char) == 9:
                    rect_player = pygame.Rect((frame_rect.x + x * tilesize[0], frame_rect.y + y * tilesize[0]),
                                              tilesize)
        dir_player = os.path.join(os.path.join(game.assets_dir, "sprites"), "player")
        anim_dict = {'idle': os.path.join(dir_player, 'idle.png'), 'running': os.path.join(dir_player, 'running.png')}
        p = Player(game, rect_player, world, animations_paths=anim_dict)
        return world, p


def read_map_and_scale(path: str, game: Game, frame_rect: pygame.Rect) -> \
        tuple[World, Player]:
    with open(path, 'r') as f:
        lines = f.readlines()
        d = {}
        world = World()
        tilesize_x = round(float(frame_rect.width) / len(lines[0].split()))
        tilesize_y = round(float(frame_rect.height) / len(lines))
        tilesize = (tilesize_x, tilesize_y)
        for y, line in enumerate(lines):
            for x, char in enumerate(line.split()):
                if int(char) == 1:
                    rect = pygame.Rect((frame_rect.x + x * tilesize[0], frame_rect.y + y * tilesize[0]), tilesize)
                    ent = StaticEntity(game, rect, layer=World.BLOCKING, type='blocking')
                    image = pygame.image.load(os.path.join(game.base_dir, 'Assets/map/erbafunghi.png')).convert()
                    ent.image = pygame.transform.smoothscale(image, tilesize)
                    d[(x, y)] = ent
                    world.add(ent)
                if int(char) == 9:
                    rect_player = pygame.Rect((frame_rect.x + x * tilesize[0], frame_rect.y + y * tilesize[0]),
                                              tilesize)
        p = Player(game, rect_player, world)
        return world, p


def read_map_simple(path: str, game: Game, frame_rect: pygame.Rect, tilesize: tuple[int, int]):
    with open(path, 'r') as f:
        lines = f.readlines()
        d = {}
        world = World()
        for y, line in enumerate(lines):
            for x, char in enumerate(line.split()):
                rect = pygame.Rect((frame_rect.x + x * tilesize[0], frame_rect.y + y * tilesize[1]), tilesize)
                if int(char) == 1:
                    ent = StaticEntity(game, rect, layer=World.BLOCKING, type='blocking')
                    image = pygame.Surface(tilesize)
                    pygame.draw.rect(image, color=pygame.Color("white"), rect=pygame.Rect((0, 0), rect.size))
                    ent.image = image
                    d[(x, y)] = ent
                    world.add(ent)
                if int(char) == 2:
                    ent = StaticEntity(game, rect, layer=World.BLOCKING, type='blocking')
                    image = pygame.Surface(rect.size)
                    pygame.draw.rect(image, color=pygame.Color("grey"), rect=pygame.Rect((0, 0), rect.size))
                    ent.image = image
                    d[(x, y)] = ent
                    world.add(ent)
                if int(char) == 9:
                    p = TestPlayer(game, rect, world)

        return world, p


if __name__ == '__main__':
    g = Game(basedir='/home/marcello/PycharmProjects/Platformer/')
    print(read_map(os.path.join(g.base_dir, 'Assets/map/map.txt'), g, tilesize=(16, 16)))
