from PyQt5.QtWidgets import QApplication

from gui.main_app import MainApp

if __name__ == "__main__":
    app = QApplication([])

    app.setApplicationName("Name of your app")

    my_gui = MainApp()
    my_gui.show()
    app.exec_()
