from typing import Sequence

import pygame

from src.ball import Ball
from src.button import Button
from src.paddle import Paddle
from src.utils import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

pygame.display.set_caption("Pong in Pygame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PAD_WIDTH, PAD_HEIGHT = 15, 90
PADDLE_VELOCITY = 5

BALL_X_VELOCITY = 6
BALL_Y_VELOCITY = 4

CREATE_NEW_GAME_FONT = pygame.font.SysFont("monospace", 25, bold=True)
SCORE_FONT = pygame.font.SysFont("monospace", 30, bold=True)

PONG_LOGO_IMAGE = pygame.transform.scale(
    pygame.image.load("assets/pong_logo.png"), (64 * 6, 64 * 6)
)


def draw_window(left: Paddle, right: Paddle, ball: Ball, scores: Sequence[int]):
    WIN.fill(BLACK)

    # Draw the border between the two paddles
    draw_dashed_line(WIN, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 3, 10)  # type: ignore

    # Draw the paddles
    left.draw(WIN)
    right.draw(WIN)

    ball.draw(WIN)

    # Draw the score
    current_score_text_for_left = SCORE_FONT.render(
        f"Current Score: {scores[1]}", True, WHITE
    )
    current_score_text_for_right = SCORE_FONT.render(
        f"Current Score: {scores[0]}", True, WHITE
    )

    WIN.blit(
        current_score_text_for_left,
        (20, 20),
    )

    WIN.blit(
        current_score_text_for_right,
        (WIDTH - current_score_text_for_right.get_width(), 20),
    )

    # Draw a button to go back to the home screen
    back_to_home_screen_text = CREATE_NEW_GAME_FONT.render(
        "Back to Home Screen", True, WHITE
    )
    back_to_home_screen_button = Button(
        WIDTH - back_to_home_screen_text.get_width() - 20,
        HEIGHT - back_to_home_screen_text.get_height() - 20,
        home_screen,
        [],
        back_to_home_screen_text,
    )
    back_to_home_screen_button.draw(WIN)
    back_to_home_screen_button.clicked(pygame.mouse.get_pos())

    pygame.display.update()


def handle_paddle_movement(
    left: Paddle,
    right: Paddle,
    ball: Ball,
    keys_pressed: Sequence[bool],
    playing_with_computer: bool,
):
    if playing_with_computer:
        # Handle the ai's movement
        if ball.x < WIDTH / 2 + 50:
            if ball.y < left.y and left.top > 0:
                left.y -= PADDLE_VELOCITY
            elif ball.y > left.y and left.bottom < HEIGHT:
                left.y += PADDLE_VELOCITY
    else:
        # Handle the left paddle's movement
        if keys_pressed[pygame.K_w] and left.top > 0:
            left.y -= PADDLE_VELOCITY
        elif keys_pressed[pygame.K_s] and left.bottom < HEIGHT:
            left.y += PADDLE_VELOCITY

    # Handle the right paddle's movement
    if keys_pressed[pygame.K_UP] and right.top > 0:
        right.y -= PADDLE_VELOCITY
    elif keys_pressed[pygame.K_DOWN] and right.bottom < HEIGHT:
        right.y += PADDLE_VELOCITY


def home_screen():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WIN.fill(BLACK)
        WIN.blit(PONG_LOGO_IMAGE, (WIDTH // 2 - PONG_LOGO_IMAGE.get_width() // 2, 0))

        start_game_with_computer_text = CREATE_NEW_GAME_FONT.render(
            "Play with a computer", True, WHITE
        )
        start_game_with_computer_button = Button(
            WIDTH // 8 - 40,
            HEIGHT // 2 + 100,
            main,
            [True],
            start_game_with_computer_text,
        )

        start_game_with_two_players_text = CREATE_NEW_GAME_FONT.render(
            "Play with a friend", True, WHITE
        )
        start_game_with_two_players_button = Button(
            WIDTH // 8 + 350,
            HEIGHT // 2 + 100,
            main,
            [False],
            start_game_with_two_players_text,
        )

        start_game_with_computer_button.draw(WIN)
        start_game_with_computer_button.clicked(pygame.mouse.get_pos())

        start_game_with_two_players_button.draw(WIN)
        start_game_with_two_players_button.clicked(pygame.mouse.get_pos())

        pygame.display.update()

    pygame.quit()


def main(play_with_computer: bool = True):

    run = True

    left_paddle = Paddle(50, HEIGHT / 2 - PAD_HEIGHT / 2, PAD_WIDTH, PAD_HEIGHT)
    right_paddle = Paddle(
        WIDTH - 50, HEIGHT / 2 - PAD_HEIGHT / 2, PAD_WIDTH, PAD_HEIGHT
    )

    ball = Ball(WIDTH / 2 - 5, HEIGHT / 2 - 5, 10, BALL_Y_VELOCITY, BALL_X_VELOCITY)

    scores = [0, 0]

    while run:
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Check if the ball collided with the wall, along the x-axis
        if ball.move_ball((left_paddle, right_paddle)):
            if ball.x > WIDTH / 2:
                scores[1] += 1
            else:
                scores[0] += 1

        keys_pressed = pygame.key.get_pressed()

        handle_paddle_movement(
            left_paddle, right_paddle, ball, keys_pressed, play_with_computer
        )
        draw_window(left_paddle, right_paddle, ball, scores)

    pygame.quit()


if __name__ == "__main__":
    try:
        home_screen()
    except pygame.error:
        print("Quitting the game")
        pygame.quit()
