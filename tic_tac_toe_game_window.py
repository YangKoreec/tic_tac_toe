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
        self.player_block = False # Блокировщик хода игрока, для того чтобы бот успел сходить

        # Фигуры, которыми играют пользователь и бот
        self.player_fig = 1 # То чем играет пользователь (Пользователь всегда начинает с крестиков)
        self.bot_fig = 2 # То чем играет бот (Бот всегда начинает с ноликов)

        # Переменные с информацией о статистике пользователя и бота за сеанс
        self.player_score = 0 # Счёт пользователя
        self.bot_score = 0 # Счёт бота

        # Надписи с информацией об игре
        self.player_fig_label = Label(self.window, text='YOU:') # Надпись для вывода информации о фигуре, которой играет пользователь
        self.bot_fig_lable = Label(self.window, text='BOT:') # Надпись для вывода информации о фигуре, которой играет бот
        self.player_score_label = Label(self.window, text='Your score: 0', font=('Arial', 15, 'bold')) # Надпись для вывода инофрмации о счёте пользователя
        self.bot_score_label = Label(self.window, text='Bot score: 0', font=('Arial', 15, 'bold')) # Надпись для вывода инофрмации о счёте бота

        # Холсты для вывода картинок фигур пользователя и бота
        self.player_fig_view = Canvas(self.window, bg='black', width=72, height=72)
        self.bot_fig_view = Canvas(self.window, bg='black', width=72, height=72)

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
                               command=lambda i=num: self.player_move(i)) # Передача функции при нажатии, используется лямбда-функция, так как необходимо передать
                                                                           # в функцию номер кнопки. i=num используется, чтобы избежать позднего связывания.
                        for num in range(0, 9)]

        # Параметры окна
        self.window.title("Крестики-Нолики") # Имя окна
        self.window.geometry('640x480') # Размер окна в пикселях

        # Вывод информации о фигуре пользователя
        self.player_fig_view.create_image(38, 38, image=self.red_cross_img) # Задаём изображение фигуры пользователя
        self.player_fig_label.place(x=10, y=35)
        self.player_fig_view.place(x=45, y=10)

        # Вывод информации о фигуре бота
        self.bot_fig_view.create_image(38, 38, image=self.blue_circle_img) # Задаём изображение фигуры бота
        self.bot_fig_lable.place(x=10, y=115)
        self.bot_fig_view.place(x=45, y=90)

        # Вывод информации о счётах пользователь и пользователя
        self.player_score_label.place(x=10, y=200)
        self.bot_score_label.place(x=10, y=230)

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
    def player_move(self, num : int) -> None:
        if not self.player_block:
            if self.make_move('player', num): # Совершаем пользовательский ход и проверяем его возможность
                self.player_block = True # Блокируем ход игрока, чтобы сходил бот

    # Функция для обработки хода бота
    # num - номер клетки
    def bot_move(self, num : int) -> None:
        if self.make_move('bot', num): # Совершаем ход бота и проверяем его возможность
            self.player_block = False # Разблокируем ход игрока

    # Функция для обработки хода пользователя или бота
    def make_move(self, name : str, num : int) -> bool:
        if self.game_cells[num] == 0: # Проверяем, что клетка не занята фигурой
            self.game_logging(name, num, self.player_fig if name == 'player' else self.bot_fig) # Заносим ход в таблицу ходов
            self.change_cell_val(num, self.player_fig if name == 'player' else self.bot_fig) # Изменяем значение выбранной клетки
            self.current_move += 1 # Увеличиваем счетчик ходов на 1
            return True
        else:
            return False

    # Функция для изменения состояния клетки игрового поля
    # num - номер клетки
    # fig_num - номер фигуры
    def change_cell_val(self, num : int, fig_num : int) -> None:
        if fig_num == 1: # Проверяем номер фигуры
            self.buttons[num].configure(image=self.red_cross_img) # Изменяем картинку выбранной кнопки на нужную фигуру
        elif fig_num == 2:
            self.buttons[num].configure(image=self.blue_circle_img)
        self.game_cells[num] = fig_num # Вносим изменения в состояние поля

    # Функция для приведения игрового поля в начальное состояние (используется при смене хода)
    def reset_game(self):
        self.game_cells = np.zeros(9) # Очищаем игровое поле
        self.game_logs.drop(self.game_logs.index, axis='rows', inplace=True) # Очищаем таблицу ходов
        self.current_move = 0 # Обнуляем счетчик ходов
        self.change_figures() # Меняем фигуры пользователя и игрока

        # Задаём последовательность ходов в зависимости от фигуры пользователя
        if self.player_fig == 1:
            self.player_block = False
        elif self.player_fig == 2:
            self.player_block = True

        for i in range(9): # Возвращаем картинки клеток в исходное состояние
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

    # Функция для изменения счёта пользователя или бота
    # name - имя победителя ('player', 'bot')
    def change_score(self, name : str) -> None:
        if name == 'player': # Проверяем кто победил
            self.player_score += 1 # Увеличивает счёт на 1
            self.player_score_label.configure(text=f'Your score: {self.player_score}') # Выводим новый счёт
        elif name == 'bot':
            self.bot_score += 1
            self.bot_score_label.configure(text=f'Bot score: {self.bot_score}')

    # Функция для изменения фигур пользователя и бота
    def change_figures(self):
        self.player_fig, self.bot_fig = self.bot_fig, self.player_fig

        if self.player_fig == 1:
            self.player_fig_view.create_image(38, 38, image=self.red_cross_img)
            self.bot_fig_view.create_image(38, 38, image=self.blue_circle_img)
        elif self.player_fig == 2:
            self.player_fig_view.create_image(38, 38, image=self.blue_circle_img)
            self.bot_fig_view.create_image(38, 38, image=self.red_cross_img)

    # Функция возвращает текущее состояние игрового поля
    def get_play_cells(self):
        return self.game_cells

    # Функция возвращает таблицу с последовательностью ходов
    def get_game_logs(self):
        return self.game_logs