import pygame
from common import Common
from sprites import *


class TankWar(object):
    """
    单双模式的父类， 定义一些通用的方法
    """
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.hero = None
        self.enemies_life = True
        self.player2 = None
        self.player1 = None
        self.walls = None

    def draw_map(self, game_type):
        """
        绘制地图
        :return:
        """
        map_type = Settings.MAP_DICT[game_type]
        for y in range(len(map_type)):
            for x in range(len(map_type[y])):
                if map_type[y][x] == 0:
                    continue
                wall = Wall(Settings.WALLS[map_type[y][x]], self.screen)
                wall.rect.x = x * Settings.BOX_SIZE
                wall.rect.y = y * Settings.BOX_SIZE
                if map_type[y][x] == Settings.RED_WALL:
                    wall.type = Settings.RED_WALL
                elif map_type[y][x] == Settings.IRON_WALL:
                    wall.type = Settings.IRON_WALL
                elif map_type[y][x] == Settings.WEED_WALL:
                    wall.type = Settings.WEED_WALL
                elif map_type[y][x] == Settings.HERO_BOSS_WALL:
                    wall.type = Settings.HERO_BOSS_WALL
                    wall.life = 1
                elif map_type[y][x] == Settings.ENEMY_BOSS_WALL:
                    wall.type = Settings.ENEMY_BOSS_WALL
                    wall.life = 1
                self.walls.add(wall)

    def create_sprite(self, game_type):
        pass

    def event_handler(self):
        pass

    def check_collide(self):
        pass

    def update_sprites(self):
        pass

    def run(self, game_type):
        """
        运行
        调用类的入口
        :param game_type: 游戏类型 会决定地图的绘制矩阵等
        """
        from screen import AfterScreen
        Common.init_game()
        self.create_sprite(game_type)
        if game_type == "D":
            while True:
                self.screen.fill(Settings.SCREEN_COLOR)
                # 1、设置刷新帧率
                self.clock.tick(Settings.FPS)
                # 2、事件监听
                self.event_handler()
                # 3、碰撞监测
                self.check_collide()
                # 4、更新/绘制精灵/精灵组
                self.update_sprites()
                # 5、更新显示
                pygame.display.update()
                if not self.player2.is_alive:
                    page = AfterScreen()
                    page.win("Player1")
                elif not self.player1.is_alive:
                    page = AfterScreen()
                    page.win("Player2")

        elif game_type == "S":
            while True:
                self.screen.fill(Settings.SCREEN_COLOR)
                # 1、设置刷新帧率
                self.clock.tick(Settings.FPS)
                # 2、事件监听
                self.event_handler()
                # 3、碰撞监测
                self.check_collide()
                # 4、更新/绘制精灵/精灵组
                self.update_sprites()
                # 5、更新显示
                pygame.display.update()
                if not self.enemies_life:
                    page = AfterScreen()
                    page.win()
                elif not self.hero.is_alive:
                    page = AfterScreen()
                    page.single_lose()




