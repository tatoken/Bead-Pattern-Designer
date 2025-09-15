import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import main_window

def main():
    app = QApplication(sys.argv)
    w = main_window()
    w.resize(1200, 800)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
