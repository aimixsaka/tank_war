import PySimpleGUI as sg
import os


def func():
    """
    地图绘制的工具类，
    可以不调用
    :return :
    """
    path = r"D:\PythonCode\python\workspace\tank_war\tank_war\tools\resources\images\walls"
    files = [path + "\\" + file for file in os.listdir(path)]

    sg.Image()

    layout = [
        [sg.Image(files[0], size=(30, 30), enable_events=True) for i in range(19)] for j in range(15)
    ]
    layout.append([sg.Button("保存地图"), sg.Button("刷新"), sg.Button("退出")])

    window = sg.Window("绘制地图", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "退出":
            break
        if event in (None, "刷新"):
            window.refresh()
        elif event in range(285):
            print(event)
            elem = window.find_element(event)
            num = elem.Filename.split("\\")[-1].split(".")[0]
            num = (int(num) + 1) % 5
            elem.Filename = files[num]
            elem.Update(files[num], size=(30, 30))
            window.refresh()
        elif event in (None, "保存地图"):
            lines = []
            line = []
            img = 0
            for i in range(15):
                for j in range(19):
                    elem = window.find_element(img)
                    num = elem.Filename.split("\\")[-1].split(".")[0]
                    line.append(num)
                    img += 1
                lines.append(line)
                line = []

            content = "["
            for line in lines:
                content += "["
                for num in line:
                    content += num + ","
                content += "],\n"
            content += "]"

            with open("map.txt", "w") as f:
                f.write(content)


if __name__ == "__main__":
    func()