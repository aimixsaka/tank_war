import pygame

from TankWar.common import Common
from sprites import *
from tank_war import TankWar


class TankWarDouble(TankWar):
    """
    双人模式
    """

    def __init__(self):
        super(TankWarDouble, self).__init__()
        self.enemy = None

    def create_sprite(self):
        self.enemy = HeroOrEnemy(Settings.ENEMY_IMAGE_NAME, self.screen, Settings.ENEMY)
        super(TankWarDouble, self).create_sprite()

    def draw_map(self):
        super(TankWarDouble, self).draw_map()

    def check_keydown(self, event):
        """检查按下按钮的事件"""
        if event.key == pygame.K_LEFT:
            # 按下左键
            self.hero.direction = Settings.LEFT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_RIGHT:
            # 按下右键
            self.hero.direction = Settings.RIGHT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_UP:
            # 按下上键
            self.hero.direction = Settings.UP
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_DOWN:
            # 按下下键
            self.hero.direction = Settings.DOWN
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_s:
            # 按下左键
            self.hero.direction = Settings.LEFT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_f:
            # 按下右键
            self.hero.direction = Settings.RIGHT
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_e:
            # 按下上键
            self.hero.direction = Settings.UP
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_d:
            # 按下下键
            self.hero.direction = Settings.DOWN
            self.hero.is_moving = True
            self.hero.is_hit_wall = False
        elif event.key == pygame.K_SPACE:
            self.enemy.shot()
        elif event.key == pygame.K_1:
            # 英雄发子弹
            self.hero.shot()

    def check_keyup(self, event):
        """检查松开按钮的事件"""
        if event.key == pygame.K_LEFT:
            # 松开左键
            self.hero.direction = Settings.LEFT
            self.hero.is_moving = False
        elif event.key == pygame.K_RIGHT:
            # 松开右键
            self.hero.direction = Settings.RIGHT
            self.hero.is_moving = False
        elif event.key == pygame.K_UP:
            # 松开上键
            self.hero.direction = Settings.UP
            self.hero.is_moving = False
        elif event.key == pygame.K_DOWN:
            # 松开下键
            self.hero.direction = Settings.DOWN
            self.hero.is_moving = False
        elif event.key == pygame.K_s:
            # 松开左键
            self.hero.direction = Settings.LEFT
            self.hero.is_moving = False
        elif event.key == pygame.K_f:
            # 松开右键
            self.hero.direction = Settings.RIGHT
            self.hero.is_moving = False
        elif event.key == pygame.K_e:
            # 松开上键
            self.hero.direction = Settings.UP
            self.hero.is_moving = False
        elif event.key == pygame.K_d:
            # 松开下键
            self.hero.direction = Settings.DOWN
            self.hero.is_moving = False

    def event_handler(self):
        for event in pygame.event.get():
            # 判断是否是退出游戏
            if event.type == pygame.QUIT:
                Common.game_over()
            elif event.type == pygame.KEYDOWN:
                TankWarDouble.check_keydown(self, event)
            elif event.type == pygame.KEYUP:
                TankWarDouble.check_keyup(self, event)

    def check_collide(self):
        # 保证坦克不移出屏幕
        self.hero.hit_wall()
        # 子弹击中墙
        for wall in self.walls:
            # 子弹击中墙
            for bullet in self.hero.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        wall.kill()
                        bullet.kill()
                    elif wall.type == Settings.BOSS_WALL:
                        self.game_still = False
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            for bullet in self.enemy.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        wall.kill()
                        bullet.kill()
                    elif wall.type == Settings.BOSS_WALL:
                        self.game_still = False
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            # 我方坦克撞墙
            if pygame.sprite.collide_rect(self.hero, wall):
                # 不可穿越墙
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                    self.hero.is_hit_wall = True
                    # 移出墙内
                    self.hero.move_out_wall(wall)
            # 敌方坦克撞墙
            if pygame.sprite.collide_rect(self.enemy, wall):
                # 不可穿越墙
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL or wall.type == Settings.BOSS_WALL:
                    self.enemy.is_hit_wall = True
                    # 移出墙内
                    self.enemy.move_out_wall(wall)
        # 子弹击中、敌方坦克碰撞、敌我坦克碰撞
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy.bullets, True, True)
        # 敌方子弹击中我方
        for bullet in self.enemy.bullets:
            if pygame.sprite.collide_rect(bullet, self.hero):
                bullet.kill()
                self.hero.kill()

    def update_sprites(self):
        if self.hero.is_moving:
            self.hero.update()
        if self.enemy.is_moving:
            self.enemy.update()
        self.walls.update()
        self.hero.bullets.update()
        self.enemy.bullets.update()
        self.enemy.bullets.draw(self.screen)
        self.hero.bullets.draw(self.screen)
        self.screen.blit(self.hero.image, self.hero.rect)
        self.walls.draw(self.screen)

    def run(self):
        super(TankWarDouble, self).run()
