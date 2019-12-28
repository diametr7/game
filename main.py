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


# class Bomb(pygame.sprite.Sprite):
#     #image = load_image("bomb.png")
#
#     def __init__(self, group):
#         super().__init__(group)
#         self.image = Bomb.image
#         self.rect = self.image.get_rect()
#
#     def coord(self):
#         return self.rect.x, self.rect.y
bg = pygame.transform.scale(load_image('decoration.jpg'), (WIDTH, HEIGHT))
camera = load_image('camera.png')
x = 400
start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos

    screen.blit(bg, (0, 0))
    if x > 500:
        screen.blit(camera, (0, -100))
    elif x < 300:
        screen.blit(camera, (-200, -100))
    else:
        screen.blit(camera, (-500 + int(x), -100))
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
