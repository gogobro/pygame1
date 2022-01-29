import pygame
import pytmx
import random
import time
# Переменные не лежащие в основном цикле
WINDOW_SIZE = WINDOW_WIDHT, WINDOW_HEIGHT = 900, 900
FPS = 30
TILE_SIZE = 18
ENEMY_EVENT_TYPE = 30
player_exp = 0
player_lvl = 1
free_lvl = 1
player_shield = 10
player_dmg = 10
player_hp = 60
fight_flag = False
shop_flag = False
startsc = True
reheal = False
parry = False
duble = False
death = False
win = False

# Стартовый экран загрузки + переход на экран правил


def start_screen(screen, clock):
    global startsc
    intro_text = ["New Game", "",
                  "",
                  "Rules"]
    fon = pygame.transform.scale(pygame.image.load('fone.png'), WINDOW_SIZE)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 280
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 230
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while startsc:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                startsc = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()
                if 180 <= x[0] <= 772 and 236 <= x[1] <= 376:
                    return
                elif 180 <= x[0] <= 772 and 463 <= x[1] <= 603:
                    rules(screen)
                    start_screen(screen, clock)
                    return
        if startsc:
            pygame.display.flip()
            clock.tick(FPS)
# Экран правил + переход на стартовый экран


def rules(screen):
    intro_text = ["Rules", "Добро пожаловать!",
                  "Управление героем по карте: стрелочки",
                  "Управление героем в битве: z - удар, x - покинуть бой, с - щит",
                  "v - Способность отхил (если вы ее установили)",
                  "s - Открытие окна прокачки (доступно только при нахождении на карте!)",
                  "a - Способность двойной удар (если вы ее установили)",
                  "d - Способность парирования (если вы ее установили)"]
    screen.fill((100, 150, 200))
    font = pygame.font.Font(None, 34)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
# Магазин для прокачки героя


class Shop:
    def __init__(self):
        pass

    def render_shop(self, screen):
        if shop_flag:
            screen.fill((100, 150, 200))
            screen.blit(pygame.transform.scale(pygame.image.load('sprites/heal_icon.png'), (150, 150)), (100, 100))
            screen.blit(pygame.transform.scale(pygame.image.load('sprites/parry_png.png'), (150, 150)), (350, 100))
            screen.blit(pygame.transform.scale(pygame.image.load('sprites/duble_icon.png'), (150, 150)), (600, 100))
            screen.blit(pygame.transform.scale(pygame.image.load('sprites/hart_icon.png'), (150, 150)), (100, 350))
            screen.blit(pygame.transform.scale(pygame.image.load('sprites/dmg_icon.png'), (150, 150)), (350, 350))
            screen.blit(pygame.transform.scale(pygame.image.load('sprites/shield_icon.png'), (150, 150)), (600, 350))
            screen.blit(pygame.transform.scale(
                pygame.image.load('sprites/hero_stand_pose.png'), (3000, 3000)), (-1200, -600))
            text = [f'lvl: {player_lvl}', f'free lvl: {free_lvl}', f'hp: {player_hp}', f'dmg: {player_dmg}',
                    f'shield: {player_shield}']
            font = pygame.font.Font(None, 40)
            text_coord = 650
            for line in text:
                string_rendered = font.render(line, True, (255, 255, 255))
                intro_rect = string_rendered.get_rect()
                text_coord += 20
                intro_rect.top = text_coord
                intro_rect.x = 730
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    def activate(self):
        global shop_flag
        shop_flag = True

    def deactivate(self):
        global shop_flag
        shop_flag = False
# функция определения нажатия на иконки магазина

    def find(self, x):
        global player_hp, player_dmg, player_shield, free_lvl, reheal, parry, duble
        if free_lvl:
            if 100 <= x[1] <= 250:
                if 100 <= x[0] <= 250:
                    if player_lvl >= 5 and not reheal:
                        reheal = True
                        free_lvl -= 1
                elif 350 <= x[0] <= 500:
                    if player_lvl >= 10 and not parry:
                        parry = True
                        free_lvl -= 1
                elif 600 <= x[0] <= 750:
                    if player_lvl >= 15 and not duble:
                        duble = True
                        free_lvl -= 1
            elif 350 <= x[1] <= 500:
                if 100 <= x[0] <= 250:
                    player_hp += 60
                    free_lvl -= 1
                elif 350 <= x[0] <= 500:
                    player_dmg += 30
                    free_lvl -= 1
                elif 600 <= x[0] <= 750:
                    player_shield += 10
                    free_lvl -= 1
