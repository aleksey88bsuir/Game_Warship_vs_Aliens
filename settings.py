import pygame


WIDTH = 1000  # гирина экрана
HEIGHT = 500  # высота экрана
FPS = 50  # кадров в секунду
MIN_HEIGHT_FOR_MOB = 300  # минимальная высота на которую опускаются боты
POWER_UP_TIME = 5000  # время действия апгрейда в милисекундах

font_name = pygame.font.match_font('arial')
background = {}
background['game'] = pygame.image.load('GO_1000_500/Background.jpg')
background['hello'] = pygame.image.load('GO_1000_500/Hello.jpg')
background['victory'] = pygame.image.load('GO_1000_500/Winner.jpg')
background['defeat'] = pygame.image.load('GO_1000_500/Defeat.jpg')
background_rect = background['hello'].get_rect()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Warship vs aliens")
pygame.display.set_icon(pygame.image.load("Pictures/icons8-ок-16.png"))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
mines = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bombs = pygame.sprite.Group()
rockets = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
balloons = pygame.sprite.Group()
