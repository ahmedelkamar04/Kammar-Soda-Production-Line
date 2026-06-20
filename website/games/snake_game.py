import random
import pygame

# -----------------------------
# SNAKE (Pygame) - simple + clean
# - Arrow keys to move
# - Eat food to grow
# - Wall/self collision = Game Over
# - Restart: R or click Restart
# -----------------------------

W, H = 800, 520
CELL = 20
FPS = 12  # snake speed

GRID_W, GRID_H = W // CELL, H // CELL

class Button:
    def __init__(self, text, center, size=(220, 54)):
        self.text = text
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center

    def hover(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen, font, hover=False):
        bg = (70, 140, 220) if hover else (55, 110, 190)
        pygame.draw.rect(screen, bg, self.rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=12)
        img = font.render(self.text, True, (255, 255, 255))
        screen.blit(img, img.get_rect(center=self.rect.center))

class Snake:
    def __init__(self):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.dir = (1, 0)  # moving right
        self.grow = 0

    def set_dir(self, new_dir):
        # prevent instant reverse
        if (new_dir[0] == -self.dir[0] and new_dir[1] == -self.dir[1]):
            return
        self.dir = new_dir

    def head(self):
        return self.body[0]

    def update(self):
        hx, hy = self.head()
        dx, dy = self.dir
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)

        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()

    def collides_self(self):
        return self.head() in self.body[1:]

    def draw(self, screen):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            color = (80, 200, 120) if i == 0 else (60, 170, 100)
            pygame.draw.rect(screen, color, rect, border_radius=6)

class Food:
    def __init__(self, snake_body):
        self.pos = self.random_pos(snake_body)

    def random_pos(self, snake_body):
        while True:
            p = (random.randrange(GRID_W), random.randrange(GRID_H))
            if p not in snake_body:
                return p

    def respawn(self, snake_body):
        self.pos = self.random_pos(snake_body)

    def draw(self, screen):
        x, y = self.pos
        rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
        pygame.draw.rect(screen, (240, 220, 90), rect, border_radius=6)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((W, H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 22)
        self.big = pygame.font.SysFont("arial", 52)

        self.restart_btn = Button("Restart", (W // 2, H // 2 + 80))
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < GRID_W and 0 <= y < GRID_H

    def draw_grid(self):
        # light grid (optional)
        for x in range(0, W, CELL):
            pygame.draw.line(self.screen, (35, 35, 48), (x, 0), (x, H))
        for y in range(0, H, CELL):
            pygame.draw.line(self.screen, (35, 35, 48), (0, y), (W, y))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if not self.game_over:
                        if event.key in (pygame.K_LEFT, pygame.K_a):
                            self.snake.set_dir((-1, 0))
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.snake.set_dir((1, 0))
                        elif event.key in (pygame.K_UP, pygame.K_w):
                            self.snake.set_dir((0, -1))
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.snake.set_dir((0, 1))

                    if self.game_over and event.key == pygame.K_r:
                        self.reset()

                if self.game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart_btn.hover(mouse):
                        self.reset()

            if not self.game_over:
                self.update()

            self.draw(mouse)
            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.snake.update()

        # wall collision
        if not self.in_bounds(self.snake.head()):
            self.game_over = True
            return

        # self collision
        if self.snake.collides_self():
            self.game_over = True
            return

        # eat food
        if self.snake.head() == self.food.pos:
            self.score += 1
            self.snake.grow += 2
            self.food.respawn(self.snake.body)

    def draw(self, mouse):
        self.screen.fill((25, 25, 35))
        self.draw_grid()
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

        ui = self.font.render(f"Score: {self.score}   |   Restart: R (after game over)    |   2026 ", True, (230, 230, 230))
        self.screen.blit(ui, (12, 10))

        if self.game_over:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 165))
            self.screen.blit(overlay, (0, 0))

            title = self.big.render("GAME OVER", True, (255, 255, 255))
            score = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            hint = self.font.render("Press R or click Restart", True, (220, 220, 220))

            self.screen.blit(title, title.get_rect(center=(W // 2, H // 2 - 60)))
            self.screen.blit(score, score.get_rect(center=(W // 2, H // 2 - 10)))
            self.screen.blit(hint, hint.get_rect(center=(W // 2, H // 2 + 25)))

            self.restart_btn.draw(self.screen, self.font, self.restart_btn.hover(mouse))

if __name__ == "__main__":
    Game().run()