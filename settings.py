import pygame


WIDTH = 1000  # гирина экрана
HEIGHT = 500  # высота экрана
FPS = 50  # кадров в секунду
MIN_HEIGHT_FOR_MOB = 300  # минимальная высота на которую опускаются боты
POWER_UP_TIME = 5000  # время действия апгрейда в милисекундах

font_name = pygame.font.match_font('arial')
background = {'game': pygame.image.load('GO_1000_500/Background.jpg'),
              'hello': pygame.image.load('GO_1000_500/Hello.jpg'),
              'victory': pygame.image.load('GO_1000_500/Winner.jpg'),
              'defeat': pygame.image.load('GO_1000_500/Defeat.jpg')}
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

'''
setting_level = {
    'easy': {'number_of_mobs': 3,
             'number_of_balloons': 5,
             'bomb_change': 100,
             'number_of_rockets': 15,
             'player_health': 100},
    'medium': {'number_of_mobs': 5,
               'number_of_balloons': 7,
               'bomb_change': 50,
               'number_of_rockets': 15,
               'player_health': 100},
    'hard': {'number_of_mobs': 8,
             'number_of_balloons': 9,
             'bomb_change': 50,
             'number_of_rockets': 15,
             'player_health': 100},
    'custom': {'number_of_mobs': 3,
               'number_of_balloons': 5,
               'bomb_change': 100,
               'number_of_rockets': 15,
               'player_health': 100},
}
'''
