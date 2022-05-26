import pymysql


class SqlApi(object):
    """
    连接mysql，提供接口
    """
    def __init__(self):
        # 数据库连接,根据本地mysql数据库实际修改
        self.db = pymysql.connect(host="localhost", user="root", passwd="1111", database="tank_war")
        # 创建游标对象,给后面方法使用
        self.cursor = self.db.cursor()

    def check_exist(self, username):
        self.cursor.execute("SELECT count(*) FROM `user` WHERE `username` = '{}'".format(username))
        num = self.cursor.fetchall()[0][0]
        return num

    def get_pwd(self, username):
        self.cursor.execute("SELECT `password` FROM `user` WHERE `username` = '{}'".format(username))
        pwd = self.cursor.fetchall()[0][0]
        return pwd

    def get_rank(self):
        self.cursor.execute("SELECT `username`, `grade` FROM `user` ORDER BY `grade` DESC")
        lst = self.cursor.fetchall()
        return lst

    def get_grade(self, username):
        self.cursor.execute("SELECT `grade` FROM `user` WHERE `username` = '{}'".format(username))
        grade = self.cursor.fetchall()[0][0]
        return grade

    def update_grade(self, new_grade, username):
        self.cursor.execute("UPDATE `user` SET `grade` = {} WHERE `username` = '{}'".format(
            new_grade, username))
        self.db.commit()

    def register(self, username, pwd):
        self.cursor.execute("INSERT INTO `user`(`username`, `password`) VALUES ('{}', '{}')".format(username, pwd))
        self.db.commit()
