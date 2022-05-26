import tkinter as tk
from tkinter import messagebox
from screen import StartScreen
from PIL import Image, ImageTk
from settings import Settings
from sql_api import SqlApi


class InitScreen(object):
    def __init__(self):
        self.sql_api = SqlApi()  # 获取sql接口

        self.top = tk.Tk()  # 窗口顶层对象
        self.top.title("TANK  WAR")  # 标题
        self.top.geometry("950x600")

        self.name_label = None  # username标签栏
        self.pwd_label = None   # password标签栏
        self.grade_label = None  # 展示分数
        self.num_label = None  # 设置敌人数
        self.reg_name_label = None  # 注册提示栏
        self.reg_pwd_label = None
        self.now_num_label = None

        self.name_entry = None  # 输入框
        self.pwd_entry = None
        self.num_entry = None
        self.reg_name_entry = None
        self.reg_pwd_entry = None

        self.login_button = None  # 登录确定按钮
        self.num_button = None  # 敌人数设置确定按钮
        self.register_button = None  # 注册确定按钮

        self.canvas = tk.Canvas(self.top, width=950, height=600)
        self.img = ImageTk.PhotoImage(Image.open(Settings.INIT_IMG))
        self.canvas.create_image(475, 300, image=self.img)
        self.canvas.pack()

    def login(self):
        self.name_label = tk.Label(self.top, text="请输入用户名： ")
        self.pwd_label = tk.Label(self.top, text="请输入密码： ")
        self.login_button = tk.Button(self.top, text="登录", command=self.check_login)
        self.name_entry = tk.Entry(self.top)
        self.pwd_entry = tk.Entry(self.top)
        # 把组件放在画布上
        self.canvas.create_window(475, 10, width=200, height=20, window=self.name_label)
        self.canvas.create_window(475, 30, width=200, height=20, window=self.name_entry)
        self.canvas.create_window(475, 50, width=200, height=20, window=self.pwd_label)
        self.canvas.create_window(475, 70, width=200, height=20, window=self.pwd_entry)
        self.canvas.create_window(475, 90, width=70, height=30, window=self.login_button)

    def check_login(self):
        username = self.name_entry.get()
        password = self.pwd_entry.get()
        num = self.sql_api.check_exist(username)
        if num:
            pwd = self.sql_api.get_pwd(username)
            if password == pwd:
                with open("privacy", "w") as f:
                    f.write(username)
                self.top.destroy()
                start = StartScreen()
                start.start_screen()
            else:
                self.pwd_entry.delete(0, tk.END)
                messagebox.showerror("密码错误")
        else:
            messagebox.showerror("该用户不存在")

    def register(self):
        self.reg_name_label = tk.Label(self.top, text="用户名")
        self.reg_pwd_label = tk.Label(self.top, text="密码")
        self.reg_name_entry = tk.Entry(self.top)
        self.reg_pwd_entry = tk.Entry(self.top)
        self.register_button = tk.Button(self.top, text="注册", command=self.check_register)

        self.canvas.create_window(475, 200, width=200, height=20, window=self.reg_name_label)
        self.canvas.create_window(475, 220, width=200, height=20, window=self.reg_name_entry)
        self.canvas.create_window(475, 240, width=200, height=20, window=self.reg_pwd_label)
        self.canvas.create_window(475, 260, width=200, height=20, window=self.reg_pwd_entry)
        self.canvas.create_window(475, 285, width=70, height=30, window=self.register_button)

    def check_register(self):
        name = self.reg_name_entry.get()
        pwd = self.reg_pwd_entry.get()
        num = self.sql_api.check_exist(name)
        if not num:
            if 4 < len(pwd) < 18:
                self.sql_api.register(name, pwd)
                messagebox.showinfo("注册成功，请登录进入游戏")
                self.reg_name_entry.delete(0, tk.END)
                self.reg_pwd_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("密码长度必须大于4小于18")
        else:
            messagebox.showerror("该用户名已被占用")

    def show_grades(self):
        lst = self.sql_api.get_rank()
        s = "=====排名======\n"
        n = 1
        for name, grade in lst:
            s += "第{}名： {}     {}\n".format(n, name, grade)
            n += 1
        self.grade_label = tk.Label(self.top, text=s)
        self.canvas.create_window(80, 80, width=150, height=600, window=self.grade_label)

    def set(self):
        self.num_label = tk.Label(self.top, text="请输入预期的敌人数")
        self.num_entry = tk.Entry(self.top)
        self.num_button = tk.Button(self.top, text="确定", command=self.check_num)
        with open("settings", "r") as f:
            num = f.read()
        self.now_num_label = tk.Label(self.top, text="现敌人数： {}".format(num))
        self.canvas.create_window(850, 20, width=200, height=40, window=self.num_label)
        self.canvas.create_window(850, 60, width=100, height=30, window=self.num_entry)
        self.canvas.create_window(850, 95, width=70, height=30, window=self.num_button)
        self.canvas.create_window(850, 150, width=100, height=30, window=self.now_num_label)

    def check_num(self):
        num = self.num_entry.get()
        if num:
            with open("settings", "w") as f:
                f.write(num)
            messagebox.showinfo("修改成功")
        else:
            messagebox.showerror("输入为空")

    def start(self):
        self.set()
        self.login()
        self.register()
        self.show_grades()
        self.show_grades()
        self.top.mainloop()


