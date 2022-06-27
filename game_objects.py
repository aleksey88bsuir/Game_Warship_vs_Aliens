import random
from settings import *
from sound import expl_sound, shoot_sound
from animations import animate
import description


animate_ = animate()   # Импорт анимации


class Ship(pygame.sprite.Sprite):
    """Класс корабля, которым управляет игрок."""
    full_hp = pygame.image.load('GO_1000_500/Ship_hp_100.png')
    medium_hp = pygame.image.load('GO_1000_500/Ship_hp_40-70.png')
    low_hp = pygame.image.load('GO_1000_500/Ship_hp_40.png')
    player_images = {'full_hp': full_hp,
                     'medium_hp': medium_hp,
                     'low_hp': low_hp}

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.player_images['full_hp']
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 80
        self.speed_x = 5
        self.min_speed = 1
        self.max_speed = 10
        self.delta_speed = .1
        self.direction_ship = 'right'
        self.health = 100
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.rocket_delay = 200
        self.count_rocket = 15
        self.last_rotate = 30
        self.last_launch = pygame.time.get_ticks()

    def update(self):
        key_state_in_ship = pygame.key.get_pressed()
        if key_state_in_ship[pygame.K_LEFT]:
            self.direction_ship = 'left'
        if key_state_in_ship[pygame.K_RIGHT]:
            self.direction_ship = 'right'
        if key_state_in_ship[pygame.K_UP]:
            self.speed_x += self.delta_speed
            if self.speed_x > self.max_speed:
                self.speed_x = self.max_speed
        if key_state_in_ship[pygame.K_DOWN]:
            self.speed_x -= self.delta_speed
            if self.speed_x < self.min_speed:
                self.speed_x = self.min_speed
        if key_state_in_ship[pygame.K_SPACE]:
            self.shoot(all_sprites=all_sprites, bullets=bullets)
        if key_state_in_ship[pygame.K_b]:
            self.launch_rocket(all_spr=all_sprites, rockets_=rockets)
        if self.direction_ship == 'right':
            self.rect.x += self.speed_x
        else:
            self.rect.x -= self.speed_x

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.direction_ship = 'left'
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction_ship = 'right'

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 80
        if self.power >= 2 and pygame.time.get_ticks() - \
                self.power_time > POWER_UP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.health > 70:
            self.image = self.player_images['full_hp']
        elif 40 <= self.health <= 69:
            self.image = self.player_images['medium_hp']
        else:
            self.image = self.player_images['low_hp']

    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if not self.hidden:
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                if self.power == 1:
                    bullet = Bullet(self.rect.left+33, self.rect.top)
                    shoot_img = Explosion(bullet.rect.center, 'shoot')
                    shoot_img.frame_rate = 2
                    all_sprites.add(shoot_img)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                if self.power >= 2:
                    bullet1 = Bullet(self.rect.left+33, self.rect.centery)
                    bullet2 = Bullet(self.rect.right-33, self.rect.centery)
                    shoot_img1 = Explosion(bullet1.rect.center, 'shoot')
                    shoot_img1.frame_rate = 2
                    all_sprites.add(shoot_img1)
                    shoot_img2 = Explosion(bullet2.rect.center, 'shoot')
                    shoot_img2.frame_rate = 2
                    all_sprites.add(shoot_img2)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, -200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def receive_damage(self, damage):
        self.health -= damage

    def launch_rocket(self, all_spr, rockets_):
        now = pygame.time.get_ticks()
        if now - self.last_launch > self.rocket_delay and \
                self.count_rocket > 0:
            self.last_launch = now
            new_rocket = Rocket(self.rect.centerx+5, self.rect.top)
            all_spr.add(new_rocket)
            rockets_.add(new_rocket)
            self.count_rocket -= 1

    def death_player(self):
        while self.rect.y < 500:
            now = pygame.time.get_ticks()
            if now - self.last_rotate > self.death_rotate:
                self.last_rotate = now
                self.angle += 1
                self.image = pygame.transform.rotate(self.orig, self.angle)
                self.rect = self.image.get_rect()
                if self.angle >= 50:
                    self.rect.y += 1
                    if self.rect.y > 500:
                        self.kill()


