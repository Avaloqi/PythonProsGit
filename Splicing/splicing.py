import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import configparser


def configMe():
    config = configparser.RawConfigParser()
    config.add_section('Location')
    config.set('Location', 'output', outLocation)
    with open('cfg.ini', 'w') as configFile:
        config.write(configFile)


def hit():
    global on_vstack
    if not on_vstack:
        on_vstack = True
        model.set('垂直拼接')
    else:
        on_vstack = False
        model.set('水平拼接')


def make():
    global outLocation
    print('make')
    image1 = cv2.imread(image1Name)
    image2 = cv2.imread(image2Name)
    print('image1', image1.shape)
    print('image2', image2.shape)

    if outLocation == '':
        # 输出地址未选则查看配置文件内是否保存有地址
        config = configparser.ConfigParser()
        config.read('cfg.ini')
        outLocation = config.get('Location', 'output')
        if outLocation == '':
            tk.messagebox.showerror(title='Error', message='无文件输出路径')
            return
    else:
        configMe()

    print(outLocation)

    hs1, ho1, ws1, wo1 = \
        int(eh1.get()) if eh1.get() else 0, \
        int(eh2.get()) if eh2.get() else image1.shape[0], \
        int(ew1.get()) if ew1.get() else 0, \
        int(ew2.get()) if ew2.get() else image1.shape[1]

    hs2, ho2, ws2, wo2 = \
        int(eh21.get()) if eh21.get() else 0, \
        int(eh22.get()) if eh22.get() else image2.shape[0], \
        int(ew21.get()) if ew21.get() else 0, \
        int(ew22.get()) if ew22.get() else image2.shape[1]

    if (hs1 > ho1) | (ws1 > wo1) | (ho1 > image1.shape[0]) | (wo1 > image1.shape[1]):
        tk.messagebox.showerror('Error', '图片1选取范围有误')
        return
    if (hs2 > ho2) | (ws2 > wo2) | (ho2 > image2.shape[0]) | (wo2 > image2.shape[1]):
        tk.messagebox.showerror('Error', '图片2选取范围有误')
        return

    if on_vstack:  # 垂直拼接
        if wo1 - ws1 != wo2 - ws2:
            tk.messagebox.showerror('Error', '垂直拼接时图片选取宽度大小应相同')
            return
        output = np.vstack((image1[hs1:ho1, ws1:wo1], image2[hs2:ho2, ws2:wo2]))
    else:
        if ho1 - hs1 != ho2 - hs2:
            tk.messagebox.showerror('Error', '水平拼接时图片选取高度大小应相同')
            return
        output = np.hstack((image1[hs1:ho1, ws1:wo1], image2[hs2:ho2, ws2:wo2]))

    cv2.imshow('Splicing', output)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imwrite(outLocation, output)


def askFile():
    filename = tk.filedialog.askopenfilename()
    if filename != '':
        Image1Button.set('已选择')
        global image1Name
        image1Name = filename
        image = cv2.imread(filename)
        hR1.set('0~%d' % image.shape[0])
        wR1.set('0~%d' % image.shape[1])


def askFile2():
    filename = tk.filedialog.askopenfilename()
    if filename != '':
        Image2Button.set('已选择')
        global image2Name
        image2Name = filename
        image = cv2.imread(filename)
        hR2.set('0~%d' % image.shape[0])
        wR2.set('0~%d' % image.shape[1])


def choiceOutLocation():
    filename = tk.filedialog.askdirectory()
    if filename != '':
        loc.set('已选择')
        global outLocation
        outLocation = filename + '/' + 'outPut.png'
        print(outLocation)


def tk_center(width, height, screen_width, screen_height):
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    return '{}x{}+{}+{}'.format(width, height, x, y)


if __name__ == '__main__':
    image1Name = ''
    image2Name = ''
    outLocation = ''

    # 页面
    window = tk.Tk()
    window.title('Splicing')
    # window.iconbitmap('res/my.ico')   # .ico文件
    size = tk_center(400, 300, window.winfo_screenwidth(), window.winfo_screenheight())
    window.geometry(size)
    window.resizable(0, 0)  # 不允许用户拉伸窗口

    model = tk.StringVar()
    model.set('水平拼接')
    label = tk.Label(window, textvariable=model).grid(row=0, column=1)
    on_vstack = False
    button = tk.Button(window, text='切换模式', command=hit).grid(row=1, column=1)

    Image1Button = tk.StringVar()
    Image1Button.set('选择图片')
    image1Label = tk.Label(window, text='图片1').grid(row=2, column=0)
    button1 = tk.Button(window, textvariable=Image1Button, command=askFile).grid(row=2, column=1)

    hR1 = tk.StringVar()
    hLabel = tk.Label(window, text='垂直区域:').grid(row=3, column=1)
    hRange = tk.Label(window, textvariable=hR1).grid(row=4, column=1)
    eh1 = tk.Entry(window, width=6)
    eh1.grid(row=3, column=2)
    eh2 = tk.Entry(window, width=6)
    eh2.grid(row=4, column=2)
    wR1 = tk.StringVar()
    wLabel = tk.Label(window, text='水平区域:').grid(row=3, column=3)
    wRange = tk.Label(window, textvariable=wR1).grid(row=4, column=3)
    ew1 = tk.Entry(window, width=6)
    ew1.grid(row=3, column=4)
    ew2 = tk.Entry(window, width=6)
    ew2.grid(row=4, column=4)

    Image2Button = tk.StringVar()
    Image2Button.set('选择图片')
    image2Label = tk.Label(window, text='图片2').grid(row=5, column=0)
    button2 = tk.Button(window, textvariable=Image2Button, command=askFile2).grid(row=5, column=1)

    hR2 = tk.StringVar()
    hLabel2 = tk.Label(window, text='垂直区域:').grid(row=6, column=1)
    hRange2 = tk.Label(window, textvariable=hR2).grid(row=7, column=1)
    eh21 = tk.Entry(window, width=6)
    eh21.grid(row=6, column=2)
    eh22 = tk.Entry(window, width=6)
    eh22.grid(row=7, column=2)
    wR2 = tk.StringVar()
    wLabel2 = tk.Label(window, text='水平区域:').grid(row=6, column=3)
    wRange2 = tk.Label(window, textvariable=wR2).grid(row=7, column=3)
    ew21 = tk.Entry(window, width=6)
    ew21.grid(row=6, column=4)
    ew22 = tk.Entry(window, width=6)
    ew22.grid(row=7, column=4)

    loc = tk.StringVar()
    loc.set('输出路径')
    locButton = tk.Button(window, textvariable=loc, command=choiceOutLocation).grid(row=8, column=1)
    makeButton = tk.Button(window, text='开始拼接', command=make).grid(row=9, column=1)

    window.mainloop()  # 进入消息循环
