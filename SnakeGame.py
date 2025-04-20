import pygame
import random
import sys
import time

# initialization
pygame.init()

# window setup
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# colours setup
GREEN = (0, 255, 0)  # snake
RED = (255, 0, 0)    # food
BLACK = (0, 0, 0)    # background
WHITE = (255, 255, 255)

# font setup
font = pygame.font.SysFont(None, 35)

def draw_text(text, color, y_offset = 0, align_left = True):
    rendered = font.render(text, True, color)
    if align_left:
        rect = rendered.get_rect(topleft = (150, HEIGHT // 2 + y_offset))
    else:
        rect = rendered.get_rect(center = (WIDTH // 2, HEIGHT // 2 + y_offset))
    win.blit(rendered, rect)

def draw_menu():
    win.fill(BLACK)
    draw_text("Welcome to Snake Game !", WHITE, -60, False)
    draw_text(" [1] - Level 1: Simple", WHITE, 0)
    draw_text(" [2] - Level 2: Challenge", WHITE, 30)
    draw_text(" [Q] - Quit", WHITE, 60)
    pygame.display.update()

def draw_game_over(score, seconds):
    win.fill(BLACK)
    draw_text("Game Over!", WHITE, -90, False)
    draw_text(f"Score: {score}", WHITE, -30)
    draw_text(f"Timeused: {seconds:.1f} s", WHITE, 0)
    draw_text("[R] - Restart", WHITE, 60)
    draw_text("[Q] - Quit", WHITE, 90)
    pygame.display.update()

def game_loop(speed):
    snake = [(100, 100)]
    direction = (BLOCK_SIZE, 0)
    food = get_random_food(snake)
    clock = pygame.time.Clock()
    score = 0
    start_time = time.time()

    running = True
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # check direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != (BLOCK_SIZE, 0):
            direction = (-BLOCK_SIZE, 0)
        elif keys[pygame.K_RIGHT] and direction != (-BLOCK_SIZE, 0):
            direction = (BLOCK_SIZE, 0)
        elif keys[pygame.K_UP] and direction != (0, BLOCK_SIZE):
            direction = (0, -BLOCK_SIZE)
        elif keys[pygame.K_DOWN] and direction != (0, -BLOCK_SIZE):
            direction = (0, BLOCK_SIZE)

        # movement
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # check borders or self eating
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake):
            elapsed = time.time() - start_time
            draw_game_over(score, elapsed)
            return wait_for_restart()

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = get_random_food(snake)
        else:
            snake.pop()

        # draw
        win.fill(BLACK)
        for seg in snake:
            pygame.draw.rect(win, GREEN, (*seg, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(win, BLACK, (seg[0] + 2, seg[1] + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
        pygame.draw.rect(win, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))

        # scores and time
        elapsed = time.time() - start_time
        score_text = font.render(f"Score: {score}  Timeused: {elapsed:.1f}s", True, WHITE)
        win.blit(score_text, (10, 10))
        pygame.display.update()

def get_random_food(snake):
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake:
            return (x, y)

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    while True:
        draw_menu()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_loop(speed=10)
                        waiting = False
                    elif event.key == pygame.K_2:
                        game_loop(speed=18)
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == '__main__':
    main()
