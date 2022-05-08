from PIL import Image
import os


# 处理图片大小的工具
files = os.listdir("./imgs")

for file in files:
    if not file.endswith(".py"):
        img = Image.open("./imgs/" + file)
        img = img.resize((40, 40))
        img.save(file)
