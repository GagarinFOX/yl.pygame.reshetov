import pygame
from pygame import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic  # Импортируем uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia
import sqlite3

size = height, width = 1280, 720

background_color = "black"


class Mainmenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu1.ui', self)
        self.start_btn.clicked.connect(self.start_game)
        self.exit_btn.clicked.connect(self.exit_game)
        self.music_btn.clicked.connect(self.music_off)
        self.sounds_btn.clicked.connect(self.sounds_off)
        self.music_pos1.clicked.connect(self.set_music1)
        self.music_pos2.clicked.connect(self.set_music2)
        self.music_pos3.clicked.connect(self.set_music3)
        self.music_pos4.clicked.connect(self.set_music4)

    def start_game(self):
        self.close()
        main()

    def exit_game(self):
        self.close()

    def music_off(self):
        pass  # без музыки

    def sounds_off(self):
        pass  # без звуков

    def set_music1(self):
        print('1')

    def set_music2(self):
        print('2')

    def set_music3(self):
        print('3')

    def set_music4(self):
        print('4')


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(size)  # Создаем окошко
    pygame.display.set_caption("23:59")  # Пишем в шапку
    bg = Surface(size)  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(background_color))  # Заливаем поверхность сплошным цветом
    running = True
    fps = 60
    while running:  # Основной цикл программы
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    board.get_click(event.pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    time_on = not time_on
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    speed += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    speed -= 1
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mainmenu()
    ex.show()
    sys.exit(app.exec_())
