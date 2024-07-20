import os
import sys
import pyautogui
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, \
    QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon, QFont, QPainter, QBrush, QColor
from PyQt6.QtCore import Qt, QSize
import time
import platform


class PiTV(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PiTV')
        self.setGeometry(100, 100, 1920, 1080)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.set_background_image('wallpaper.png')

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

        self.setup_welcome_text()

        self.setup_buttons()

    def set_background_image(self, image_path):
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap(image_path))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

    def setup_welcome_text(self):
        self.welcome_label = QLabel("Welcome to PiTV!", self)
        self.welcome_label.setFont(QFont('Arial', 24))
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def setup_buttons(self):
        button_layout = QHBoxLayout()

        button_data = [
            ('YouTube', 'youtube.png', 'open https://youtube.com'),
            ('ExpressVPN', 'vpn.png', 'open -a ExpressVPN.app'),
            ('Firefox', 'firefox.png', 'open -a Firefox.app')
        ]

        for name, icon, command in button_data:
            button = self.create_button(name, icon, command)
            button_layout.addWidget(button)

        self.layout.addLayout(button_layout)

        # Power button
        power_button = QPushButton(self)
        power_button.setIcon(QIcon(self.create_rounded_icon('power.png')))
        power_button.setIconSize(QSize(20, 20))
        power_button.setFixedSize(60, 60)
        power_button.clicked.connect(self.show_power_menu)
        power_button.move(10, 10)

        # Screen button
        screen_button = QPushButton(self)
        screen_button.setIcon(QIcon(self.create_rounded_icon('screen.png')))
        screen_button.setIconSize(QSize(20, 20))
        screen_button.setFixedSize(60, 60)
        screen_button.clicked.connect(lambda: exit(0))
        screen_button.move(80, 10)

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

    def create_button(self, name, icon, command):
        button = QPushButton(self)
        button.setIcon(QIcon(self.create_rounded_icon(icon)))
        button.setIconSize(QSize(70, 70))
        button.setFixedSize(120, 120)
        button.setToolTip(name)
        button.setStyleSheet("QPushButton { text-align: center; }")
        button.clicked.connect(lambda: self.button_clicked(command))

        button_layout = QVBoxLayout(button)
        button_layout.addStretch()
        label = QLabel(name, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(label)

        return button

    def create_rounded_icon(self, image_path):
        pixmap = QPixmap(image_path).scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        brush = QBrush(pixmap)
        painter.setBrush(brush)
        painter.setPen(Qt.GlobalColor.transparent)
        rect = pixmap.rect()
        radius = 20  # Adjust the radius for rounded corners
        painter.drawRoundedRect(rect, radius, radius)
        painter.end()
        return rounded

    def button_clicked(self, command):
        os.system(command)

    def show_power_menu(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Power Options")
        msg_box.setText("Choose an action:")
        msg_box.setIcon(QMessageBox.Icon.Information)
        restart_button = msg_box.addButton("Restart", QMessageBox.ButtonRole.ActionRole)
        shutdown_button = msg_box.addButton("Shutdown", QMessageBox.ButtonRole.ActionRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg_box.exec()

        if msg_box.clickedButton() == restart_button:
            self.restart_system()
        elif msg_box.clickedButton() == shutdown_button:
            self.shutdown_system()

    def restart_system(self):
        if platform.system() == 'Windows':
            os.system("shutdown /r /t 0")
        elif platform.system() == 'Darwin':
            os.system("sudo shutdown -r now")
        elif platform.system() == 'Linux':
            os.system("sudo reboot")

    def shutdown_system(self):
        if platform.system() == 'Windows':
            os.system("shutdown /s /t 0")
        elif platform.system() == 'Darwin':
            os.system("sudo shutdown -h now")
        elif platform.system() == 'Linux':
            os.system("sudo shutdown now")

    def minimise_window(self):
        if platform.system() == 'Windows':
            pyautogui.keyDown('winleft')
            pyautogui.press('left')
            pyautogui.keyUp('winleft')
        elif platform.system() == "Darwin":
            pyautogui.hotkey('command', 'm')
        pyautogui.press('n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PiTV()
    main_window.show()
    sys.exit(app.exec())
