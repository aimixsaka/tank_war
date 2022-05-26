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
    def __init__(self, text, color, font_size, y=None):
        """
        设置文字surface，并设置文字坐标
        :param text: 要显示的文本
        :param color: 文本颜色
        :param font_size: 字体对象
        :param y: 提供的y坐标（x坐标通过计算可得
        """
        self.font_addr = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.font_addr, font_size)

        self.surface = self.font.render(text, True, color)

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
    def __init__(self, width, height, img, font_size, single_text, double_text, exit_text, size, single_y,
                 double_y, exit_y, single_color=Settings.WHITE, double_color=Settings.WHITE, exit_color=Settings.WHITE):
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
        self.single_text = single_text
        self.double_text = double_text
        self.exit_text = exit_text
        self.size = size
        self.single_y = single_y
        self.double_y = double_y
        self.exit_y = exit_y
        self.single_color = single_color
        self.double_color = double_color
        self.exit_color = exit_color
        self.single_button = None
        self.double_button = None
        self.exit_button = None

    def set_button(self):
        self.single_button = Button(self.single_text, self.single_color, self.size, self.single_y)
        self.double_button = Button(self.double_text, self.double_color, self.size, self.double_y)
        self.exit_button = Button(self.exit_text, self.exit_color, self.size, self.exit_y)
        self.single_button.display(self.screen)
        self.double_button.display(self.screen)
        self.exit_button.display(self.screen)

    def check_click(self):
        while True:
            # 监听鼠标移动，到文字那就变红
            if self.single_button.check_click(pygame.mouse.get_pos()):
                self.single_button = Button(self.single_text, Settings.RED, self.size, self.single_y)
            else:
                self.single_button = Button(self.single_text, Settings.WHITE, self.size, self.single_y)
            if self.double_button.check_click(pygame.mouse.get_pos()):
                self.double_button = Button(self.double_text, Settings.RED, self.size, self.double_y)
            else:
                self.double_button = Button(self.double_text, Settings.WHITE, self.size, self.double_y)
            if self.exit_button.check_click(pygame.mouse.get_pos()):
                self.exit_button = Button(self.exit_text, Settings.RED, self.size, self.exit_y)
            else:
                self.exit_button = Button(self.exit_text, Settings.WHITE, self.size, self.exit_y)

            self.single_button.display(self.screen)
            self.double_button.display(self.screen)
            self.exit_button.display(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Common.game_over()
            # 如果左键被按下
            if pygame.mouse.get_pressed()[0]:

                if self.single_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarSingle()
                    tank_war.run("S")
                if self.double_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarDouble()
                    tank_war.run("D")
                if self.exit_button.check_click(pygame.mouse.get_pos()):
                    Common.game_over()


class StartScreen(Screen):
    """
    开始屏幕
    """
    def __init__(self):
        super(StartScreen, self).__init__(Settings.DISPLAY_WIDTH, Settings.DISPLAY_HEIGHT, Settings.BG_IMG, 36,
                                          "Single", "Double", "Exit", 33, 400, 450, 500)

    def start_screen(self):
        # 加载音乐和标题
        pygame.mixer.music.load(Settings.NEW_START)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        game_title = self.font.render("BATTLE OF TANKS", True, Settings.WHITE)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        # 加载按钮
        super().set_button()
        super().check_click()


class AfterScreen(Screen):
    """
    结束屏幕
    包括输和赢
    """
    def __init__(self):
        super(AfterScreen, self).__init__(Settings.DISPLAY_WIDTH, Settings.DISPLAY_HEIGHT, Settings.BG_IMG, 72,
                                          "AgainSingle", "AgainDouble", "Exit", 40, 390, 470, 630)
        self.home_button = None
        self.again_single_button = None
        self.again_double_button = None

    def start_screen(self):
        # 设置输赢的页面按钮
        super(AfterScreen, self).set_button()
        self.home_button = Button("Home", Settings.WHITE, self.size, 550)
        self.home_button.display(self.screen)

        while True:
            # 监听鼠标移动，到文字那就变红
            if self.single_button.check_click(pygame.mouse.get_pos()):
                self.single_button = Button(self.single_text, Settings.RED, self.size, self.single_y)
            else:
                self.single_button = Button(self.single_text, Settings.WHITE, self.size, self.single_y)
            if self.double_button.check_click(pygame.mouse.get_pos()):
                self.double_button = Button(self.double_text, Settings.RED, self.size, self.double_y)
            else:
                self.double_button = Button(self.double_text, Settings.WHITE, self.size, self.double_y)
            if self.exit_button.check_click(pygame.mouse.get_pos()):
                self.exit_button = Button(self.exit_text, Settings.RED, self.size, self.exit_y)
            else:
                self.exit_button = Button(self.exit_text, Settings.WHITE, self.size, self.exit_y)
            if self.home_button.check_click(pygame.mouse.get_pos()):
                self.home_button = Button("Home", Settings.RED, self.size, 550)
            else:
                self.home_button = Button("Home", Settings.WHITE, self.size, 550)

            self.single_button.display(self.screen)
            self.double_button.display(self.screen)
            self.home_button.display(self.screen)
            self.exit_button.display(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Common.game_over()
            # 如果左键被按下
            if pygame.mouse.get_pressed()[0]:
                if self.single_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarSingle()
                    tank_war.run("S")
                if self.double_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    tank_war = TankWarDouble()
                    tank_war.run("D")
                if self.home_button.check_click(pygame.mouse.get_pos()):
                    pygame.quit()
                    start = StartScreen()
                    start.start_screen()
                if self.exit_button.check_click(pygame.mouse.get_pos()):
                    Common.game_over()

    def win(self, winner=None):
        # 赢时的界面，包括单双人
        pygame.mixer.init()
        pygame.mixer.music.load(Settings.NEW_START)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        if not winner:
            game_title = self.font.render("YOU WIN!", True, Settings.RED)
        else:
            game_title = self.font.render(winner + "Win!", True, Settings.RED)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        self.start_screen()

    def single_lose(self):
        # 单人模式输了的界面
        pygame.mixer.init()
        pygame.mixer.music.load(Settings.OVER_MUS)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        game_title = self.font.render("YOU LOSE", True, Settings.RED)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        self.start_screen()



