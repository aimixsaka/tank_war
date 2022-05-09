import pygame
from settings import Settings
from common import Common
from tank_war_single import TankWarSingle
from tank_war_double import TankWarDouble


class Button(object):
    def __init__(self, text, color, font, y=None):
        self.surface = font.render(text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        self.x = (Settings.DISPLAY_WIDTH - self.WIDTH) // 2
        self.y = y

    def display(self, screen):
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
    def __init__(self, width, height, img, font_size):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.bg = pygame.image.load(img)
        self.font_addr = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.font_addr, font_size)


class StartScreen(Screen):
    def __init__(self):
        super(StartScreen, self).__init__(Settings.DISPLAY_WIDTH, Settings.DISPLAY_HEIGHT, Settings.BG_IMG, 36)

    def start_screen(self):
        pygame.mixer.music.load(Settings.BG_MUS)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        game_title = self.font.render("BATTLE OF TANKS", True, Settings.WHITE)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))

        single_button = Button("Single", Settings.WHITE, self.font, y=400)
        double_button = Button("Double", Settings.WHITE, self.font, y=450)

        single_button.display(self.screen)
        double_button.display(self.screen)

        pygame.display.update()

        while True:
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
    def __init__(self):
        super(AfterScreen, self).__init__(Settings.DISPLAY_WIDTH, Settings.DISPLAY_HEIGHT, Settings.BG_IMG, 72)

    def set_same_button(self):
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
        pygame.mixer.music.load(Settings.BG_MUS)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        if not winner:
            game_title = self.font.render("YOU WIN!", True, Settings.WHITE)
        else:
            game_title = self.font.render(winner + "Win!", True, Settings.WHITE)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        self.set_same_button()

    def single_lose(self):
        pygame.mixer.music.load(Settings.BG_MUS)
        pygame.mixer.music.play(30)
        self.screen.blit(self.bg, (0, 0))
        game_title = self.font.render("YOU LOSE", True, Settings.WHITE)
        self.screen.blit(game_title, ((Settings.DISPLAY_WIDTH - game_title.get_width()) // 2, 200))
        self.set_same_button()



