import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 800
HEIGHT = 600
STEP = 10

sheep_killed = 0
bomb_pysked = 0
sheep_killed_last = 0
bomb_pysked_last = 0

level = 1
level_next = 10
level_step = 10
level_disappear = 0
parts = (WIDTH + 200) // (2 * level_disappear + 1)
N = 2 * level_disappear + 1
V = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

unsheep_sprites = pygame.sprite.Group()
sheep_sprites = pygame.sprite.Group()
bomb_sprites = pygame.sprite.Group()
fire_sprites = pygame.sprite.Group()


def change_level():
    global level, level_next, level_disappear, level_step, parts, N, V
    if sheep_killed >= level_next:
        level += 1
        level_step = 10 * level
        level_next += level_step
        if level % 3 == 1:
            V = 1
        elif level % 3 == 2:
            V = 2
        else:
            V = 3
            level_disappear += 1
        parts = (WIDTH + 200) // (2 * level_disappear + 1)
        N = 2 * level_disappear + 1


def load_image(name, color_key=None):
    image = pygame.image.load(name)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def middle_screen():
    global sheep_killed, bomb_pysked, sheep_killed_last, bomb_pysked_last, bomb_num, bomb_log, \
        sheep_sprites, unsheep_sprites, level, level_step, level_next
    change_level()
    intro_text = [f"{level} уровень", f"Рейтинг: {level_step - level_next + sheep_killed} из {level_step}",
                  f"Всего выпущено {bomb_pysked} бомб, {bomb_pysked_last} бомб выпущено в последней игре",
                  f"Убито {sheep_killed} кораблей, {sheep_killed_last} кораблей убито в последней игре"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                sheep_killed_last = 0
                bomb_pysked_last = 0
                sheep_sprites.empty()
                unsheep_sprites.empty()
                bomb_log = True
                bomb_num = 0
                Sheep("1.bmp", WIDTH, 1)
                return
        pygame.display.flip()
        clock.tick(FPS)


class UnSheep(pygame.sprite.Sprite):
    def __init__(self, name, x, n):
        super().__init__(unsheep_sprites)
        self.image = pygame.transform.scale(load_image(name, color_key=-1), (200, 150))
        self.n = n
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.v = V

    def update(self, *args):
        if self.rect.x <= -200:
            self.kill()
        self.rect.x -= self.v
        if self.rect.x <= 300 and len(unsheep_sprites) + len(sheep_sprites) < 2:
            Sheep('1.bmp', WIDTH, 1)
            self.kill()


class Sheep(pygame.sprite.Sprite):
    # image = pygame.transform.scale(load_image("1.bmp", color_key=-1), (200, 150))

    def __init__(self, name, x, n):
        super().__init__(sheep_sprites)
        self.image = pygame.transform.scale(load_image(name, color_key=-1), (200, 150))
        self.go = 1
        self.n = n
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 130
        self.v = V
        self.mask = pygame.mask.from_surface(self.image)

    def revers(self):
        self.image = pygame.transform.flip(self.image, False, True)
        self.go = (self.go + 1) % 2
        if self.go == 1:
            self.rect.y = 130
        else:
            self.rect.y = 180

    def update(self, *args):
        if self.rect.x <= -200:
            self.kill()
        else:
            self.rect.x -= self.v
        if self.rect.x <= WIDTH + 200 - self.n * parts:
            if self.n != N:
                self.n += 1
                self.revers()
        if self.rect.x <= 300 and len(unsheep_sprites) + len(sheep_sprites) < 2:
            Sheep('1.bmp', WIDTH, 1)

    def fired(self):
        global sheep_killed, sheep_killed_last
        sheep_killed += 1
        sheep_killed_last += 1
        # print(len(unsheep_sprites) + len(sheep_sprites), unsheep_sprites, sheep_sprites)
        if len(unsheep_sprites) + len(sheep_sprites) >= 2:
            UnSheep('1.bmp', self.rect.x, self.n)
        else:
            Sheep('1.bmp', WIDTH, 1)
        fire = Fire(self.rect.x + 40, self.rect.y)
        for _ in range(9):
            fire.update()
            fire_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(10)
        fire.kill()
        self.kill()


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(fire_sprites)
        self.i = 0
        self.image = load_image(f"regularExplosion0{self.i}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.i = (self.i + 1) % 9
        self.image = load_image(f"regularExplosion0{self.i}.png")


class Bomb(pygame.sprite.Sprite):
    image = load_image("car.png")

    def __init__(self):
        global bomb_pysked, bomb_pysked_last
        super().__init__(bomb_sprites)
        self.radius = 20
        bomb_pysked += 1
        bomb_pysked_last += 1
        self.k = (600 - y) / (400 - x)
        self.b = 600 - 400 * self.k
        self.x = 400
        self.y = 600
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        global drawing, bomb_log
        self.radius -= 0.02
        self.image = pygame.transform.scale(Bomb.image, (int(self.radius), int(self.radius)))
        self.rect = self.image.get_rect()
        if self.k >= 0:
            self.y -= 2 * self.k / (self.k ** 2 + 1) ** 0.5
            self.x -= 2 / (self.k ** 2 + 1) ** 0.5
        else:
            self.y += 2 * self.k / (self.k ** 2 + 1) ** 0.5
            self.x += 2 / (self.k ** 2 + 1) ** 0.5
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.rect.y <= 230:
            drawing = False
            bomb_log = True
        for el in sheep_sprites:
            if pygame.sprite.collide_mask(self, el):
                drawing = False
                el.fired()
                bomb_log = True

    def coord(self):
        return self.rect.x, self.rect.y


bg = pygame.transform.scale(load_image('decoration.jpg'), (WIDTH, HEIGHT))
# camera = load_image('camera.png')
Sheep("1.bmp", WIDTH, 1)
sheep_sprites.draw(screen)
start_screen()
running = True
drawing = False
bomb_log = True
bomb_num = 0  # 10
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if bomb_log:
                bomb_num += 1
                bomb_sprites.empty()
                Bomb()
                drawing = True
                bomb_log = False

    sheep_sprites.update()
    unsheep_sprites.update()
    screen.blit(bg, (0, 0))
    sheep_sprites.draw(screen)
    if drawing:
        for el in bomb_sprites:
            el.update()
        bomb_sprites.draw(screen)
    if bomb_num == 10 and drawing is False:
        middle_screen()
    # if x > 500:
    #     screen.blit(camera, (0, -100))
    # elif x < 300:
    #     screen.blit(camera, (-200, -100))
    # else:
    #     screen.blit(camera, (-500 + int(x), -100))
    pygame.display.flip()
    clock.tick(FPS)
terminate()
