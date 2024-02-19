import pygame
import sys
import random
import neat

WIDTH = 600
HEIGHT = 400
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
MAX_FITNESS = 1000000000
best_agent_id = "49"


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
        self.max_points = 0

    def add_point(self):
        self.points = self.points + 1
        if self.points > self.max_points:
            self.max_points = self.points

    def draw(self):
        score_text = self.font.render(f"Score: {round(self.points,2)}",
                                      True, self.color)
        WINDOW.blit(score_text, (10, 10))
        max_score_text = self.font.render(f"Max: {round(self.max_points,2)}",
                                          True, self.color)
        WINDOW.blit(max_score_text, (150, 10))


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
            self.move_and_draw()
            self.reward_or_death()
            pygame.display.update()
            WINDOW.fill((0, 191, 255))
            pygame.time.Clock().tick(60)

    def plAI(self):
        self.config_path = "config.txt"
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  self.config_path)
        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.fitness_threshold = 1000000
        self.generation = 0
        self.checkpointer = neat.Checkpointer(filename_prefix='flappy_agent_')

        while True:
            self.population.run(self.eval_genomes, 1)
            if self.generation % 5 == 0:
                self.save_checkpoint()
            self.generation += 1

    def get_inputs(self):
        bird_y = self.bird.y
        bird_x = self.bird.x
        pipe_x = self.pipe_pairs[0].upper_pipe.x
        pipe_y = self.pipe_pairs[0].upper_pipe.height
        return [bird_y, bird_x, pipe_x, pipe_y]

    def save_checkpoint(self):
        self.checkpointer.save_checkpoint(config=self.config, population=self.population.population, species_set=self.population.species, generation=self.generation)

    def load_checkpoint(self):
        restored_population = self.checkpointer.restore_checkpoint('flappy_agent_'+str(best_agent_id))
        self.population = restored_population
        self.population.add_reporter(neat.StdOutReporter(True))
        self.generation = int(best_agent_id)

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.reset()
            fitness = 0
            pygame.time.set_timer(pygame.USEREVENT, 1500)
            alive_for = 0

            while True:
                alive_for_add = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.bird.flap()
                        elif event.key == pygame.K_s:
                            self.save_checkpoint()
                        elif event.key == pygame.K_l:
                            self.load_checkpoint()
                    elif event.type == pygame.USEREVENT:
                        self.new_pipe_pair_event()
                inputs = self.get_inputs()
                output = net.activate(inputs)
                if output[0] > 0.5:
                    self.bird.flap()
                self.move_and_draw()
                fitness_add, alive_for_add = self.reward_or_death()
                alive_for += alive_for_add
                if alive_for > 4000:
                    break
                fitness += fitness_add

                pygame.display.update()
                WINDOW.fill((0, 191, 255))
                pygame.time.Clock().tick(60)
            genome.fitness = fitness

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
            return (-100, 4000)
        elif self.bird.passed_pipes(self.pipe_pairs[0]):
            self.score.add_point()
            return (self.score.points * 1000, 1)
        if (self.bird.y < 0 or self.bird.y + self.bird.height > HEIGHT):
            self.reset()
            return (-2000, 4001)
        if (self.pipe_pairs[0].upper_pipe.x +
           self.pipe_pairs[0].upper_pipe.width < 0):
            self.pipe_pairs.pop(0)
            return 0, 0
        return 1, 0

    def reset(self):
        self.pipe_pairs = []
        self.new_pipe_pair_event()
        self.bird.y = HEIGHT // 2 - 25
        self.bird.speed = 0
        self.bird.gravity = 0.5
        self.score.points = 0
        pygame.time.set_timer(pygame.USEREVENT, 1500)


def main():
    flappy_bird_game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    flappy_bird_game.play()
                elif event.key == pygame.K_a:
                    flappy_bird_game.plAI()


if __name__ == "__main__":
    main()
