import bcrypt
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)


class LoginForm(QDialog):
    """Pop-up window for the Admin mode.

    The User need to enter the Good Username with password to enter in admin mode

    $2b$12$AKM6JaeHMcCARJjb8KHitu5JM.zixJeRF9pe0D5yeGMpSgCPMaOPq is the Hash for password

    Args:
        QDialog (QWidget): Popup window

    """

    def __init__(
        self,
        parent,
        hashed_password="$2b$12$AKM6JaeHMcCARJjb8KHitu5JM.zixJeRF9pe0D5yeGMpSgCPMaOPq",
        with_user=False,
        username=None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Admin mode")
        self.setFixedWidth(300)
        self.setFixedHeight(180)

        self.with_user = with_user
        self.hashed_password = hashed_password
        self.username = username

        if self.with_user:
            self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton("Login", self)
        self.buttonLogin.clicked.connect(self.handle_login)

        layout = QWidget(self)
        grid_layout = QGridLayout()
        layout.setLayout(grid_layout)

        if self.with_user:
            grid_layout.addWidget(QLabel("Username"), 0, 0)  # First row
            grid_layout.addWidget(self.textName, 0, 1)  # First row

        # Always add password label and input fields (now on second row)
        grid_layout.addWidget(QLabel("Password"), 1, 0)
        grid_layout.addWidget(self.textPass, 1, 1)

        grid_layout.addWidget(self.buttonLogin, 2, 0, 1, 2)  # Span 2 columns

    def handle_login(self):
        """Check if the User and password match."""
        is_valid_login = False

        if self.with_user:
            is_valid_login = (
                self.textName.text() == self.username
                and self.check_password(self.textPass.text(), self.hashed_password)
            )
        else:
            is_valid_login = self.check_password(
                self.textPass.text(), self.hashed_password
            )

        if is_valid_login:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Bad user or password")

    def check_password(self, plain_text_password, hashed_password):
        """Check hashed password.

        Using bcrypt, the salt is saved into the hash itself

        Args:
            plain_text_password (str): password to test.
            hashed_password (str): hashed password to compaire.

        Returns:
            bool: return if the password match with the hashed password in the DB
        """
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())


def get_hashed_password(plain_text_password: str):
    """Hash a password for the first time.

    Using bcrypt, the salt is saved into the hash itself.

    Args:
        plain_text_password (str): New Password to Hash and add to the database

    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


if __name__ == "__main__":
    password = input("Enter the password you want to hash: ")
    print(get_hashed_password(password))
