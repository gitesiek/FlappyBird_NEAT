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
        return (self.x > pipe_pair.upper_pipe.x +
                pipe_pair.upper_pipe.width / 2 and
                self.x < pipe_pair.upper_pipe.x +
                pipe_pair.upper_pipe.width / 2 + 10)


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
        self.color = (255, 255, 255)

    def add_point(self):
        self.points = self.points + 1

    def draw(self):
        score_text = self.font.render(f"Score: {round(self.points,2)}",
                                      True, self.color)
        WINDOW.blit(score_text, (10, 10))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.bird = Bird(HEIGHT // 2 - 25, 0, 0.5)
        self.score = Score()
        self.pipe_pairs = []
        self.new_pipe_pair_event()
        pygame.time.set_timer(pygame.USEREVENT, 1500)

    def new_pipe_pair_event(self):
        pipe_pair = PipePair()
        pipe_pair.create_pipes()
        self.pipe_pairs.append(pipe_pair)

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()
                elif event.type == pygame.USEREVENT:
                    self.new_pipe_pair_event()

            WINDOW.fill((0, 191, 255))
            self.move_and_draw()
            self.reward_or_death()
            pygame.display.update()
            pygame.time.Clock().tick(60)

    def move_and_draw(self):
        self.bird.move()
        self.bird.draw()
        self.score.draw()
        for pipe_pair in self.pipe_pairs:
            pipe_pair.move_pipe_pair()
            pipe_pair.draw_pipe_pair()

    def reward_or_death(self):
        if self.bird.collided_with(self.pipe_pairs[0]):
            self.reset()
        elif self.bird.passed_pipes(self.pipe_pairs[0]):
            self.score.add_point()
        if (self.pipe_pairs[0].upper_pipe.x +
           self.pipe_pairs[0].upper_pipe.width < 0):
            self.pipe_pairs.pop(0)
        if (self.bird.y < 0 or self.bird.y + self.bird.height > HEIGHT):
            self.reset()

    def reset(self):
        self.pipe_pairs = []
        self.new_pipe_pair_event()
        self.bird.y = HEIGHT // 2 - 25
        self.bird.speed = 0
        self.bird.gravity = 0.5
        self.score.points = 0
        pygame.time.set_timer(pygame.USEREVENT, 1500)


class QAgent():
    def __init__(self):
        pass

    def update_q_value(self):
        pass

    def get_best_action(self):
        pass

    def save_model(self):
        pass

    def load_model(self):
        pass


def main():
    flappyBird = Game()
    flappyBird.play()


if __name__ == "__main__":
    main()
