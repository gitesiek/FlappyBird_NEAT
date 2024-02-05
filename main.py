import pygame
import sys


class Bird:
    def __init__(self, x, y, width, height, speed, gravity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.gravity = gravity

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 0),
                         [self.x, self.y, self.width, self.height])

    def flap(self):
        self.speed = -10

    def move(self):
        self.speed += self.gravity
        self.y += self.speed


class Obstacle:
    def __init__(self, x, gap_height, shift, width, speed, height):
        self.upper = [x, 0, width, height // 2 - gap_height // 2]
        self.lower = [x, height // 2 + gap_height // 2,
                      width, height // 2 - gap_height // 2]
        self.shift = shift
        self.speed = speed

    def move(self):
        self.upper[0] -= self.speed
        self.lower[0] -= self.speed

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), self.upper)
        pygame.draw.rect(window, (0, 255, 0), self.lower)


def draw_obstacles(obstacles, window):
    for obstacle in obstacles:
        obstacle.draw(window)


class Score:
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont(None, 36)

    def add_point(self):
        self.points = self.points + 1/19

    def draw(self, window):
        score_text = self.font.render(f"Score: {round(self.points,2)}",
                                      True, (255, 255, 255))
        window.blit(score_text, (10, 10))


def main():
    pygame.init()

    width = 600
    height = 400
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy Bird")

    bird = Bird(100, height // 2 - 25, 50, 50, 0, 0.5)
    obstacles = []
    last_obstacle_time = pygame.time.get_ticks()
    score = Score()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.move()

        for obstacle in obstacles:
            obstacle.move()

        current_time = pygame.time.get_ticks()

        if current_time - last_obstacle_time > 2500:
            new_obstacle = Obstacle(width, 175, 200, 50, 5, height)
            obstacles.append(new_obstacle)
            last_obstacle_time = current_time

        obstacles = [o for o in obstacles if o.upper[0] + 50 > 0]

        for obstacle in obstacles:
            if (
                bird.x < obstacle.upper[0] + obstacle.upper[2] and
                bird.x + bird.width > obstacle.upper[0] and
                (bird.y < obstacle.upper[3] or
                 bird.y + bird.height > obstacle.lower[1])
            ):
                print("Game Over!")
                pygame.quit()
                sys.exit()

        if (
            obstacles and bird.x >
            obstacles[0].upper[0] + obstacles[0].upper[2]
        ):
            score.add_point()

        window.fill((0, 191, 255))
        bird.draw(window)
        draw_obstacles(obstacles, window)
        score.draw(window)

        pygame.display.update()
        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main()
