"""
    禁忌搜索解决TSP问题（原创 99%）
    14个城市预计迭代1400~1500次
"""
import os
import sys
import time
from tkinter import messagebox

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk

import CityInfor
import TabuSearch
import DrawInfor


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':

    # # 指定城市数据
    # X = pd.read_excel("./data/City3.xlsx", header=None)
    # X = np.array(X)
    # # 指定起点
    # beginCity = 12
    # beginCity
    #
    # # 随机城市个数
    # citySize = np.random.randint(100)
    # citySize = 11
    # # 随机城市坐标
    # np.random.seed(0)
    # X = np.random.rand(citySize, 2) * 100
    # X
    #
    # # 随机起点
    # beginCity = np.random.randint(X.shape[0])
    # beginCity
    #
    # X_excel = pd.DataFrame(X)
    # X_excel.to_excel('./data/X.xlsx')
    # np.savetxt('./data/beginCity.txt', [beginCity], fmt='%f', delimiter=' ')

    np.set_printoptions(suppress=True)  # 取消np的科学计数法

    # 为0则是用例子
    isnotExampleFlag = 0
    isnotRanbeginFlag = 0
    isnotTabooPeriodM = 0

    # TK可视化
    """
        GUI参数设置
    """
    # 方法
    def take_Example(*args):
        selected_option = cityOption.get()
        cityName.set(selected_option)

    # 起点单选
    def show_selected_option_TabooPerio():
        global isnotTabooPeriodM
        selected_option = var_TabooPeriod.get()

        # 如果为1，则使用例子
        if selected_option == 1:
            isnotTabooPeriodM = 1
            # 初始化时显示组件
            label_TabooPeriod.grid(row=5, column=0, columnspan=1, padx=10, pady=15)
            entry_TabooPeriod.grid(row=5, column=1, columnspan=2, padx=10, pady=15)

        else:
            isnotTabooPeriodM = 0
            label_TabooPeriod.grid_forget()
            entry_TabooPeriod.grid_forget()

    def show_selected_option_beginCity():
        global isnotRanbeginFlag
        selected_option = var_beginCity.get()

        # 如果为1，则使用例子城市
        if selected_option == 1:
            isnotRanbeginFlag = 1
            # 初始化时显示组件
            label_beginCity.grid(row=3, column=0, columnspan=1, padx=10, pady=15)
            entry_beginCity.grid(row=3, column=1, columnspan=2, padx=10, pady=15)

        else:
            isnotRanbeginFlag = 0
            label_beginCity.grid_forget()
            entry_beginCity.grid_forget()


    def show_selected_option():
        global isnotExampleFlag
        selected_option = var_city.get()

        # 如果为1，则使用例子城市
        if selected_option == 1:
            isnotExampleFlag = 1
            entry_citySize.grid_forget()
            label_citySize.grid_forget()
            label_options.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
            option_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=10)

        else:
            isnotExampleFlag = 0
            label_options.grid_forget()
            option_menu.grid_forget()
            label_citySize.grid(row=1, column=0, columnspan=1, padx=10, pady=15)
            entry_citySize.grid(row=1, column=1, columnspan=1, padx=10, pady=15)


    def set_parameter():
        try:
            citySizeP = int(entry_citySize.get())
            citySize.set(citySizeP)
            # 从Entry获取输入的值并更新变量的值
            # 获取城市个数
            if var_city.get()==0:
                # 随机
                # 城市大小
                if int(citySize.get()) <5:
                    citySize.set(0)
                    raise ValueError("城市个数小于5还需要搜索？")
                citySizeP = int(entry_citySize.get())
                citySize.set(citySizeP)
            else:
                if cityName.get()=="City1.xlsx" or cityName.get()=="City2.xlsx":
                    citySize.set(14)
                elif cityName.get()=="City3.xlsx":
                    citySize.set(34)
                elif cityName.get()=="City4.xlsx":
                    citySize.set(31)

            beginCityP = int(entry_beginCity.get())
            beginCity.set(beginCityP)
            #起点要小于城市个数-1
            if var_beginCity.get()==1 and ((beginCity.get()>=citySize.get()) or beginCity.get()<0):
                beginCity.set(0)
                raise ValueError("起点位置错误！")

            TabooPeriodP = int(entry_TabooPeriod.get())
            TabooPeriod.set(TabooPeriodP)
            if var_TabooPeriod.get()==1 and (TabooPeriod.get()<=0):
                TabooPeriod.set(0)
                raise ValueError("禁忌期限要大于0，而且为int！")

            if float(interval.get())<=0:
                interval.set(0.01)
                raise ValueError("迭代速度要大于0ms！")
            else:
                # 间隔时间
                intervalP = entry_interval.get()
                interval.set(intervalP)


            root.destroy()

        except ValueError as e:
            messagebox.showwarning("错误赋值警告","严重的赋值错误！\n"+f"{e}")
        except Exception as e:
            messagebox.showwarning("错误赋值警告",f"{e}")

    def quit_proccess():
        root.destroy()
        sys.exit()

        # 可视化内容
    # 创建Tkinter窗口
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', quit_proccess)
    # 创建一个IntVar变量，用于保存选中的选项的索引
    var_city = tk.IntVar()

    # 设置默认选项的索引
    var_city.set(0)

    # 城市生成单选按钮
    radiobutton_show_entry = tk.Radiobutton(root, text="随机城市", variable=var_city, value=0, command=show_selected_option)
    radiobutton_show_entry.grid(row=0, column=0, columnspan=1, padx=10, pady=15)

    radiobutton_show_option_menu = tk.Radiobutton(root, text="例子城市", variable=var_city, value=1, command=show_selected_option)
    radiobutton_show_option_menu.grid(row=0, column=1, columnspan=1, padx=10, pady=15)

    # 选择后的展示
    # 定义例子选项
    cityName = tk.StringVar()
    cityName.set("City1.xlsx")
    label_options = tk.Label(root, text="选择例子城市：")
    cityOptions = ["City1.xlsx", "City2.xlsx", "City3.xlsx", "City4.xlsx"]
    # 创建一个StringVar变量，用于保存选中的选项
    cityOption = tk.StringVar(root)
    cityOption.set(cityOptions[0])  # 设置默认选项
    # 创建OptionMenu，并将其与StringVar绑定
    option_menu = tk.OptionMenu(root, cityOption, *cityOptions, command=take_Example)

    # 输入随机城市个数
    citySize = tk.IntVar()
    citySize.set(0)
    label_citySize = tk.Label(root, text="随机城市个数：")
    entry_citySize = tk.Entry(root, textvariable=citySize, width=15)

    # 初始化时默认显示Entry组件
    label_citySize.grid(row=1, column=0, columnspan=1, padx=10, pady=15)
    entry_citySize.grid(row=1, column=1, columnspan=2, padx=10, pady=15)

    # 创建一个IntVar变量，用于保存选中的选项的索引
    var_beginCity = tk.IntVar()

    # 设置默认选项的索引
    var_beginCity.set(1)

    # 城市起点单选按钮
    radiobutton_show_entry_beginCityRan = tk.Radiobutton(root, text="随机起点", variable=var_beginCity, value=0,
                                            command=show_selected_option_beginCity)
    radiobutton_show_entry_beginCityRan.grid(row=2, column=0, columnspan=1, padx=10, pady=15)

    radiobutton_show_beginCity = tk.Radiobutton(root, text="自定义起点", variable=var_beginCity, value=1,
                                                  command=show_selected_option_beginCity)
    radiobutton_show_beginCity.grid(row=2, column=1, columnspan=1, padx=10, pady=15)

    # 输入城市的起点
    beginCity = tk.IntVar()
    beginCity.set(0)
    label_beginCity = tk.Label(root, text="城市起点(int)：")
    entry_beginCity = tk.Entry(root, textvariable=beginCity, width=15)

    # 初始化时显示组件
    label_beginCity.grid(row=3, column=0, columnspan=1, padx=10, pady=15)
    entry_beginCity.grid(row=3, column=1, columnspan=2, padx=10, pady=15)

    # 创建一个IntVar变量，用于保存选中的选项的索引
    var_TabooPeriod = tk.IntVar()

    # 设置默认选项的索引
    var_TabooPeriod.set(1)

    # 禁忌期限单选按钮
    radiobutton_show_entry_TabooPeriodM = tk.Radiobutton(root, text="默认禁忌期限", variable=var_TabooPeriod, value=0,
                                                      command=show_selected_option_TabooPerio)
    radiobutton_show_entry_TabooPeriodM.grid(row=4, column=0, columnspan=1, padx=10, pady=15)

    radiobutton_show_TabooPerio = tk.Radiobutton(root, text="自定义禁忌期限", variable=var_TabooPeriod, value=1,
                                                  command=show_selected_option_TabooPerio)
    radiobutton_show_TabooPerio.grid(row=4, column=1, columnspan=1, padx=10, pady=15)

    # 输入禁忌期限
    TabooPeriod = tk.IntVar()
    TabooPeriod.set(0)
    label_TabooPeriod = tk.Label(root, text="禁忌期限(int)：")
    entry_TabooPeriod = tk.Entry(root, textvariable=TabooPeriod, width=15)

    # 初始化时显示组件
    label_TabooPeriod.grid(row=5, column=0, columnspan=1, padx=10, pady=15)
    entry_TabooPeriod.grid(row=5, column=1, columnspan=2, padx=10, pady=15)

    # 画图间隔时间
    interval = tk.StringVar()
    interval.set("0.01")
    label_interval = tk.Label(root, text="画图速度(ms)：")
    label_interval.grid(row=6, column=0, columnspan=1, padx=10, pady=15)
    # 创建一个Entry小部件，将其与StringVar绑定
    entry_interval = tk.Entry(root, textvariable=interval, width=15)
    entry_interval.grid(row=6, column=1, columnspan=1, padx=10, pady=15)


    # 创建一个按钮开始
    TSbegin_button = tk.Button(root, text="开始禁忌搜索", command=set_parameter)
    TSbegin_button.grid(row=10, column=0, columnspan=2, padx=10, pady=20)



    # 创建一个按钮开始
    # TSbegin_button = tk.Button(root, text="退出程序", command=quit_proccess)
    # TSbegin_button.grid(row=11, column=0, columnspan=2, padx=10, pady=20)

    root.title("TS参数设置")
    # 让窗口居中
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    # 禁止用户调整窗口大小
    root.resizable(False, False)

    # 运行Tkinter主循环
    root.mainloop()

    np.random.seed(int(time.time()))
    X = None
    # 城市的选择
    if isnotExampleFlag == 0:
        # 随机
        citySize = int(citySize.get())
        # 随机城市坐标
        X = np.random.rand(citySize, 2) * 100
    else:
        # 不随机
        cityName = str(cityName.get())
        cityPath = "./data/"+cityName
        # 指定城市数据
        X = pd.read_excel(cityPath, header=None)
        X = np.array(X)

    # print(X)
    # X_excel = pd.DataFrame(X)
    # X_excel.to_excel('./data/X.xlsx', header=None,index=None)


    # 起点的选择
    if isnotRanbeginFlag == 0:
        # 随机起点
        beginCity = np.random.randint(X.shape[0])
    else:
        # 不随机
        beginCity = int(beginCity.get())

    # print(beginCity)
    # np.savetxt('./data/beginCity.txt', [beginCity], fmt='%f', delimiter=' ')

    # 禁忌期限的选择
    if isnotTabooPeriodM == 0:
        # 默认起点
        TabooPeriod = None
    else:
        # 不随机
        TabooPeriod = int(TabooPeriod.get())


    # print(TabooPeriod)

    interval = float(interval.get())/1000



    # 传入城市坐标和起点位置即可，不传入有默认值，开启testflag = 1则使用测试数据
    CT = CityInfor.City(X = X,beginCity = beginCity,testflag = 0)

    # 个城市坐标位置X,可以换成load CityPosition1.mat
    # CT.X
    # CT.D
    # CT.citySize
    # CT.beginCity

    # 传入城市信息的对象和禁忌期限(默认大于总城市数3/4)，初始化禁忌搜素
    TS = TabuSearch.TabuSearch(CT,TabooPeriod = TabooPeriod,testflag = 0)
    # TS.TabooPeriod
    # TS.H_val
    # TS.path_i
    # TS.path_s
    # TS.f_i
    # TS.f_s

    # 可视化画图
    VD = DrawInfor.DrawInfor(CT,TS)

    root = tk.Tk()
    root.title("程序控制")

    running = False
    paused = False
    counter = 0


    def loop():
        global running, paused, counter
        if running and not paused:
            if TS.overTebuSearch() > TS.circSize:
                VD.ClearPathI()
                plt.pause(0)
            TS.iterations += 1
            TS.AspirationCriteria() # 渴望准则
            isNewPathS = TS.NBIteration(CT.D, CT.beginCity)  # 邻域操作

            VD.DisplayPathI(CT.X, TS.path_i)

            if isNewPathS == 1:
                VD.DisplayPathS(CT.X, TS.path_s)
            VD.DisplayFS(TS.iterations, TS.f_s)
            VD.DisplayFI(TS.iterations, TS.f_i)
            plt.pause(interval)  # 画图速度

        root.after(0, loop)  # 调整时间间隔为500毫秒，控制循环速度

    def start_loop():
        global running, paused
        running = True
        paused = False
        loop()

    def stop_loop():
        global running
        running = False


    def restart_program():
        root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)


    def exit_program():
        root.destroy()
        sys.exit()


    # 创建按钮
    start_button = tk.Button(root, text="开始", command=start_loop)
    start_button.pack(side="left")

    stop_button = tk.Button(root, text="停止", command=stop_loop)
    stop_button.pack(side="left")

    restart_button = tk.Button(root, text="重启", command=restart_program)
    restart_button.pack(side="left")

    exit_button = tk.Button(root, text="退出", command=exit_program)
    exit_button.pack(side="left")

    # 让窗口居中
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 12) - (width // 12)
    y = (root.winfo_screenheight() // 15) - (height // 15)
    root.geometry(f"{width+50}x{height+50}+{x}+{y}")
    # 禁止用户调整窗口大小
    root.resizable(False, False)

    # 运行主循环
    root.mainloop()


    # while TS.overTebuSearch()<=TS.circSize:
    #
    #     TS.iterations += 1
    #     # print('第{}次迭代:'.format(TS.iterations))
    #     # print("当前的迭代位置:"+str(TS.iterOver))
    #     # print("走过的路径:")
    #     # print(TS.passPath)
    #     # # 渴望准则
    #     # print("准则解禁:")
    #      # print(TS.AspirationCriteria()) # 渴望准则
    #     isNewPathS = TS.NBIteration(CT.D, CT.beginCity)# 邻域操作
    #     # print("当代的最后信息_i：")
    #     # print(TS.f_i)
    #     # print(TS.path_i)
    #     # print('当前禁忌对象有：')
    #     # print(TS.displayTabooObj())
    #     # print("被禁忌的对象长度：")
    #     # print(TS.H_val)
    #     VD.DisplayPathI(CT.X, TS.path_i)
    #
    #     # 与最优值的比较，保存全局最优解
    #     # print("当前最优解")
    #     # print(TS.path_s)
    #     # print(TS.f_s)
    #     if isNewPathS == 1:
    #         VD.DisplayPathS(CT.X,TS.path_s)
    #     VD.DisplayFS(TS.iterations,TS.f_s)
    #     VD.DisplayFI(TS.iterations,TS.f_i)
    #     plt.pause(interval) # 画图速度
    #
    #     # print('-'*20)
    # # 清空局部最优画图
    # VD.ClearPathI()
    # plt.pause(0)