# Основное поле передвижения состоит из тайлов


class Map:
    def __init__(self, filename, free_titles):
        self.map = pytmx.load_pygame(f'{filename}')
        self.height = self.map.height
        self.widht = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_titles

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.widht):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_title_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return self.get_title_id(position) in self.free_tiles
# Класс врага закачка его картинок\данных для ведения боя


class Enemy:
    def __init__(self, enemy):
        self.enemy = enemy
        self.hp = 0
        self.dmg = 0
        self.get_xp = 0
        self.ultimate = 0
        self.cords = (-300, -500, 0, 0)
        self.ult = None
        self.until_ult = 0
        self.enemy_sprites = []

    def load_of_sprites(self):
        # слайм
        if self.enemy == 'slime':
            self.hp = 40
            self.dmg = 10
            self.get_xp = 20
            self.ultimate = 3
            self.cords = (-300, -500, 0, 0)
            img1 = pygame.image.load('sprites/slime_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/slime_get_hit.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/slime_attack.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # гоблин
        elif self.enemy == 'goblin':
            self.hp = 60
            self.dmg = 20
            self.get_xp = 60
            self.ultimate = 3
            img1 = pygame.image.load('sprites/goblin_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/goblin_atack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/goblin_get_hit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # лягушка с копьем
        elif self.enemy == 'frog':
            self.hp = 60
            self.dmg = 40
            self.get_xp = 50
            self.ultimate = 3
            img1 = pygame.image.load('sprites/frog_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/frog_attack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/frog_gethit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # энт
        elif self.enemy == 'ent':
            self.hp = 160
            self.dmg = 70
            self.get_xp = 70
            self.ultimate = 3
            self.cords = (-500, -700, 0, 0)
            img1 = pygame.image.load('sprites/ent_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/ent_attack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/ent_get_hit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # голем
        elif self.enemy == 'golem':
            self.hp = 250
            self.dmg = 70
            self.get_xp = 80
            self.ultimate = 3
            self.cords = (-500, -700, 0, 0)
            img1 = pygame.image.load('sprites/golem_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/golem_atack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/golem_gethit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # демон
        elif self.enemy == 'demon':
            self.hp = 150
            self.dmg = 100
            self.get_xp = 70
            self.ultimate = 3
            self.cords = (-500, -700, 0, 0)
            img1 = pygame.image.load('sprites/demon_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/demon_attack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/demon_gethit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # маг
        elif self.enemy == 'mage':
            self.hp = 120
            self.dmg = 220
            self.get_xp = 100
            self.ultimate = 3
            self.cords = (-500, -900, 0, 0)
            img1 = pygame.image.load('sprites/mage_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/mage_attack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/mage_gethit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # проклятый слайм
        elif self.enemy == 'wlime':
            self.hp = 220
            self.dmg = 120
            self.get_xp = 100
            self.ultimate = 2
            img1 = pygame.image.load('sprites/wlime_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/wlime_attack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/wlime_gethit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
        # дракон - финальный босс
        elif self.enemy == 'dragon':
            self.hp = 1000
            self.dmg = 220
            self.get_xp = 500
            self.ultimate = 4
            self.cords = (-400, -400, 0, 0)
            img1 = pygame.image.load('sprites/dragon_stand.png')
            img1 = pygame.transform.scale(img1, (2000, 2000))

            img2 = pygame.image.load('sprites/dragon_attack.png')
            img2 = pygame.transform.scale(img2, (2000, 2000))

            img3 = pygame.image.load('sprites/dragon_gethit.png')
            img3 = pygame.transform.scale(img3, (2000, 2000))

            img4 = pygame.image.load('sprites/dragon_ult.png')
            img4 = pygame.transform.scale(img4, (2000, 2000))
            self.enemy_sprites.append(img1)
            self.enemy_sprites.append(img2)
            self.enemy_sprites.append(img3)
            self.enemy_sprites.append(img4)

    # удобная функция для рендера спрайтов
    def render(self):
        self.enemy_sprites = []
        self.load_of_sprites()

    # недоработанная функция ультимативных способностей врагов
    def ults(self, enemy, hero):
        if enemy == 'slime':
            self.hp += 20
# основной класс боя с врагом:
# отрисовывает сцену отакует как и игрока так и врага


class Fight:
    def __init__(self):
        self.enemy = ''
        self.vrag = None
        self.hero = Herofight()
        self.hero.load_sprites()
        self.pose_hero = 0
        self.pose_enemy = 0
        self.turn = True

    # основная сцена
    def scene(self, sc):
        global fight_flag, death
        if self.enemy != '':
            fight_flag = True
            time.sleep(0.15)
            sc.fill((100, 150, 200))
            for i in range(self.vrag.hp):
                pygame.draw.line(sc, (255, 0, 0), (890 - i, 5), (890 - i, 20))
            for i in range(self.hero.hp):
                pygame.draw.line(sc, (255, 0, 0), (890 - i, 800), (890 - i, 815))
            if self.hero.shield:
                for i in range(self.hero.shield):
                    pygame.draw.line(sc, (0, 0, 255), (890 - self.hero.hp + i, 800), (890 - self.hero.hp + i, 815))
                pygame.draw.circle(sc, (100, 170, 255), (220, 730), 150)
            font = pygame.font.Font(None, 50)
            text = font.render(f"Супер через {self.vrag.ultimate - self.vrag.until_ult + 1}!",
                               True, (255, 215, 0))
            text1 = [f'heal: {self.hero.heal}', f'duble: {self.hero.duble}', f'parry: {self.hero.parry[0]}']
            font = pygame.font.Font(None, 40)
            text_coord = 650
            for line in text1:
                string_rendered = font.render(line, True, (255, 255, 255))
                intro_rect = string_rendered.get_rect()
                text_coord += 20
                intro_rect.top = text_coord
                intro_rect.x = 730
                text_coord += intro_rect.height
                sc.blit(string_rendered, intro_rect)
            # отрисовка  героя и врага
            sc.blit(text, (300, 25))
            sc.blit(self.vrag.enemy_sprites[self.pose_enemy], self.vrag.cords)
            sc.blit(self.hero.hero_sprites.sprites()[self.pose_hero].image, self.hero.hero_sprites.sprites()[0].rect)
            # порядок очереди героя и врага
            if not self.turn:
                self.enemy_attack()
                death = self.hero_check()
            elif self.turn:
                if self.vrag.hp <= 0:
                    lvlup(player_exp)
                    self.deactivate()
                self.enemy_move()

    # активация класса
    def activate(self, enemy1):
        if enemy1:
            self.fn_restart()
            self.enemy = enemy1
            self.vrag = Enemy(self.enemy)
            self.vrag.render()
            self.hero.hp = player_hp
            self.hero.dmg = player_dmg

    # деактивация класса
    def deactivate(self):
        global fight_flag, player_exp, win
        if self.enemy == 'dragon':
            win = True
        self.enemy = ''
        self.pose_hero = 0
        self.pose_enemy = 0
        player_exp += self.vrag.get_xp
        self.vrag = None
        fight_flag = False
        self.turn = True

    # z - удар героя
    def hero_attack(self):
        if self.turn:
            self.vrag.hp -= self.hero.dmg
            self.pose_hero = 1
            self.pose_enemy = 1
            self.turn = False

    # с - щит героя
    def hero_shield(self):
        if self.turn:
            self.hero.shield += player_shield
            self.pose_hero = 0
            self.pose_enemy = 0
            self.turn = False

    # статичное положение
    def enemy_move(self):
        # статичный спрайт героя
        self.pose_hero = 0
        # статичный спрайт врага
        self.pose_enemy = 0

    # атака врага
    def enemy_attack(self):
        # использования супер приема врагом (пока только у слизня)
        if self.enemy_super():
            self.pose_enemy = 0
            self.time_fn()
            self.turn = True
        # удар врага если у игрока есть щит
        elif self.hero.shield:
            # если парирование готово удар идет на врага
            if self.parry_func():
                self.vrag.hp -= self.vrag.dmg
                self.pose_enemy = 1
                self.pose_hero = 1
            else:
                x = self.hero.shield - self.vrag.dmg
                if x < 0:
                    self.hero.hp += x
                    self.hero.shield = 0
                elif x >= 0:
                    self.hero.shield = x
                self.pose_enemy = 2
        else:
            # если парирование готово удар идет на врага
            if self.parry_func():
                self.vrag.hp -= self.vrag.dmg
                self.pose_enemy = 1
                self.pose_hero = 1
            else:
                # удар врага
                self.hero.hp -= self.vrag.dmg
                self.pose_enemy = 2
        # переход очереди
        self.time_fn()
        self.turn = True

    # супер прием врага (только у слизня)
    def enemy_super(self):
        if self.vrag.until_ult == self.vrag.ultimate:
            self.vrag.ults(self.enemy, self.hero)
            self.vrag.until_ult = 0
            return True
        else:
            self.vrag.until_ult += 1
            return False

    # способность регенерации героя
    def reheal_func(self):
        if self.hero.heal <= 0:
            if reheal and self.turn:
                self.pose_hero = 0
                self.pose_enemy = 0
                self.hero.hp += player_hp // 10
                self.hero.heal = 4
                self.turn = False

    # способность парирования героя
    def parry_func(self):
        if self.hero.parry[1]:
            if parry and not self.turn:
                self.hero.parry[1] = False
                self.hero.parry[0] = 4
                return True

    # способность двойного удара героя
    def duble_func(self):
        if self.hero.duble <= 0:
            if duble and self.turn:
                self.pose_hero = 1
                self.pose_enemy = 1
                self.vrag.hp -= player_dmg * 2
                self.hero.duble = 4
                self.turn = False

    # кул даун способностей
    def time_fn(self):
        if self.hero.duble > 0:
            self.hero.duble -= 1
        if self.hero.heal > 0:
            self.hero.heal -= 1
        if self.hero.parry[0] > 0:
            self.hero.parry[0] -= 1

    # обнуления кул дауна
    def fn_restart(self):
        self.hero.duble = 4
        self.hero.heal = 4
        self.hero.parry = [4, False]

    # проверка на смерть героя
    def hero_check(self):
        if self.hero.hp <= 0:
            return True
        else:
            return False
# класс героя во время битвы


class Herofight:
    def __init__(self):
        self.hero_sprites = pygame.sprite.Group()
        self.dmg = player_dmg
        self.hp = player_hp
        self.shield = 0
        self.parry = [4, False]
        self.heal = 4
        self.duble = 4
        for i in range(3):
            hero_sp = pygame.sprite.Sprite()
            self.hero_sprites.add(hero_sp)

    def load_sprites(self):
        self.hero_sprites.sprites()[0].image = pygame.image.load('sprites/hero_stand_pose.png')
        self.hero_sprites.sprites()[0].rect = (-1200, -650, 0, 0)
        self.hero_sprites.sprites()[0].image = pygame.transform.scale(self.hero_sprites.sprites()[0].image,
                                                                      (3000, 3000))
        self.hero_sprites.sprites()[1].image = pygame.image.load('sprites/hero_hit1.png')
        self.hero_sprites.sprites()[1].rect = (-1200, -650, 0, 0)
        self.hero_sprites.sprites()[1].image = pygame.transform.scale(self.hero_sprites.sprites()[1].image,
                                                                      (3000, 3000))
        self.hero_sprites.sprites()[2].image = pygame.image.load('sprites/hero_hit2.png')
        self.hero_sprites.sprites()[2].rect = (-1200, -650, 0, 0)
        self.hero_sprites.sprites()[2].image = pygame.transform.scale(self.hero_sprites.sprites()[2].image,
                                                                      (3000, 3000))

# класс героя на поле


class Hero:
    def __init__(self, pic, position):
        self.image = pygame.image.load(f'{pic}')
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, ((self.x - 1) * TILE_SIZE - delta, (self.y - 1) * TILE_SIZE - delta))
# связующий класс игры, героя на поле и карты


class Game:
    def __init__(self, labirint, hero):
        self.hero = hero
        self.labirint = labirint

    def render(self, screen):
        self.labirint.render(screen)
        self.hero.render(screen)

    def update_hero(self, movement):
        next_x, next_y = self.hero.get_position()
        if movement == 'left':
            next_x -= 1
        elif movement == 'right':
            next_x += 1
        elif movement == 'up':
            next_y -= 1
        elif movement == 'down':
            next_y += 1
        if self.labirint.is_free((next_x, next_y)) and not fight_flag:
            self.hero.set_position((next_x, next_y))
# вызов существа по типу тайла на котором он стоит


def enemy_rnd(cell_id):
    x = random.randint(0, 100)
    if cell_id == 632:
        if x >= 90:
            return 'slime'
        elif 81 <= x <= 90:
            return 'goblin'
        elif x == 81:
            return 'frog'
        else:
            return False
    elif cell_id in [706, 708, 630, 667, 668, 740]:
        if x >= 95:
            return 'ent'
        else:
            return False
    elif cell_id == 736:
        if x >= 85:
            return 'golem'
        else:
            return False
    elif cell_id == 704:
        if x >= 85:
            return 'mage'
        elif 70 <= x < 85:
            return 'wlime'
        else:
            return False
    elif cell_id == 733:
        if x >= 50:
            return 'demon'
        else:
            return False
    elif cell_id in [709, 710, 711, 712, 733]:
        return 'dragon'
# лвл ап героя - повышение уровня который можно потратить в магазине


def lvlup(xp):
    global player_lvl, free_lvl
    g = 60 * (player_lvl + 1)
    if xp >= g:
        player_lvl += 1
        free_lvl += 1
# смерть героя - конец игры


def game_over(sc):
    intro_text = "GAME OVER"
    sc.fill((0, 0, 0))
    font = pygame.font.Font(None, 70)
    text = font.render(intro_text,
                       True, (255, 255, 255))
    sc.blit(text, (450, 450, 0, 0))
# победа героя - конец игры


def u_win(sc):
    intro_text = "YOU WIN"
    intro_text2 = f"Final score: {player_exp}"
    sc.fill((255, 255, 255))
    font = pygame.font.Font(None, 90)
    font = pygame.font.Font(None, 60)
    text = font.render(intro_text,
                       True, (255, 215, 0))
    text2 = font.render(intro_text2, True, (0, 0, 0))
    sc.blit(text, (400, 600, 0, 0))
    sc.blit(text2, (400, 400, 0, 0))
# сохранение результатов героя при победе


def save():
    with open('score.txt', 'r') as f1:
        g = f1.readlines()
    with open('score.txt', 'a') as f2:
        x = g[-1].split()[0][-1]
        f2.write(f'attempt{str(int(x) + 1)} score: {str(player_exp)}, hp: {str(player_hp)}, dmg: {str(player_dmg)},'
                 f' shield: {str(player_shield)}, lvl: {str(player_lvl)}\n')
# главная функция отрисовывающая весь процесс
# также фиксирует нажатие клавиш двигает героев
# выполняет отрисовку сцен


def main():
    # инициализация классов
    fight = Fight()
    shop = Shop()
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    labirint = Map('map1.tmx', [670, 632, 704, 736, 733, 658, 709])
    hero = Hero('hero.png', (5, 44))
    game = Game(labirint, hero)
    clock = pygame.time.Clock()
    start_screen(screen, clock)
    running = True
    while running:
        # фпс цикл
        for event in pygame.event.get():
            # ивент цикл
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if death:
                    running = False
                elif win:
                    save()
                    running = False
                if shop_flag:
                    x = pygame.mouse.get_pos()
                    shop.find(x)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.update_hero("up")
                elif event.key == pygame.K_DOWN:
                    game.update_hero("down")
                elif event.key == pygame.K_LEFT:
                    game.update_hero("left")
                elif event.key == pygame.K_RIGHT:
                    game.update_hero("right")
                elif event.key == pygame.K_s and not fight_flag:
                    if shop_flag:
                        shop.deactivate()
                    else:
                        shop.activate()
                elif event.key == pygame.K_x and fight_flag:
                    fight.deactivate()
                elif event.key == pygame.K_z and fight_flag:
                    fight.hero_attack()
                elif event.key == pygame.K_c and fight_flag:
                    fight.hero_shield()
                elif event.key == pygame.K_v and fight_flag:
                    fight.reheal_func()
                elif event.key == pygame.K_d and fight_flag and fight.hero.parry[0] <= 0:
                    fight.hero.parry[1] = True
                elif event.key == pygame.K_a and fight:
                    fight.duble_func()
                if not fight_flag:
                    x = enemy_rnd(labirint.get_title_id(hero.get_position()))
                    fight.activate(x)
        if death:
            # проверка на смерть
            game_over(screen)
        elif win:
            # проверка на победу
            u_win(screen)
        else:
            screen.fill((0, 0, 0))
            game.render(screen)
            if shop_flag:
                shop.render_shop(screen)
            fight.scene(screen)
        pygame.display.flip()
        clock.tick(FPS)
    if not running:
        # закрытие окна
        pygame.quit()


# запуск процесса
if __name__ == "__main__":
    main()


