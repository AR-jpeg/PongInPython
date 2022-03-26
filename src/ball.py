from typing import Sequence
import pygame

from src.paddle import Paddle
from src.sounds import HIT_WALL_SOUND, PADDLE_HIT_SOUND


class Ball(pygame.Rect):
    def __init__(
        self, left: int, top: int, radius: int = 5, y_velocity=5, x_velocity=5
    ) -> None:
        self.left = left
        self.top = top
        self.radius = radius

        self.y_velocity = y_velocity
        self.x_velocity = x_velocity

        super().__init__(self.left, self.top, self.radius, self.radius)

    def move_ball(self, paddles: Sequence[Paddle]):
        lost_a_point = False

        if (self.y <= 0) or (self.bottom >= 500):
            self.y_velocity *= -1

        # Check if the ball collided with the either or the two paddles
        for paddle in paddles:
            if self.colliderect(paddle):
                PADDLE_HIT_SOUND.play()
                self.x_velocity *= -1
                break

        if (self.x <= 0) or (self.right >= 800):
            self.x_velocity *= -1
            HIT_WALL_SOUND.play()
            lost_a_point = True

        self.y += self.y_velocity
        self.x += self.x_velocity

        return lost_a_point

    def draw(self, win: pygame.surface.Surface):
        pygame.draw.circle(win, (255, 255, 255), (self.left, self.top), self.radius)
