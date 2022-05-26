import pygame
import pymysql
from settings import Settings


class Common:
    """
    工具类，提供一些pygame的静态方法
    """
    @staticmethod
    def init_game():
        """
        初始化游戏的一些设置
        """
        pygame.init()  # 初始化pygame模块
        pygame.display.set_caption(Settings.GAME_NAME)  # 设置窗口标题
        pygame.mixer.init()  # 初始化音频模块

    @staticmethod
    def game_over():
        """
        游戏结束
        """
        with open("privacy", "w") as f:
            f.write("")
        pygame.quit()
        exit()

    @staticmethod
    def get_username():
        """
        读取用户名
        :return:
        """
        with open("settings", "r") as f:
            username = f.readlines()[1]
        return username


