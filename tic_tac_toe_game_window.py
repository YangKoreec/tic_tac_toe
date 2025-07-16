import numpy as np
from tkinter import *
from PIL import Image, ImageTk


class TTTWindow():
    def __init__(self):
        self.window = Tk() # Создание окна

        # Черная сетка между кнопками
        self.black_grid = Canvas(self.window, bg='black', width=230, height=230) # Создание чёрного холста поверх, которого будут кнопки

        # Изображения для кнопок
        self.start_img = ImageTk.PhotoImage(Image.new('RGB', (70, 70), color='white')) # Пустая кнопка
        self.red_cross_img = ImageTk.PhotoImage(file='red_cross.png') # Крестик
        self.blue_circle_img = ImageTk.PhotoImage(file='blue_circle.png') # Нолик

        # Создание кнопок, которые будут выполнять роль ячеек игрового поля
        self.buttons = [Button(self.black_grid, # Прикрепляем кнопки к окну
                               activebackground='white', # Цвет кнопки при наведении на нее курсора
                               image=self.start_img,
                               width=70, # Высота кнопки в пикселях
                               height=70, # Ширина кнопки в пикселях
                               relief='flat', # Столь кнопки
                               bd=0, # Размер рамки кнопки в пикселях
                               command=lambda i=num: self.button_click(i)) # Передача функции при нажатии, используется лямбда-функция, так как необходимо передать
                                                                         # в функцию номер кнопки. i=num используется, чтобы избежать позднего связываения.
                        for num in range(0, 9)]

        # Параметры окна
        self.window.title("Крестики-Нолики") # Имя окна
        self.window.geometry('640x480') # Размер окна в пикселях

        # Размещение холста для кнопок
        self.black_grid.place(x=200, y=100)

        # Размещение кнопок
        i = 0 # Счетчик для отступа по оси X
        j = 0 # Счетчик для отступа по оси Y
        for button in self.buttons:
            x = 42 + 75 * (i % 3) # Вычисление положения кнопки по оси X относительно начала
            y = 42 + 75 * j # Вычисление положения кнопки по оси Y относительно начала
            self.black_grid.create_window(x, y, window=button) # Расположение кнопки на окне
            i += 1
            if i % 3 == 0:
                j += 1

    # Метод для вывода окна на экран
    def show(self):
        self.window.mainloop() # Вывод окна

    def button_click(self, num):
        self.buttons[num].configure(image=self.blue_circle_img)