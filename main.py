import sys
import pygame
import sqlite3

# музыкааааааа
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
    # помощь, начать игру, выйти
    # картинка
    intro_text = ["Морской Бой", "Главное меню",
                  "Подбейте как можно больше кораблей.",
                  "У вас всего 5 торпед.",
                  "Для перехода на следующий уровень необходимо убить 4 корабля."]
    screen.fill((30, 30, 50))
    Button('play.png', 6, 320, 100)
    Button('info.png', 0, 380, 100)
    Button('close.png', 4, 440, 100)
    pygame.draw.rect(screen, (38, 158, 63), (300, 80, 200, 80))
    button_sprites.draw(screen)
    pr_line(intro_text[0], 334, 10, 'white')
    pr_line(intro_text[1], 329, 50, 'white')
    pr_line(intro_text[2], 20, 480, 'white')
    pr_line(intro_text[3], 20, 520, 'white')
    pr_line(intro_text[4], 20, 560, 'white')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 100 and y <= 140:
                    if x >= 320 and x <= 360:
                        clock.tick(10)
                        button_sprites.empty()
                        return
                    elif x >= 380 and x <= 420:
                        clock.tick(10)
                        info()
                        screen.fill((30, 30, 50))
                        pygame.draw.rect(screen, (38, 158, 63), (300, 80, 200, 80))
                        button_sprites.draw(screen)
                        pr_line(intro_text[0], 334, 10, 'white')
                        pr_line(intro_text[1], 329, 50, 'white')
                        pr_line(intro_text[2], 20, 480, 'white')
                        pr_line(intro_text[3], 20, 520, 'white')
                        pr_line(intro_text[4], 20, 560, 'white')
                    elif x >= 440 and x <= 480:
                        clock.tick(10)
                        terminate()
        pygame.display.flip()
        clock.tick(FPS)


def info():
    # rules
    intro_text = ["Морской Бой", "Главное меню",
                  "Подбейте как можно больше кораблей.",
                  "У вас всего 5 торпед.",
                  "Для перехода на следующий уровень необходимо убить 4 корабля."]
    screen.fill((30, 30, 50))
    but = Button('back.png', 7, 20, 20)
    back_but.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 20 and y <= 60 and x >= 20 and x <= 60:
                    clock.tick(10)
                    but.kill()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def middle_screen():
    # досрочно закончить игру(в зал славы), играть, помощь
    global sheep_killed, bomb_pysked, bomb_num, saved_bombs, \
        sheep_sprites, unsheep_sprites, level, sheep_killed_last, bomb_pysked_last
    intro_text = [f"{level} уровень",
                  f"Всего выпущено бомб: {bomb_pysked}",
                  f"Убито кораблей: {sheep_killed}", f"Запасных бомб: {saved_bombs}"]
    screen.fill((30, 30, 40))
    Button('play.png', 6, 320, 100)
    Button('info.png', 0, 380, 100)
    Button('stop.png', 4, 440, 100)
    pygame.draw.rect(screen, (38, 158, 63), (300, 80, 200, 80))
    button_sprites.draw(screen)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 100 and y <= 140:
                    if x >= 320 and x <= 360:
                        clock.tick(10)
                        sheep_killed_last = 0
                        bomb_pysked_last = 0
                        sheep_sprites.empty()
                        unsheep_sprites.empty()
                        button_sprites.empty()
                        bomb_num = 0
                        Sheep("1.bmp", WIDTH, 1)
                        return
                    elif x >= 380 and x <= 420:
                        clock.tick(10)
                        info()
                        screen.fill((30, 30, 50))
                        pygame.draw.rect(screen, (38, 158, 63), (300, 80, 200, 80))
                        button_sprites.draw(screen)
                        text_coord = 50
                        for line in intro_text:
                            string_rendered = font.render(line, 1, pygame.Color('white'))
                            intro_rect = string_rendered.get_rect()
                            text_coord += 10
                            intro_rect.top = text_coord
                            intro_rect.x = 10
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)
                    elif x >= 440 and x <= 480:
                        clock.tick(10)
                        button_sprites.empty()
                        hall_of_fame()
        pygame.display.flip()
        clock.tick(FPS)


def rating(spisok):
    itog = []
    i = 1
    for el in spisok[len(spisok) - 1:0:-1]:
        itog.append([str(i), el[0], str(el[1])])
        i += 1
    # print(itog)
    return itog


font = pygame.font.Font(None, 30)


def pr_line(line, x, y, color, sh=None, tag=30):
    font1 = pygame.font.Font(sh, tag)
    string_rendered = font1.render(line, 1, pygame.Color(color))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = x
    intro_rect.y = y
    screen.blit(string_rendered, intro_rect)


