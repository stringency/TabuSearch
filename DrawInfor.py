"""
    可视化画图
"""
import sys

import matplotlib
import numpy as np
import matplotlib.pyplot as plt


class DrawInfor(object):
    # 画图
    cityPic = None
    FIPic = None
    FSPic = None

    # 数据
    fsSite = None
    fiSite = None

    def __init__(self, CT, TS):
        # 动态城市图初始化
        self.cityPic = plt.figure('city', figsize=(16, 7))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.ion()
        plt.subplot(1, 3, 1)
        plt.xlabel("城市x坐标")
        plt.ylabel("城市y坐标")
        plt.title("TS动态搜索图")
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.1, hspace=0.2)

        # 数据初始化
        self.fsSite = [[0, 1], [0, TS.f_s]]
        self.fiSite = [[0, 1], [0, TS.f_i]]

        # 起点城市
        plt.scatter(CT.X[:, 0], CT.X[:, 1], c='k', marker='v', s=28, label='citySite')
        plt.scatter(CT.X[CT.beginCity][0], CT.X[CT.beginCity][1], c='purple', marker='^', edgecolors='k', s=130,
                    label='beginCitySite')
        # 标记城市名称
        for i in range(CT.citySize):
            plt.text(CT.X[i][0] + 0.05, CT.X[i][1] + 0.05, str(i), c='g', label='cityName')

        plt.plot(np.r_[CT.X[TS.path_s][:, 0], CT.X[CT.beginCity][0]],
                 np.r_[CT.X[TS.path_s][:, 1], CT.X[CT.beginCity][1]], c='r', label='DrawPS')
        plt.plot(np.r_[CT.X[TS.path_i][:, 0], CT.X[CT.beginCity][0]],
                 np.r_[CT.X[TS.path_i][:, 1], CT.X[CT.beginCity][1]], c='r', alpha=0.5, label='DrawPI')

        fig = plt.gcf()
        # 获取屏幕的宽度和高度
        screen_width = fig.canvas.manager.window.winfo_screenwidth()
        screen_height = fig.canvas.manager.window.winfo_screenheight()

        # 获取图形窗口的宽度和高度
        fig_width, fig_height = fig.get_size_inches() * fig.dpi

        # 计算居中的坐标
        center_x = (screen_width - fig_width) / 2
        center_y = (screen_height - fig_height) / 2

        # 设置窗口位置
        fig.canvas.manager.window.geometry(f"{int(fig_width)}x{int(fig_height)}+{int(center_x)}+{int(center_y)}")

    # 可视化最佳适应度变化
    def DisplayFS(self, iterations, f_s):
        # self.FSPic = plt.figure('FS')
        plt.subplot(1, 3, 3)
        plt.xlabel("迭代次数")
        plt.ylabel("路径长度")
        plt.title("Path_S最佳路径展示")
        self.fsSite[0][0] = self.fsSite[0][1]
        self.fsSite[1][0] = self.fsSite[1][1]
        self.fsSite[0][1] = iterations
        self.fsSite[1][1] = f_s
        plt.plot(self.fsSite[0], self.fsSite[1])

    # 可视化动态寻找路径的适应度变化
    def DisplayFI(self, iterations, f_i):
        # self.FIPic = plt.figure('FI')
        plt.subplot(1, 3, 2)
        plt.xlabel("迭代次数")
        plt.ylabel("路径长度")
        plt.title("Path_I当前迭代最佳路径展示")
        self.fiSite[0][0] = self.fiSite[0][1]
        self.fiSite[1][0] = self.fiSite[1][1]
        self.fiSite[0][1] = iterations
        self.fiSite[1][1] = f_i
        plt.plot(self.fiSite[0], self.fiSite[1])

    # 可视化最佳路径
    def DisplayPathS(self, X, path_s):
        # plt.figure('city')
        plt.subplot(1, 3, 1)
        plt.title("TS动态搜索图.当前最短路径:{}".format(self.fsSite[1][1]))
        # 清空旧的path_s
        lines = plt.gca().lines
        for line in lines:
            if line.get_label() == 'DrawPS':
                line.remove()
        plt.plot(np.r_[X[path_s][:, 0], X[path_s[0]][0]], np.r_[X[path_s][:, 1], X[path_s[0]][1]], c='r',
                 label='DrawPS')

    # 可视化动态寻找路径过程
    def DisplayPathI(self, X, path_i):
        # plt.figure('city')
        plt.subplot(1, 3, 1)
        # 清空旧的path_s
        lines = plt.gca().lines
        for line in lines:
            if line.get_label() == 'DrawPI':
                line.remove()
        plt.plot(np.r_[X[path_i][:, 0], X[path_i[0]][0]], np.r_[X[path_i][:, 1], X[path_i[0]][1]], c='b',
                 alpha=0.4, label='DrawPI')

    def ClearPathI(self):
        plt.figure('city')
        plt.subplot(1, 3, 1)
        # 清空旧的path_s
        lines = plt.gca().lines
        for line in lines:
            if line.get_label() == 'DrawPI':
                line.remove()
