import numpy as np
import pandas as pd
from tkinter import *
from PIL import Image, ImageTk


class TTTWindow():
    def __init__(self):
        self.window = Tk() # Создание окна
        self.game_cells = np.zeros(9) # Массив хранящий текущее состояние игрового поля (0 - пустая клетка, 1 - крестик, 2 - нолик)
        self.game_logs = pd.DataFrame(
            {'name': [], 'figure': [], 'move': [], 'c_0': [], 'c_1': [], 'c_2': [], 'c_3': [], 'c_4': [], 'c_5': [],
             'c_6': [], 'c_7': [], 'c_8': []}) # Таблица хранящая последовательность ходов
        self.current_move = 0 # Номер текущего хода

        # Фигуры, которыми играют пользователь и бот
        self.player_fig = 1 # То чем играет пользователь (Пользователь всегда начинает с крестиков)
        self.bot_fig = 2 # То чем играет бот (Бот всегда начинает с ноликов)

        # Черная сетка между клетками
        self.black_grid = Canvas(self.window, bg='black', width=230, height=230) # Создание чёрного холста поверх, которого будут клетки

        # Изображения для клеток
        self.start_img = ImageTk.PhotoImage(Image.new('RGB', (70, 70), color='white')) # Пустая клетка
        self.red_cross_img = ImageTk.PhotoImage(file='red_cross.png') # Крестик
        self.blue_circle_img = ImageTk.PhotoImage(file='blue_circle.png') # Нолик

        # Создание кнопок, которые будут выполнять роль клеток игрового поля
        self.buttons = [Button(self.black_grid, # Прикрепляем кнопки к холсту
                               activebackground='white', # Цвет кнопки при наведении на нее курсора
                               image=self.start_img, # Картинка белого квадрата, в качестве начального состояния кнопки
                               width=70, # Высота кнопки в пикселях
                               height=70, # Ширина кнопки в пикселях
                               relief='flat', # Стиль кнопки
                               bd=0, # Размер рамки кнопки в пикселях
                               command=lambda i=num: self.button_click(i)) # Передача функции при нажатии, используется лямбда-функция, так как необходимо передать
                                                                           # в функцию номер кнопки. i=num используется, чтобы избежать позднего связывания.
                        for num in range(0, 9)]

        # Параметры окна
        self.window.title("Крестики-Нолики") # Имя окна
        self.window.geometry('640x480') # Размер окна в пикселях

        # Размещение холста с клетками
        self.black_grid.place(x=200, y=100)

        # Размещение клеток
        i = 0 # Счетчик для отступа по оси X
        j = 0 # Счетчик для отступа по оси Y
        for button in self.buttons:
            x = 42 + 75 * (i % 3) # Вычисление положения клетки по оси X относительно начала
            y = 42 + 75 * j # Вычисление положения клетки по оси Y относительно начала
            self.black_grid.create_window(x, y, window=button) # Расположение клетки на окне
            i += 1
            if i % 3 == 0:
                j += 1

        # Настройка типов столбцов в таблице ходов
        self.game_logs['name'] = self.game_logs['name'].astype(str)

    # Метод для вывода окна на экран
    def show(self) -> None:
        self.window.mainloop() # Вывод окна

    # Функция для обработки нажатия на клетки игрового поля
    # num - номер клетки
    def button_click(self, num : int) -> None:
        self.game_logging('player', num, self.player_fig) # Заносим ход пользователя в таблицу ходов
        self.change_button_img(num, self.player_fig) # Изменяем значение выбранной клетки
        self.current_move += 1 # Переходим к следующему ходу

    # Функция для изменения состояния клетки игрового поля
    # num - номер клетки
    # fig_num - номер фигуры
    def change_button_img(self, num : int, fig_num : int) -> None:
        if fig_num == 1: # Проверяем номер фигуры
            self.buttons[num].configure(image=self.red_cross_img) # Изменяем картинку выбраной кнопки на нужную фигуру
        if fig_num == 2:
            self.buttons[num].configure(image=self.blue_circle_img)
        self.game_cells[num] = fig_num # Вносим изменения в состояние поля

    # Функция для приведения игрового поля в начальное состояние
    def reset_game(self):
        self.game_cells = np.zeros(9) # Очищаем игровое поле
        self.game_logs.drop(self.game_logs.index, axis='rows', inplace=True) # Очищаем таблицу ходов
        self.current_move = 0 # Обнуляем счетчик ходов

        for i in range(9): # Очщаем картинки клеток
            self.buttons[i].configure(image=self.start_img)

    # Функция для записи хода
    # name - имя того кто сделал ход ('player', 'bot')
    # num - номер клетки
    # fig_num - номер фигуры
    def game_logging(self, name : str, num : int, fig_num : int):
        self.game_logs.loc[self.current_move, 'name'] = name
        self.game_logs.loc[self.current_move, 'figure'] = fig_num
        self.game_logs.loc[self.current_move, 'move'] = num
        self.game_logs.loc[self.current_move, [f'c_{i}' for i in range(9)]] = self.game_cells