def hall_of_fame():
    # обновлять рекорды после добавления
    global sheep_killed, bomb_pysked_last, bomb_pysked, sheep_killed_last
    con = sqlite3.connect('rating.sqlite3')
    cur = con.cursor()
    res = rating(cur.execute(f"""SELECT name, score FROM rating ORDER BY score""").fetchall())[:5]
    intro_text = ["Введите свое имя и нажмите Enter:", f"Заработано баллов: {sheep_killed}", "Таблица лидеров"]
    screen.fill((30, 30, 30))
    Button('new.png', 6, 320, 500)
    Button('info.png', 0, 380, 500)
    Button('close.png', 4, 440, 500)
    pygame.draw.rect(screen, (38, 158, 63), (300, 480, 200, 80))
    button_sprites.draw(screen)
    pr_line(intro_text[0], 10, 20, 'white')
    pr_line(intro_text[1], 10, 140, 'white')
    pr_line(intro_text[2], 400, 20, 'white')
    X, Y = 400, 70
    i = 1
    for el in res:
        if i == 1:
            s = 'gold'
        elif i == 2:
            s = 'black'
        elif i == 3:
            s = 'red'
        else:
            s = 'white'
        pr_line('   '.join(el), X, Y, s)
        Y += 20
        i += 1
    app = True
    clock = pygame.time.Clock()
    box = InputBox(10, 70, 140, 32)
    done = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 500 and y <= 540:
                    if x >= 320 and x <= 360:
                        clock.tick(10)
                        sheep_killed_last = 0
                        bomb_pysked_last = 0
                        sheep_sprites.empty()
                        unsheep_sprites.empty()
                        button_sprites.empty()
                        main()
                    elif x >= 380 and x <= 420:
                        clock.tick(10)
                        info()
                        screen.fill((30, 30, 30))
                        box.draw(screen)
                        pygame.draw.rect(screen, (38, 158, 63), (300, 480, 200, 80))
                        button_sprites.draw(screen)
                        pr_line(intro_text[0], 10, 20, 'white')
                        pr_line(intro_text[1], 10, 140, 'white')
                        pr_line(intro_text[2], 400, 20, 'white')
                        pr_line(f'Вы на {j} месте', 10, 200, 'white')
                        X, Y = 400, 70
                        i = 1
                        for el in res:
                            if i == 1:
                                s = 'gold'
                            elif i == 2:
                                s = 'grey'
                            elif i == 3:
                                s = 'orange'
                            else:
                                s = 'white'
                            pr_line('   '.join(el), X, Y, s)
                            Y += 20
                            i += 1
                        pygame.display.flip()
                        clock.tick(30)
                    elif x >= 440 and x <= 480:
                        clock.tick(10)
                        terminate()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y >= 500 and y <= 540:
                        if x >= 320 and x <= 360:
                            clock.tick(10)
                            sheep_killed_last = 0
                            bomb_pysked_last = 0
                            sheep_sprites.empty()
                            unsheep_sprites.empty()
                            button_sprites.empty()
                            main()
                        elif x >= 380 and x <= 420:
                            clock.tick(10)
                            info()
                            screen.fill((30, 30, 30))
                            pygame.draw.rect(screen, (38, 158, 63), (300, 80, 480, 80))
                            button_sprites.draw(screen)
                            pygame.display.flip()
                        elif x >= 440 and x <= 480:
                            clock.tick(10)
                            terminate()
                if box.stop is False:
                    box.handle_event(event)
                else:
                    name = box.texts()
                    done = True
                    break
            box.update()

            screen.fill((30, 30, 30))
            box.draw(screen)
            pygame.draw.rect(screen, (38, 158, 63), (300, 480, 200, 80))
            button_sprites.draw(screen)
            pr_line(intro_text[0], 10, 20, 'white')
            pr_line(intro_text[1], 10, 140, 'white')
            pr_line(intro_text[2], 400, 20, 'white')
            X, Y = 400, 70
            i = 1
            for el in res:
                if i == 1:
                    s = 'gold'
                elif i == 2:
                    s = 'grey'
                elif i == 3:
                    s = 'orange'
                else:
                    s = 'white'
                pr_line('   '.join(el), X, Y, s)
                Y += 20
                i += 1
            pygame.display.flip()
            clock.tick(30)
        if app:
            cur.execute(f"""INSERT INTO rating('name', 'score') VALUES('{name}', {sheep_killed})""")
            res1 = rating(cur.execute(f"""SELECT name, score FROM rating ORDER BY score""").fetchall())
            con.commit()
            con.close()
            j = 0
            for el in res1:
                if [str(el[1]), el[2]] == [name, str(sheep_killed)]:
                    j = el[0]
                    break
            app = False
            pr_line(f'Вы на {j} месте', 10, 200, 'white')
            pygame.display.flip()


