import os

import pygame.image

from UI.Abstract import UIElement, UICanvas
from Utils import Image


class CheckBox(UIElement):
    def __init__(self, parent: UICanvas = None, x=0, y=0, center=None, width=50, height=50, bg_color: tuple | str = 'transparent',
                 fg_color=(0, 0, 0), text: str = "", corner_radius=10,
                 default: bool = False):
        super().__init__(parent, x, y, center, width, height, bg_color, fg_color, text, corner_radius)
        false_image, true_image = Image.images_from_spritesheet(os.path.join(self.game.sprite_dir, 'ui/switch.png'), (64, 40))
        self.true_image = pygame.transform.smoothscale(true_image, (width, height))
        self.false_image = pygame.transform.smoothscale(false_image, (width, height))
        self.current_image = self.true_image if default else self.false_image
        self.ticked = default

    def update(self, dt):
        if self.visible:
            if self.game.clicked_sx == -1:
                if self.rect.collidepoint(self.game.mousepos):
                    self.ticked = not self.ticked
                    print(self.ticked)
                    self.current_image = self.true_image if self.ticked else self.false_image

    def render(self, surface: pygame.Surface):
        if self.visible:
            surface.blit(self.current_image, self.rect)
