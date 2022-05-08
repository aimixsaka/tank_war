import pygame
from settings import Settings


class Common:

    @staticmethod
    def init_game():
        """
        初始化游戏的一些设置
        :return:
        """
        pygame.init()  # 初始化pygame模块
        pygame.display.set_caption(Settings.GAME_NAME)  # 设置窗口标题
        pygame.mixer.init()  # 初始化音频模块

    @staticmethod
    def game_over():
        pygame.quit()
        exit()