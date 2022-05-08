import pygame

from TankWar.common import Common
from sprites import *


class TankWar(object):
    """
    单双模式的父类， 定义一些通用的方法
    """
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.game_still = True
        self.hero = None
        self.walls = None

    def create_sprite(self):
        self.hero = HeroOrEnemy(Settings.HERO_IMAGE_NAME, self.screen, Settings.HERO)
        self.walls = pygame.sprite.Group()
        self.draw_map()

    def draw_map(self):
        """
        绘制地图
        :return:
        """
        for y in range(len(Settings.MAP_ONE)):
            for x in range(len(Settings.MAP_ONE[y])):
                if Settings.MAP_ONE[y][x] == 0:
                    continue
                wall = Wall(Settings.WALLS[Settings.MAP_ONE[y][x]], self.screen)
                wall.rect.x = x*Settings.BOX_SIZE
                wall.rect.y = y*Settings.BOX_SIZE
                if Settings.MAP_ONE[y][x] == Settings.RED_WALL:
                    wall.type = Settings.RED_WALL
                elif Settings.MAP_ONE[y][x] == Settings.IRON_WALL:
                    wall.type = Settings.IRON_WALL
                elif Settings.MAP_ONE[y][x] == Settings.WEED_WALL:
                    wall.type = Settings.WEED_WALL
                elif Settings.MAP_ONE[y][x] == Settings.BOSS_WALL:
                    wall.type = Settings.BOSS_WALL
                    wall.life = 1
                self.walls.add(wall)

    def event_handler(self):
        pass

    def check_collide(self):
        pass

    def update_sprites(self):
        pass

    def run(self):
        Common.init_game()
        self.create_sprite()
        while True and self.hero.is_alive and self.game_still:
            self.screen.fill(Settings.SCREEN_COLOR)
            # 1、设置刷新帧率
            self.clock.tick(Settings.FPS)
            # 2、事件监听
            self.event_handler()
            # 3、碰撞监测
            self.check_collide()
            # 4、更新/绘制精灵/经理组
            self.update_sprites()
            # 5、更新显示
            pygame.display.update()
        Common.game_over()