class Mob(pygame.sprite.Sprite):
    """Класс прищельцев."""
    total = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    SPAWN = 2
    POINTS = 30
    images = {SMALL: pygame.image.load('GO_1000_500/small_ship.png'),
              MEDIUM: pygame.image.load('GO_1000_500/middle_ship.png'),
              LARGE: pygame.image.load('GO_1000_500/mother_ship.png')
              }
    bomb_change = 100

    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        Mob.total += 1
        self.image = Mob.images[size]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = random.randrange(1, 8)
        self.speed_x = random.randrange(1, 8)
        self.direction_mod_x = random.choice(['right', 'left'])
        self.direction_mod_y = 'down'
        self.size = size

    def update(self):
        if self.direction_mod_x == 'right':
            self.rect.x += self.speed_x
        if self.direction_mod_x == 'left':
            self.rect.x -= self.speed_x
        if self.rect.right > WIDTH:
            self.direction_mod_x = 'left'
        if self.rect.left <= 0:
            self.direction_mod_x = 'right'
        if self.direction_mod_y == 'down':
            self.rect.y += self.speed_y
        else:
            self.rect.y -= self.speed_y
        if self.rect.bottom > MIN_HEIGHT_FOR_MOB:
            self.direction_mod_y = 'up'
        if self.rect.top < 0:
            self.direction_mod_y = 'down'
        self.throw_bomb(all_spr=all_sprites, bombs_=bombs)

    def throw_bomb(self, all_spr, bombs_):
        if random.randrange(Mob.bomb_change) == 0:
            next_bomb = Bomb(self.rect.centerx, self.rect.bottom)
            all_spr.add(next_bomb)
            bombs_.add(next_bomb)

    def die(self):
        if self.size != Mob.SMALL:
            for m in range(Mob.SPAWN):
                m = Mob(x=self.rect.x, y=self.rect.y, size=self.size-1)
                all_sprites.add(m)
                mobs.add(m)
        self.kill()


