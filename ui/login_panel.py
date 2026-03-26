from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

BG       = "#1e1f2e"
SURFACE  = "#2b2d42"
PRIMARY  = "#7c5cbf"
TEXT     = "#e0e0f0"
SUBTEXT  = "#9b9bb4"
BORDER   = "#3d3f5c"


class LoginPanel(QWidget):
    login_intento = pyqtSignal(str, str)
    go_register   = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {BG};")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedWidth(360)
        card.setStyleSheet(f"""
            background: {SURFACE};
            border-radius: 16px;
            padding: 30px;
            border: 1px solid {BORDER};
        """)

        box = QVBoxLayout(card)
        box.setSpacing(14)

        logo = QLabel("threads")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {TEXT};")

        sub = QLabel("Inicia sesión para continuar")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color: {SUBTEXT}; font-size: 13px;")

        estilo_input = f"""
            QLineEdit {{
                background: {BG};
                color: {TEXT};
                padding: 10px;
                border-radius: 8px;
                border: 1px solid {BORDER};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid {PRIMARY};
            }}
        """

        self.user = QLineEdit()
        self.user.setPlaceholderText("Usuario")
        self.user.setStyleSheet(estilo_input)

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Contraseña")
        self.passw.setEchoMode(QLineEdit.EchoMode.Password)
        self.passw.setStyleSheet(estilo_input)

        btn_login = QPushButton("Iniciar sesión")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY};
                color: white;
                padding: 11px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: #9370db; }}
        """)
        btn_login.clicked.connect(self.enviar_login)

        btn_reg = QPushButton("Regístrate")
        btn_reg.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reg.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {PRIMARY};
                font-size: 13px;
                border: none;
            }}
            QPushButton:hover {{ color: #9370db; }}
        """)
        btn_reg.clicked.connect(self.go_register.emit)

        box.addWidget(logo)
        box.addWidget(sub)
        box.addSpacing(6)
        box.addWidget(self.user)
        box.addWidget(self.passw)
        box.addWidget(btn_login)
        box.addWidget(btn_reg)

        layout.addWidget(card)

    def enviar_login(self):
        self.login_intento.emit(self.user.text(), self.passw.text())