from intro_gui import IntroWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IntroWindow()
    window.show()
    sys.exit(app.exec())
