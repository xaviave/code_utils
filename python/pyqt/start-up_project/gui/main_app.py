
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLineEdit
)

from .documentation import HelpWindow


"""Pyinstaller: 
pyinstaller --name "Collimator control" --clean --windowed --icon="app.ico" 
    --add-data 'style/styles.css;./style' 
    --add-data 'doc/documenation.html;./doc' 
    --add-data 'app.ico;.' main.py
"""


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.init_top_side_gui()
        self.init_bottom_side_gui()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.top_widget)
        main_layout.addWidget(self.bottom_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)

        # Apply a style to the application
        self.setGeometry(300, 300, 1000, 700)

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            with open("_internal/style/styles.css", "r") as f:
                css = f.read()
        else:
            with open("style/styles.css", "r") as f:
                css = f.read()

        self.setStyleSheet(css)

    def init_top_side_gui(self):

        self.checkbox = QCheckBox()

        self.combobox = QComboBox()
        self.combobox.addItem("Choice One")
        self.combobox.addItem("Choice Two")

        self.spinbox = QSpinBox()
        self.spinbox.setRange(0, 100)

        self.lineedit = QLineEdit()


        layout = QWidget()
        layout.setLayout(QGridLayout())
        layout.layout().setContentsMargins(0, 0, 0, 0)
        layout.layout().addWidget(QLabel("Checkbox: "), 0, 0)
        layout.layout().addWidget(self.checkbox, 0, 1)

        layout.layout().addWidget(QLabel("ComboBox: "), 1, 0)
        layout.layout().addWidget(self.combobox, 1, 1)
    
        layout.layout().addWidget(QLabel("Spinbox (0 - 100): "), 2, 0)
        layout.layout().addWidget(self.spinbox, 2, 1)

        layout.layout().addWidget(QLabel("LineEdit: "), 3, 0)
        layout.layout().addWidget(self.lineedit, 3, 1)

        # Bottom layout
        self.top_widget = QWidget()
        self.top_widget.setLayout(QHBoxLayout())
        self.top_widget.layout().setSpacing(10)
        self.top_widget.layout().addWidget(layout)

    def init_bottom_side_gui(self):
        self.start_btn = QPushButton("Start", self)
        self.start_btn.clicked.connect(self.on_click_start)

        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.clicked.connect(self.on_clock_stop)

        self.documentation_button = QPushButton("Documentation", self)
        self.documentation_button.clicked.connect(self.on_click_documentation)

        btn_widget = QWidget()
        btn_widget.setLayout(QHBoxLayout())
        btn_widget.layout().addWidget(self.start_btn)
        btn_widget.layout().addWidget(self.stop_btn)
        btn_widget.layout().addWidget(self.documentation_button)

        self.readed_data_text = QTextEdit(self)
        self.readed_data_text.setReadOnly(True)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(QVBoxLayout())
        self.bottom_widget.layout().addWidget(self.readed_data_text)
        self.bottom_widget.layout().addWidget(btn_widget)

    def on_click_start(self):
        print("Clicked on Start btn")

    def on_clock_stop(self):
        print("Clicked on Stop btn")

    def on_click_documentation(self):
        self.help_window = HelpWindow()
        self.help_window.show()