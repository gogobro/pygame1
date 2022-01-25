import pygame
import pytmx
import random

WINDOW_SIZE = WINDOW_WIDHT, WINDOW_HEIGHT = 900, 900
FPS = 30
TILE_SIZE = 18
ENEMY_EVENT_TYPE = 30
fight_flag = False


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


class Enemy:
    def __init__(self, enemy):
        self.enemy = enemy
        self.hp = 40
        self.damage = 0
        self.enemy_sprites = pygame.sprite.Group()
        for i in range(3):
            enemy_sprite1 = pygame.sprite.Sprite()
            self.enemy_sprites.add(enemy_sprite1)

    def load_of_sprites(self):
        if self.enemy == 'slime':
            self.enemy_sprites.sprites()[0].image = pygame.image.load('sprites/slime_stand.png')
            self.enemy_sprites.sprites()[0].rect = (-300, -500, 0, 0)
            self.enemy_sprites.sprites()[0].image = pygame.transform.scale(self.enemy_sprites.sprites()[0].image,
                                                                           (2000, 2000))
            self.enemy_sprites.sprites()[1].image = pygame.image.load('sprites/slime_get_hit.png')
            self.enemy_sprites.sprites()[1].rect = (-300, -500, 0, 0)
            self.enemy_sprites.sprites()[1].image = pygame.transform.scale(self.enemy_sprites.sprites()[1].image,
                                                                           (2000, 2000))
            self.enemy_sprites.sprites()[2].image = pygame.image.load('sprites/slime_attack.png')
            self.enemy_sprites.sprites()[2].rect = (-300, -500, 0, 0)
            self.enemy_sprites.sprites()[2].image = pygame.transform.scale(self.enemy_sprites.sprites()[0].image,
                                                                           (2000, 2000))


class Fight:
    def __init__(self):
        self.enemy = ''
        self.vrag = None
        self.hero = None
        self.pose_hero = 0
        self.pose_enemy = 0
        self.turn = True

    def scene(self):
        global fight_flag
        if self.enemy == 'slime':
            self.vrag.load_of_sprites()
            self.hero.load_sprites()
            fight_flag = True
            sc = pygame.display.set_mode((900, 900))
            sc.fill((100, 150, 200))
            for i in range(self.vrag.hp):
                pygame.draw.line(sc, (255, 0, 0), (890 - i, 5), (890 - i, 20))
            for i in range(self.hero.hp):
                pygame.draw.line(sc, (255, 0, 0), (890 - i, 800), (890 - i, 815))
            sc.blit(self.vrag.enemy_sprites.sprites()[self.pose_enemy].image, self.vrag.enemy_sprites.sprites()[0].rect)
            sc.blit(self.hero.hero_sprites.sprites()[self.pose_hero].image, self.hero.hero_sprites.sprites()[0].rect)
            if not self.turn:
                self.enemy_move()

    def activate(self, enemy1):
        self.enemy = enemy1
        self.vrag = Enemy(self.enemy)
        self.hero = Herofight()

    def deactivate(self):
        global fight_flag
        self.enemy = ''
        self.pose_hero = 0
        self.pose_enemy = 0
        self.vrag = None
        self.hero = None
        fight_flag = False

    def hero_attack(self):
        if self.turn:
            self.vrag.hp -= self.hero.dmg
            print(self.vrag.hp)
            self.pose_hero = 1
            self.pose_enemy = 1
            self.turn = False

    def enemy_move(self):
        self.pose_hero = 0
        self.pose_enemy = 0
        self.turn = True


class Herofight:
    def __init__(self):
        self.hero_sprites = pygame.sprite.Group()
        self.dmg = 10
        self.hp = 60
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


def enemy_rnd(cell_id):
    x = random.randint(0, 100)
    if cell_id == 625:
        if x >= 95:
            return 'slime'
        else:
            return False


def main():
    fight = Fight()
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    labirint = Map('map1.tmx', [624, 627, 625])
    hero = Hero('hero.png', (5, 44))
    game = Game(labirint, hero)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.update_hero("up")
                elif event.key == pygame.K_DOWN:
                    game.update_hero("down")
                elif event.key == pygame.K_LEFT:
                    game.update_hero("left")
                elif event.key == pygame.K_RIGHT:
                    game.update_hero("right")
                elif event.key == pygame.K_x:
                    fight.deactivate()
                elif event.key == pygame.K_z and fight_flag:
                    fight.hero_attack()
                if not fight_flag:
                    x = enemy_rnd(labirint.get_title_id(hero.get_position()))
                    fight.activate(x)
        screen.fill((0, 0, 0))
        game.render(screen)
        fight.scene()
        pygame.display.flip()
        clock.tick(FPS)
    if not running:
        pygame.quit()


if __name__ == "__main__":
    main()