def pause():  # экран паузы...(с продолжением и помощью, и досрочным заканчиванием в зал славы)
    global sheep_killed, bomb_pysked, bomb_num, saved_bombs, \
        sheep_sprites, unsheep_sprites, level, sheep_killed_last, bomb_pysked_last
    intro_text = ["Пауза", f"{level} уровень",
                  f"Всего выпущено бомб: {bomb_pysked}",
                  f"Убито кораблей: {sheep_killed}", f"Запасных бомб: {saved_bombs}"]
    screen.fill((30, 30, 30))
    Button('play.png', 6, 320, 100)
    Button('info.png', 0, 380, 100)
    Button('stop.png', 4, 440, 100)
    pygame.draw.rect(screen, (38, 158, 63), (300, 80, 200, 80))
    button_sprites.draw(screen)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y >= 100 and y <= 140:
                    if x >= 320 and x <= 360:
                        clock.tick(10)
                        button_sprites.empty()
                        return
                    elif x >= 380 and x <= 420:
                        clock.tick(10)
                        info()
                        screen.fill((30, 30, 30))
                        pygame.draw.rect(screen, (38, 158, 63), (300, 80, 200, 80))
                        button_sprites.draw(screen)
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
                    elif x >= 440 and x <= 480:
                        clock.tick(10)
                        button_sprites.empty()
                        hall_of_fame()
        pygame.display.flip()
        clock.tick(FPS)


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
                    # print(self.text)
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

    def texts(self):
        return self.text


button_sprites = pygame.sprite.Group()
help_but = pygame.sprite.Group()  # info
pause_but = pygame.sprite.Group()  # pause
continue_but = pygame.sprite.Group()  # play
end_but = pygame.sprite.Group()  # stop
close_but = pygame.sprite.Group()  # close
new_but = pygame.sprite.Group()  # new
play_but = pygame.sprite.Group()  # play
back_but = pygame.sprite.Group()
but = [help_but, pause_but, continue_but, end_but, close_but, new_but, play_but, back_but]


class Button(pygame.sprite.Sprite):
    def __init__(self, name, gr, x, y):
        super().__init__(button_sprites)
        self.add(but[gr])
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
        self.go = (self.go + 1) % 2

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
        if len(unsheep_sprites) + len(sheep_sprites) >= 2:
            UnSheep('1.bmp', self.rect.x, self.n)
        else:
            Sheep('1.bmp', WIDTH, 1)
        for i in range(9):
            Fire(self.rect.x + 40, self.rect.y, i)
            fire_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(10)
            fire_sprites.empty()
        self.kill()
    def go(self):
        return self.go

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, i):
        super().__init__(fire_sprites)
        self.image = load_image(f"regularExplosion0{i}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
            if pygame.sprite.collide_mask(self, el) and el.go == 1:
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
        if self.rect.y <= 230 or self.rect.x <= -10 or self.rect.x >= WIDTH:
            self.kill()
            drawing = False


def main():
    global sheep_killed, sheep_killed_last, bomb_pysked, bomb_pysked_last, bomb_num, \
        saved_bombs, level, level_step, level_disappear, parts, N, V, x, y, drawing
    # hall_of_fame()
    # middle_screen() +
    # pause() +
    # info() + (need text)
    bg = pygame.transform.scale(load_image('decoration.jpg'), (WIDTH, HEIGHT))
    # camera = pygame.transform.scale(load_image('1.png'), [1000, 800])
    Sheep("2.png", WIDTH, 1)
    sheep_sprites.draw(screen)
    start_screen()
    running = True
    drawing = False
    bomb_num = 0  # 5
    sheep_killed = 0
    bomb_pysked = 0
    sheep_killed_last = 0
    bomb_pysked_last = 0
    saved_bombs = 0

    level = 1
    level_step = 4
    level_disappear = 2
    parts = (WIDTH + 200) // (2 * level_disappear + 1)
    N = 2 * level_disappear + 1
    V = 1
    but = Button('pause.png', 1, 750, 10)
    # пауза
    x = 400
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= 750 and x <= 790 and y >= 10 and y <= 50:

                    but.kill()
                    pause()
                    but = Button('pause.png', 1, 750, 10)
                elif drawing is False:
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
            but.kill()
            saved_bombs = level * 5 - bomb_pysked
            if saved_bombs > 5:
                saved_bombs = 5
            if change_level():
                middle_screen()
            else:
                hall_of_fame()
        elif sheep_killed_last == 4:
            but.kill()
            if saved_bombs < 5:
                saved_bombs += 1
            change_level()
            middle_screen()
        # if x > 500:
        #     screen.blit(camera, (0, -100))
        # elif x < 300:
        #     screen.blit(camera, (-200, -100))
        # else:
        #     screen.blit(camera, (-500 + int(x), -100))
        pr_line(f"Осталось {5 + saved_bombs - bomb_num} бомб", 10, 30, 'white')
        pr_line(f"{level} уровень", 10, 10, 'white')
        pr_line(f"Убито {sheep_killed_last} кораблей", 10, 50, 'white')
        pause_but.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


main()
