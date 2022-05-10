import pygame
from settings import Settings
from common import Common
from tank_war_single import TankWarSingle
from tank_war_double import TankWarDouble


class Button(object):
    """
    伪按钮类
    实际是文字
    """
    def __init__(self, text, color, font, y=None):
        """
        设置文字surface，并设置文字坐标
        :param text: 要显示的文本
        :param color: 文本颜色
        :param font: 字体对象
        :param y: 提供的y坐标（x坐标通过计算可得
        """
        self.surface = font.render(text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        self.x = (Settings.DISPLAY_WIDTH - self.WIDTH) // 2
        self.y = y

    def display(self, screen):
        # 把文字surface渲染在screen上
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        """
        核查鼠标位置
        :param position: 鼠标位置
        :return: 是否在文字上
        """
        # 点击有效区域，x有效区域在[x, x + button.width],y有效区域在[y, y + button.height]
        x_match = self.x < position[0] < self.x + self.WIDTH
        y_match = self.y < position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False


class Screen(object):
    """
    屏幕类
    是开始和结束屏幕的父类
    """
    def __init__(self, width, height, img, font_size):
        """
        屏幕共同的初始化
        :param width: 整个背景图片的宽
        :param height: 背景图高
        :param img: 图像地址
        :param font_size: 字体大小
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.bg = pygame.image.load(img)
        self.font_addr = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.font_addr, font_size)


class StartScreen(Screen):
    """
    开始屏幕
    """
    def __init__(self):
        super(StartScreen, self).__init__(Settings.DISPLAY_WIDTH, Settings.DISPLAY_HEIGHT, Settings.BG_IMG, 36)

    def start_screen(self):
        # 加载音乐和标题
        pygame.mixer.music.load(Settings.BG_MUS)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        game_title = self.font.render("BATTLE OF TANKS", True, Settings.WHITE)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        # 加载按钮
        single_button = Button("Single", Settings.WHITE, self.font, y=400)
        double_button = Button("Double", Settings.WHITE, self.font, y=450)
        # 渲染按钮
        single_button.display(self.screen)
        double_button.display(self.screen)

        pygame.display.update()

        while True:
            # 监听鼠标移动，到文字那就变红
            if single_button.check_click(pygame.mouse.get_pos()):
                single_button = Button("Single", Settings.RED, self.font, 400)
            else:
                single_button = Button("Single", Settings.WHITE, self.font, 400)
            if double_button.check_click(pygame.mouse.get_pos()):
                double_button = Button("Double", Settings.RED, self.font, 450)
            else:
                double_button = Button("Double", Settings.WHITE, self.font, 450)

            single_button.display(self.screen)
            double_button.display(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Common.game_over()
            # 如果左键被按下
            if pygame.mouse.get_pressed()[0]:

                if single_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarSingle()
                    tank_war.run("S")
                if double_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarDouble()
                    tank_war.run("D")


class AfterScreen(Screen):
    """
    结束屏幕
    包括输和赢
    """
    def __init__(self):
        super(AfterScreen, self).__init__(Settings.DISPLAY_WIDTH, Settings.DISPLAY_HEIGHT, Settings.BG_IMG, 72)

    def set_same_button(self):
        # 设置输赢的页面按钮
        again_single_button = Button("AgainSingle", Settings.WHITE, self.font, y=390)
        again_double_button = Button("AgainDouble", Settings.WHITE, self.font, y=470)
        home_button = Button("Home", Settings.WHITE, self.font, y=550)
        exit_button = Button("Exit", Settings.WHITE, self.font, y=630)

        again_single_button.display(self.screen)
        again_double_button.display(self.screen)
        home_button.display(self.screen)
        exit_button.display(self.screen)

        pygame.display.update()

        while True:
            if again_single_button.check_click(pygame.mouse.get_pos()):
                again_single_button = Button("AgainSingle", Settings.RED, self.font, 390)
            else:
                again_single_button = Button("AgainSingle", Settings.WHITE, self.font, 390)

            if again_double_button.check_click(pygame.mouse.get_pos()):
                again_double_button = Button("AgainDouble", Settings.RED, self.font, 470)
            else:
                again_double_button = Button("AgainDouble", Settings.WHITE, self.font, 470)

            if home_button.check_click(pygame.mouse.get_pos()):
                home_button = Button("Home", Settings.RED, self.font, 550)
            else:
                home_button = Button("Home", Settings.WHITE, self.font, 550)

            if exit_button.check_click(pygame.mouse.get_pos()):
                exit_button = Button("Exit", Settings.RED, self.font, 630)
            else:
                exit_button = Button("Exit", Settings.WHITE, self.font, 630)

            again_single_button.display(self.screen)
            again_double_button.display(self.screen)
            home_button.display(self.screen)
            exit_button.display(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Common.game_over()

            if pygame.mouse.get_pressed()[0]:
                if again_single_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarSingle()
                    tank_war.run("S")
                elif again_double_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarDouble()
                    tank_war.run("D")
                elif home_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    page = StartScreen()
                    page.start_screen()
                elif exit_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()

    def win(self, winner=None):
        # 赢时的界面，包括单双人
        pygame.mixer.music.load(Settings.BG_MUS)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        if not winner:
            game_title = self.font.render("YOU WIN!", True, Settings.RED)
        else:
            game_title = self.font.render(winner + "Win!", True, Settings.WHITE)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        self.set_same_button()

    def single_lose(self):
        # 单人模式输了的界面
        pygame.mixer.music.load(Settings.OVER_MUS)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        game_title = self.font.render("YOU LOSE", True, Settings.RED)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        self.set_same_button()



