import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Documentation")
        self.resize(500, 750)
        self.text_edit = QTextEdit(readOnly=True, acceptRichText=True, objectName="help_text_edit")
        self.text_edit.setStyleSheet("color: black; background-color: #f0f0f0;")

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.text_edit, Qt.AlignLeft)

        self.init_ui()

    def init_ui(self):
        """Initializes the user interface of the help window."""
        try:
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                with open("_internal/doc/documentation.html") as f:
                    contents = f.read()
            else:
                with open("doc/documentation.html") as f:
                    contents = f.read()

            self.text_edit.setHtml(contents)

        except FileNotFoundError:
            print("No file found for documentation.html")

        # Set the text cursor position to the beginning of the document
        cursor = self.text_edit.textCursor()
        cursor.setPosition(0)

        # Scroll the view to the top of the document
        self.text_edit.setTextCursor(cursor)
        self.text_edit.verticalScrollBar().setValue(0)
