import pygame
import sys
import random

WIDTH = 600
HEIGHT = 400
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


class Bird:
    def __init__(self, y, speed, gravity):
        self.x = 100
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = speed
        self.gravity = gravity
        self.color = (255, 255, 0)

    def draw(self):
        pygame.draw.rect(WINDOW, self.color,
                         [self.x, self.y, self.width, self.height])

    def flap(self):
        self.speed = -10

    def move(self):
        self.speed += self.gravity
        self.y += self.speed

    def upper_pipe_colision(self, upper_pipe):
        return (self.x < upper_pipe.x + upper_pipe.width and
                self.x + self.width > upper_pipe.x and
                self.y < upper_pipe.height)

    def lower_pipe_colision(self, lower_pipe):
        return (self.x < lower_pipe.x + lower_pipe.width and
                self.x + self.width > lower_pipe.x and
                self.y + self.height > lower_pipe.y)

    def collided_with(self, pipe_pair):
        return (self.upper_pipe_colision(pipe_pair.upper_pipe) or
                self.lower_pipe_colision(pipe_pair.lower_pipe))

    def passed_pipes(self, pipe_pair):
        return self.x > pipe_pair.upper_pipe.x + pipe_pair.upper_pipe.width / 2


class Pipe:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.width = 50
        self.height = height
        self.speed = 5
        self.color = (0, 255, 0)

    def move(self):
        self.x = self.x - self.speed

    def draw(self):
        pygame.draw.rect(WINDOW, self.color,
                         [self.x, self.y, self.width, self.height])


class PipePair:
    def __init__(self):
        self.gap_between_pipes = 200
        self.upper_pipe, self.lower_pipe = self.create_pipes()

    def create_upper_pipe(self, upper_pipe_height):
        return Pipe(WIDTH, 0, upper_pipe_height)

    def create_lower_pipe(self, lower_pipe_y):
        return Pipe(WIDTH, lower_pipe_y, HEIGHT-lower_pipe_y)

    def create_pipes(self):
        upper_pipe_height = random.randrange(0, HEIGHT // 2)
        lower_pipe_y = upper_pipe_height + self.gap_between_pipes
        upper_pipe = self.create_upper_pipe(upper_pipe_height)
        lower_pipe = self.create_lower_pipe(lower_pipe_y)

        return upper_pipe, lower_pipe

    def move_pipe_pair(self):
        self.lower_pipe.move()
        self.upper_pipe.move()

    def draw_pipe_pair(self):
        self.upper_pipe.draw()
        self.lower_pipe.draw()


class Score:
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont(None, 36)

    def add_point(self):
        self.points = self.points + 1

    def draw(self):
        score_text = self.font.render(f"Score: {round(self.points,2)}",
                                      True, (255, 255, 255))
        WINDOW.blit(score_text, (10, 10))


class Game:
    def __init__(self):
        pass

    def draw(self):
        pass

    def move(self):
        pass

    def reset(self):
        pass


pipe_pairs = []


def new_pipe_pair_event():
    pipe_pair = PipePair()
    pipe_pair.create_pipes()
    pipe_pairs.append(pipe_pair)


def main():
    pygame.init()
    pygame.display.set_caption("Flappy Bird")

    bird = Bird(HEIGHT // 2 - 25, 0, 0.5)
    score = Score()

    pygame.time.set_timer(pygame.USEREVENT, 1500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
            elif event.type == pygame.USEREVENT:
                new_pipe_pair_event()

        WINDOW.fill((0, 191, 255))

        bird.move()
        bird.draw()

        for pipe_pair in pipe_pairs:
            pipe_pair.move_pipe_pair()
            pipe_pair.draw_pipe_pair()
            if bird.collided_with(pipe_pair):
                print("kolizja")
                pipe_pairs.pop(0)  # game.reset()
            elif bird.passed_pipes(pipe_pair):
                print("nagroda")
                score.add_point()
                pipe_pairs.pop(0)  # TODO: make it pop later ??

        score.draw()

        pygame.display.update()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()
