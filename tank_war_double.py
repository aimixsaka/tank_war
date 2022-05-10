import pygame

from common import Common
from sprites import *
from tank_war import TankWar


class TankWarDouble(TankWar):
    """
    双人模式
    """

    def __init__(self):
        super(TankWarDouble, self).__init__()

    def create_sprite(self, game_type):
        """
        创建双人模式下精灵
        包括英雄和敌人
        """
        self.player1 = HeroOrEnemy(Settings.ENEMY_IMAGE_NAME, self.screen, Settings.ENEMY)
        self.player2 = HeroOrEnemy(Settings.HERO_IMAGE_NAME, self.screen, Settings.HERO)
        self.walls = pygame.sprite.Group()
        super(TankWarDouble, self).draw_map(game_type)

    def check_keydown(self, event):
        """检查按下按钮的事件"""
        if event.key == pygame.K_LEFT:
            # 按下左键
            self.player2.direction = Settings.LEFT
            self.player2.is_moving = True
            self.player2.is_hit_wall = False
        elif event.key == pygame.K_RIGHT:
            # 按下右键
            self.player2.direction = Settings.RIGHT
            self.player2.is_moving = True
            self.player2.is_hit_wall = False
        elif event.key == pygame.K_UP:
            # 按下上键
            self.player2.direction = Settings.UP
            self.player2.is_moving = True
            self.player2.is_hit_wall = False
        elif event.key == pygame.K_DOWN:
            # 按下下键
            self.player2.direction = Settings.DOWN
            self.player2.is_moving = True
            self.player2.is_hit_wall = False
        elif event.key == pygame.K_a:
            # 按下左键
            self.player1.direction = Settings.LEFT
            self.player1.is_moving = True
            self.player1.is_hit_wall = False
        elif event.key == pygame.K_d:
            # 按下右键
            self.player1.direction = Settings.RIGHT
            self.player1.is_moving = True
            self.player1.is_hit_wall = False
        elif event.key == pygame.K_w:
            # 按下上键
            self.player1.direction = Settings.UP
            self.player1.is_moving = True
            self.player1.is_hit_wall = False
        elif event.key == pygame.K_s:
            # 按下下键
            self.player1.direction = Settings.DOWN
            self.player1.is_moving = True
            self.player1.is_hit_wall = False
        elif event.key == pygame.K_SPACE:
            self.player1.shot()
        elif event.key == pygame.K_1:
            # 英雄发子弹
            self.player2.shot()

    def check_keyup(self, event):
        """检查松开按钮的事件"""
        if event.key == pygame.K_LEFT:
            # 松开左键
            self.player2.direction = Settings.LEFT
            self.player2.is_moving = False
        elif event.key == pygame.K_RIGHT:
            # 松开右键
            self.player2.direction = Settings.RIGHT
            self.player2.is_moving = False
        elif event.key == pygame.K_UP:
            # 松开上键
            self.player2.direction = Settings.UP
            self.player2.is_moving = False
        elif event.key == pygame.K_DOWN:
            # 松开下键
            self.player2.direction = Settings.DOWN
            self.player2.is_moving = False
        elif event.key == pygame.K_a:
            # 松开左键
            self.player1.direction = Settings.LEFT
            self.player1.is_moving = False
        elif event.key == pygame.K_d:
            # 松开右键
            self.player1.direction = Settings.RIGHT
            self.player1.is_moving = False
        elif event.key == pygame.K_w:
            # 松开上键
            self.player1.direction = Settings.UP
            self.player1.is_moving = False
        elif event.key == pygame.K_s:
            # 松开下键
            self.player1.direction = Settings.DOWN
            self.player1.is_moving = False

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
        """
        判断撞墙事件，退出事件，死亡事件
        """
        # 保证坦克不移出屏幕
        self.player2.hit_wall()
        # 子弹击中墙
        for wall in self.walls:
            # 子弹击中墙
            for bullet in self.player2.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        wall.kill()
                        bullet.kill()
                    elif wall.type == Settings.ENEMY_BOSS_WALL:
                        self.player1.kill()
                    elif wall.type == Settings.HERO_BOSS_WALL:
                        self.player2.kill()
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            for bullet in self.player1.bullets:
                if pygame.sprite.collide_rect(wall, bullet):
                    if wall.type == Settings.RED_WALL:
                        wall.kill()
                        bullet.kill()
                    elif wall.type == Settings.HERO_BOSS_WALL:
                        self.player2.kill()
                    elif wall.type == Settings.ENEMY_BOSS_WALL:
                        self.player1.kill()
                    elif wall.type == Settings.IRON_WALL:
                        bullet.kill()
            # 我方坦克撞墙
            if pygame.sprite.collide_rect(self.player2, wall):
                # 不可穿越墙
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL \
                        or wall.type == Settings.HERO_BOSS_WALL \
                        or wall.type == Settings.ENEMY_BOSS_WALL:
                    self.player2.is_hit_wall = True
                    # 移出墙内
                    self.player2.move_out_wall(wall)
            # 敌方坦克撞墙
            if pygame.sprite.collide_rect(self.player1, wall):
                # 不可穿越墙
                if wall.type == Settings.RED_WALL or wall.type == Settings.IRON_WALL \
                        or wall.type == Settings.HERO_BOSS_WALL \
                        or wall.type == Settings.ENEMY_BOSS_WALL:
                    self.player1.is_hit_wall = True
                    # 移出墙内
                    self.player1.move_out_wall(wall)
        # 子弹击中、敌方坦克碰撞、敌我坦克碰撞
        pygame.sprite.groupcollide(self.player2.bullets, self.player1.bullets, True, True)
        # 敌方子弹击中我方
        for bullet in self.player1.bullets:
            if pygame.sprite.collide_rect(bullet, self.player2):
                bullet.kill()
                self.player2.kill()
        # 我方子弹击中敌人
        for bullet in self.player2.bullets:
            if pygame.sprite.collide_rect(bullet, self.player1):
                bullet.kill()
                self.player1.kill()

    def update_sprites(self):
        # 监听事件
        if self.player2.is_moving:
            self.player2.update()
        if self.player1.is_moving:
            self.player1.update()
        self.walls.update()
        self.player2.bullets.update()
        self.player1.bullets.update()
        self.player1.bullets.draw(self.screen)
        self.player2.bullets.draw(self.screen)
        self.screen.blit(self.player2.image, self.player2.rect)
        self.screen.blit(self.player1.image, self.player1.rect)
        self.walls.draw(self.screen)

    def run(self, game_type):
        # 双人模式类入口
        super(TankWarDouble, self).run(game_type)
