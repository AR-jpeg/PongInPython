import pygame


class Paddle(pygame.Rect):
    def __init__(
        self, left: int, top: int, width: int, height: int, *args, **kwargs
    ) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        super().__init__(self.left, self.top, self.width, self.height, *args, **kwargs)

    def draw(self, window: pygame.surface.Surface):
        pygame.draw.rect(window, (255, 255, 255), self)
