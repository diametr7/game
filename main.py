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
saved_bombs = 0

level = 1
level_step = 4
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
    global level, level_disappear, level_step, parts, N, V
    if sheep_killed >= level_step * level:
        level += 1
        if level % 3 == 1:
            V = 1
            level_disappear += 1
        elif level % 3 == 2:
            V = 2
        else:
            V = 3

        parts = (WIDTH + 200) // (2 * level_disappear + 1)
        N = 2 * level_disappear + 1
        return True
    return False


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
    global sheep_killed, bomb_pysked, bomb_num, saved_bombs, \
        sheep_sprites, unsheep_sprites, level, sheep_killed_last, bomb_pysked_last
    intro_text = [f"{level} уровень",
                  f"Всего выпущено бомб: {bomb_pysked}",
                  f"Убито кораблей: {sheep_killed}", f"Запасных бомб: {saved_bombs}"]
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
                bomb_num = 0
                Sheep("1.bmp", WIDTH, 1)
                return
        pygame.display.flip()
        clock.tick(FPS)


def hall_of_fame():
    intro_text = ["Введите свое имя"]
    screen.fill((30, 30, 30))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        clock = pygame.time.Clock()
        box = InputBox(100, 100, 140, 32)
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if box.stop is False:
                    box.handle_event(event)

            box.update()

            screen.fill((30, 30, 30))
            box.draw(screen)

            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

            pygame.display.flip()
            clock.tick(30)


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.stop = False
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.stop = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def stop(self):
        return self.stop

    def text(self):
        return self.text


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
        if self.rect.x <= 300:
            if len(unsheep_sprites) + len(sheep_sprites) < 2:
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
        global drawing
        for el in sheep_sprites:
            if pygame.sprite.collide_mask(self, el):
                drawing = False
                el.fired()
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

    def coord(self):
        return self.rect.x, self.rect.y


bg = pygame.transform.scale(load_image('decoration.jpg'), (WIDTH, HEIGHT))
# camera = load_image('camera.png')
Sheep("1.bmp", WIDTH, 1)
sheep_sprites.draw(screen)
start_screen()
running = True
drawing = False
bomb_num = 0  # 10
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if drawing is False:
                bomb_num += 1
                bomb_sprites.empty()
                Bomb()
                drawing = True

    sheep_sprites.update()
    unsheep_sprites.update()
    screen.blit(bg, (0, 0))
    sheep_sprites.draw(screen)
    if drawing:
        for el in bomb_sprites:
            el.update()
        bomb_sprites.draw(screen)
    if bomb_pysked_last == 5 + saved_bombs and drawing is False:
        saved_bombs = level * 5 - bomb_pysked
        if change_level():
            middle_screen()
        else:
            hall_of_fame()
    elif sheep_killed_last == 4:
        saved_bombs += 1
        change_level()
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
