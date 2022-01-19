import pygame
import pytmx

WINDOW_SIZE = WINDOW_WIDHT, WINDOW_HEIGHT = 900, 900
FPS = 30
TILE_SIZE = 18
ENEMY_EVENT_TYPE = 30


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
        print(self.get_title_id(position))
        return self.get_title_id(position) in self.free_tiles


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

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.labirint.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))
            print((next_x, next_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    labirint = Map('map1.tmx', [624, 627, 625])
    hero = Hero('hero.png', (20, 20))
    game = Game(labirint, hero)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
