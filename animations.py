import pygame


def animate():
    """Анимация."""
    explosion_anim = {'large': [], 'small': [], 'player': [], 'shoot': []}
    for i in range(9):
        filename = 'Explosions_kenney/regularExplosion0{}.png'.format(i)
        img = pygame.image.load(filename)
        image_large = pygame.transform.scale(img, (75, 75))
        explosion_anim['large'].append(image_large)
        image_small = pygame.transform.scale(img, (32, 32))
        explosion_anim['small'].append(image_small)
        filename = 'Shmup_player_expl/sonicExplosion0{}.png'.format(i)
        img = pygame.image.load(filename)
        image_player = pygame.transform.scale(img, (50, 50))
        explosion_anim['player'].append(image_player)
    for i in range(3):
        filename = 'Shoot_anim/MG_shot_{}.png'.format(i)
        img = pygame.image.load(filename)
        image_shoot = pygame.transform.scale(img, (30, 40))
        explosion_anim['shoot'].append(image_shoot)
    return explosion_anim


if __name__ == "__main__":
    animate()
