import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt

class PiTV(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PiTV')
        self.setGeometry(100, 100, 800, 450)

        # Set up the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Set background image
        self.set_background_image('wallpaper.png')

        # Set up "Welcome to PiTV!" text
        self.setup_welcome_text()

        # Set up buttons
        self.setup_buttons()

    def set_background_image(self, image_path):
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap(image_path))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()  # Send the label to the back

    def setup_welcome_text(self):
        self.welcome_label = QLabel("Welcome to PiTV!", self)
        self.welcome_label.setFont(QFont('Arial', 24))
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def setup_buttons(self):
        button_layout = QHBoxLayout()

        button_data = [
            ('YouTube', 'youtube.png'),
            ('ExpressVPN', 'vpn.png'),
            ('Firefox', 'firefox.png'),
            ('Netflix', 'netflix.png')
        ]

        for name, icon in button_data:
            button = QPushButton(name, self)
            button.setIcon(QIcon(icon))
            button.setIconSize(QPixmap(icon).rect().size())
            button.setFixedSize(100, 100)
            button.clicked.connect(lambda _, n=name: self.button_clicked(n))
            button_layout.addWidget(button)

        self.layout.addLayout(button_layout)
        power_button = QPushButton(self)
        power_button.setIcon(QIcon('power.png'))
        power_button.setIconSize(QPixmap('power.png').rect().size())
        power_button.setFixedSize(40, 40)
        power_button.clicked.connect(lambda: self.button_clicked('Power'))
        screen_button = QPushButton(self)
        screen_button.setIcon(QIcon('screen.png'))
        screen_button.setIconSize(QPixmap('screen.png').rect().size())
        screen_button.setFixedSize(40, 40)
        screen_button.clicked.connect(lambda: self.button_clicked('Screen'))
        power_button.move(10, 10)
        screen_button.move(60, 10)

    def button_clicked(self, name):
        print(f'{name} button clicked')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PiTV()
    main_window.show()
    sys.exit(app.exec())
