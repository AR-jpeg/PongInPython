from typing import Any, Callable, List, Tuple
import pygame

from pygame import Surface


class Button(pygame.Rect):
    def __init__(
        self,
        left: int,
        top: int,
        on_click: Callable,
        on_click_args: List[Any],
        text: Surface,
    ):
        self.left = left
        self.top = top
        self.width = text.get_width()
        self.height = text.get_height()
        self.on_click = on_click
        self.on_click_args = on_click_args

        self.text = text

        super().__init__(self.left, self.top, self.width, self.height)

    def draw(self, window: pygame.surface.Surface):
        pygame.draw.rect(window, (50, 50, 50), self)
        # Draw the text in the center of the button
        window.blit(
            self.text,
            (
                self.left + (self.width / 2) - (self.text.get_width() / 2),
                self.top + (self.height / 2) - (self.text.get_height() / 2),
            ),
        )

    def clicked(self, mouse_pos: Tuple[float, float]):
        if self.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.on_click(*self.on_click_args)  # type: ignore
            return True

        return False
