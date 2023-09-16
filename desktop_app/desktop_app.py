import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt


class GifViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MeowGIF")

        # Создаем метку для отображения гиф-изображений
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)  # Центрируем изображение

        # Создаем кнопки для листания гиф-изображений
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_gif)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_gif)

        # Создаем главное окно
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.gif_label)
        layout.addWidget(self.previous_button)
        layout.addWidget(self.next_button)
        self.setCentralWidget(central_widget)

        # Загружаем гиф-изображения
        # self.gif_directory = ".\cats"
        self.gif_files = [
            'https://media.tenor.com/n3V1_zxtOZMAAAAC/dancing-cat.gif',
            'https://media.tenor.com/qrnbc9aH-bAAAAAC/saturday-garfield.gif',
            'https://media.tenor.com/L6ijEr9m4f4AAAAd/razyness-razy.gif'
        ]
        # Тут меняем часть на получение гиф-изображений по апи и с фильтром на тег коты

        self.current_gif_index = 0

        # Открываем первое гиф-изображение
        self.open_gif(self.current_gif_index)

    def open_gif(self, index):
        gif_file = self.gif_files[index]
        response = requests.get(gif_file)

        if response.status_code == 200:
            with open("temp.gif", "wb") as f:
                f.write(response.content)

            self.movie = QMovie("temp.gif")
            self.movie.setCacheMode(QMovie.CacheAll)

        # Очищаем метку и устанавливаем виджет QMovie
            self.gif_label.clear()
            self.gif_label.setMovie(self.movie)

        # Запускаем воспроизведение гиф-изображения
            self.movie.start()

    def previous_gif(self):
        self.current_gif_index -= 1
        if self.current_gif_index < 0:
            self.current_gif_index = len(self.gif_files) - 1
        self.open_gif(self.current_gif_index)

    def next_gif(self):
        self.current_gif_index += 1
        if self.current_gif_index >= len(self.gif_files):
            self.current_gif_index = 0
        self.open_gif(self.current_gif_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifViewer()
    window.show()
    sys.exit(app.exec_())