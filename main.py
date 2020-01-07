import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 800
HEIGHT = 600
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
sheep_sprites = pygame.sprite.Group()
bomb_sprites = pygame.sprite.Group()
fire_sprites = pygame.sprite.Group()


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


class Sheep(pygame.sprite.Sprite):
    # image = pygame.transform.scale(load_image("1.bmp", color_key=-1), (200, 150))

    def __init__(self, name, shift):
        super().__init__(sheep_sprites)
        self.image = pygame.transform.scale(load_image(name, color_key=-1), (200, 150))
        self.go = shift
        self.rect = self.image.get_rect()
        if shift == 1:
            self.rect.x = WIDTH
        else:
            self.rect.x = -200
        self.rect.y = 150
        self.v = 1
        self.mask = pygame.mask.from_surface(self.image)

    def revers(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.go = (self.go + 1) % 2

    def update(self, *args):
        if self.go == 1:
            if self.rect.x <= -200:
                self.kill()
            else:
                self.rect.x -= self.v
        else:
            if self.rect.x >= WIDTH:
                self.kill()
            else:
                self.rect.x += self.v
        if self.rect.x == 300:
            Sheep('1.bmp', self.go)

    def fired(self):
        fire = Fire(self.rect.x + 40, self.rect.y)
        for _ in range(9):
            fire.update()
            fire_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(10)
        fire.kill()
        for el in sheep_sprites:
            el.revers()


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
        super().__init__(bomb_sprites)
        self.radius = 20
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
x = 400
Sheep("1.bmp", 1)
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
    screen.blit(bg, (0, 0))
    sheep_sprites.draw(screen)
    if drawing:
        for el in bomb_sprites:
            el.update()
        bomb_sprites.draw(screen)
    if bomb_num == 10 and drawing is False:
        bomb_num = 0
        bomb_log = True
        sheep_sprites.empty()
        sh1 = Sheep("1.bmp", 1)
        sh2 = Sheep("2.bmp", 0)
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

# import pygame
# import random
#
# pygame.init()
#
# sizef = width, height = 300, 300
#
# screen = pygame.display.set_mode(sizef)
# screen.fill((0, 0, 0))
# drawing = False
# running = True
# fps = 100
# clock = pygame.time.Clock()
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEMOTION:
#             x, y = event.pos
#
#             drawing = True
#     if drawing:
#         screen.fill((0, 0, 0))
#         pygame.draw.ellipse(screen, (0, 0, 255), (-150, -100, 600, 500), 250)
#
#     pygame.display.flip()
#
# pygame.quit()
