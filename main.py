import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import datetime


class TigerDetectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Создаем макет
        layout = QVBoxLayout()

        # Заголовок
        self.title_label = QLabel("ДЕТЕКТ АМУРСКИХ ТИГРОВ")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; background-color: #ddd; padding: 5px;")
        layout.addWidget(self.title_label)

        # Метка для изображения
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        self.showImage("images/image.jpg")

        # Кнопка выбора видео
        self.video_button = QPushButton("Выбрать видео")
        self.video_button.clicked.connect(self.loadVideo)
        layout.addWidget(self.video_button)

        # Кнопка запуска детекции
        self.detect_button = QPushButton("Запустить детект")
        self.detect_button.clicked.connect(self.startDetection)
        layout.addWidget(self.detect_button)

        # Метка статуса
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Устанавливаем макет
        self.setLayout(layout)

        # Устанавливаем свойства окна
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Tiger Detector')

        # Темная тема
        self.setStyleSheet("background-color: #333; color: #fff;")

    def loadVideo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите видео", "", "Video Files (*.mp4 *.avi *.mkv);;All Files (*)", options=options)

        if file_name:
            self.video_path = file_name
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите видео.")

    def startDetection(self):
        if hasattr(self, 'video_path'):
            self.detect_button.setEnabled(False)
            self.video_button.setEnabled(False)
            self.runDetection()
            self.detect_button.setEnabled(True)
            self.video_button.setEnabled(True)

    def runDetection(self):
        # Импортируем и запускаем код из videos.py
        from videos import detect_objects

        # Обновляем статус
        self.status_label.setText("Детект запустился, пожалуйста, ожидайте.")

        # Запускаем детекцию с выбранным видео
        detect_objects(self.video_path)

        # Обновляем статус
        output_path = os.path.join('detected', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        self.status_label.setText(f"Детект закончен, сохранено в {output_path}")

    def showImage(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(300)  # Регулируем ширину по необходимости
        self.image_label.setPixmap(pixmap)
        self.image_label.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TigerDetectorApp()
    window.show()
    sys.exit(app.exec_())