class Balloon(pygame.sprite.Sprite):
    """Летающие тарелки, поведение отличается от class Mob."""
    total = 0
    min_speed = 1
    max_speed = 10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('GO_1000_500/ballon_ship.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(WIDTH-self.rect.x)
        self.rect.top = random.randrange(0, MIN_HEIGHT_FOR_MOB)
        self.speed_x = random.randrange(Balloon.min_speed, Balloon.max_speed)
        self.direction_mod_x = random.choice(['right', 'left'])
        Balloon.total += 1

    def update(self):
        if self.direction_mod_x == 'right':
            self.rect.x += self.speed_x
        if self.direction_mod_x == 'left':
            self.rect.x -= self.speed_x
        if self.rect.right > WIDTH:
            self.direction_mod_x = 'left'
        if self.rect.left <= 0:
            self.direction_mod_x = 'right'


class Bomb(pygame.sprite.Sprite):
    """Бомбы, которые сбрасывают инопланетяне"""
    min_damage = 20
    max_damage = 60

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('GO_1000_500/laserRed03.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """Пули, выпускаемые нами из корабля"""

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('GO_1000_500/laserBlue03.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Rocket(Bullet):
    """Ракеты, выпускаемые нами из корабля"""

    def __init__(self, x, y):
        Bullet.__init__(self, x, y)
        self.image = pygame.image.load('GO_1000_500/rocket.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20


class Mine(pygame.sprite.Sprite):
    """Мины, наносят урон игроку, если наплыть на них"""

    min_damage = 90
    max_damage = 110
    BUFFER = 200

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('GO_1000_500/mine.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(WIDTH)
        self.rect.bottom = HEIGHT + 50
        self.mine_delay = 200
        self.last_move = pygame.time.get_ticks()
        self.direction_mine = 'up'
        self.event = 0
        self.hidden = True

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_move > self.mine_delay:
            self.last_move = now
            if self.direction_mine == 'up':
                self.rect.y += 1
            if self.rect.bottom == HEIGHT - 44:
                self.direction_mine = 'down'
            if self.direction_mine == 'down':
                self.rect.y -= 1
            if self.rect.bottom == HEIGHT - 50:
                self.direction_mine = 'up'

    def move_up(self, player):
        if player.rect.centerx >= 500:
            self.rect.centerx = random.randrange(0, player.rect.centerx -
                                                 Mine.BUFFER)
        else:
            self.rect.centerx = random.randrange(player.rect.centerx +
                                                 Mine.BUFFER, WIDTH)
        self.rect.bottom = HEIGHT - 48

    def move_down(self):
        self.rect.bottom = HEIGHT + 100




class Pow(pygame.sprite.Sprite):
    """Апгрейды корабля, сбрасываются с подбитых кораблей"""
    powerup_images = {'health': pygame.image.load('GO_1000_500/health_up.png'),
                      'gun': pygame.image.load('GO_1000_500/gun_up.png'),
                      'rocket': pygame.image.load('GO_1000_500/rocket_up.png')}

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['health', 'gun', 'rocket'])
        self.image = self.powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Speedometer(pygame.sprite.Sprite):
    """Отображает текущую скорость корабля"""
    def __init__(self, obj):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('GO_1000_500/Speedometr_arrow.png')
        self.rect = self.image.get_rect()
        self.orig = self.image
        self.obj = obj

    def update(self):
        self.rotate()

    def rotate(self):
        delta_angle = self.obj.speed_x * 30
        angle = 160 - delta_angle
        self.image = pygame.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect(center=(WIDTH - 41, HEIGHT - 44))


class Explosion(pygame.sprite.Sprite):
    """Класс отвечает за отрисовку анимации в игре"""
    def __init__(self, center, type_of_animation):
        pygame.sprite.Sprite.__init__(self)
        self.type_of_animation = type_of_animation
        self.image = animate_[self.type_of_animation][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(animate_[self.type_of_animation]):
                self.kill()
            else:
                center = self.rect.center
                self.image = animate_[self.type_of_animation][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def draw_health_bar(surf, x, y, health):
    """Рисует полоску жизни игрока"""
    if health < 0:
        health = 0
    bar_length = 100
    bar_height = 10
    fill = (health / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    color = None
    if health >= 70:
        color = 'green'
    elif 40 < health < 70:
        color = 'yellow'
    else:
        color = 'red'
    pygame.draw.rect(surf, (color), fill_rect)
    pygame.draw.rect(surf, (0, 0, 255), outline_rect, 2)


def draw_text(surf, text, size, x, y):
    """Отображение текста на экране"""
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (158, 36, 45))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives):
    """Рисует количество оставшихся жизней у игрока"""
    for live in range(lives):
        player_img = pygame.image.load('GO_1000_500/Ship_hp_100.png')
        img = pygame.transform.scale(player_img, (25, 19))
        img_rect = img.get_rect()
        img_rect.x = x + 30 * live
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_rockets(x, y, number_of_rockets):
    """Рисует количество оставшихся ракет у игрока"""
    for rocket in range(number_of_rockets):
        img = pygame.Surface((3, 15))
        img.fill((28, 255, 127))
        img_rect = img.get_rect()
        img_rect.x = x + 10 * rocket
        img_rect.y = y
        screen.blit(img, img_rect)


def new_mob(all_spr, mobs_):
    size = random.randint(1, 3)
    x = random.randrange(WIDTH - 50)
    y = random.randint(0, MIN_HEIGHT_FOR_MOB)
    m = Mob(x, y, size)
    all_spr.add(m)
    mobs_.add(m)


def create_balloon(all_spr, balloons_):
    new_balloon = Balloon()
    all_spr.add(new_balloon)
    balloons_.add(new_balloon)


def is_player_alive(player, hit):
    if player.health <= 0:
        death_explosion = Explosion(hit.rect.center, 'player')
        all_sprites.add(death_explosion)
        # player.death_player()
        player.hide()
        player.lives -= 1
        player.health = 100
    return player.lives == 0


def show_go_screen(player):
    number_of_mobs, number_of_balloons, running = 0, 0, True
    Mob.total = Balloon.total = 0
    if player is None:
        screen.blit(background['hello'], background_rect)
    elif player.lives == 0:
        screen.blit(background['defeat'], background_rect)
        kill_all_obf()
    elif Mob.total == 0 and Balloon.total == 0:
        screen.blit(background['victory'], background_rect)
        kill_all_obf()
    else:
        draw_text(screen, "This is bag", 64, WIDTH / 2, HEIGHT / 4)
        kill_all_obf()
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_q]:
                running = False
                waiting = False
            if key_state[pygame.K_1]:
                number_of_mobs = 3
                number_of_balloons = 5
                Mob.bomb_change = 100
                waiting = False
            if key_state[pygame.K_2]:
                number_of_mobs = 5
                number_of_balloons = 7
                Mob.bomb_change = 80
                waiting = False
            if key_state[pygame.K_3]:
                number_of_mobs = 8
                number_of_balloons = 9
                Mob.bomb_change = 50
                waiting = False
    return number_of_mobs, number_of_balloons, running


def stop_the_game():
    screen.blit(background, background_rect)
    draw_text(screen, 'PAUSE', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, description.about_the_developer, 18, WIDTH / 2,
              HEIGHT * 3 / 4)
    pygame.display.flip()
    pause_in_game = True
    while pause_in_game:
        for _ in pygame.event.get():
            if _.type == pygame.KEYDOWN:
                pause_in_game = False


def play_animation_on_hit(coord, size, all_spr):
    random.choice(expl_sound).play()
    expl = Explosion(coord, size)
    all_spr.add(expl)


def kill_all_obf():
    for obj in all_sprites:
        obj.kill()