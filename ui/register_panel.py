from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

BG      = "#1e1f2e"
SURFACE = "#2b2d42"
PRIMARY = "#7c5cbf"
TEXT    = "#e0e0f0"
SUBTEXT = "#9b9bb4"
BORDER  = "#3d3f5c"


class RegisterPanel(QWidget):
    registro_intento = pyqtSignal(str, str)
    go_login         = pyqtSignal()

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

        logo = QLabel("Crear cuenta")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {TEXT};")

        sub = QLabel("Únete a Threads")
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
        self.user.setPlaceholderText("Elige un usuario")
        self.user.setStyleSheet(estilo_input)

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Contraseña (mín. 4 caracteres)")
        self.passw.setEchoMode(QLineEdit.EchoMode.Password)
        self.passw.setStyleSheet(estilo_input)

        self.passw2 = QLineEdit()
        self.passw2.setPlaceholderText("Confirmar contraseña")
        self.passw2.setEchoMode(QLineEdit.EchoMode.Password)
        self.passw2.setStyleSheet(estilo_input)

        self.error_lbl = QLabel("")
        self.error_lbl.setStyleSheet(f"color: #f04747; font-size: 12px;")
        self.error_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_reg = QPushButton("Registrarse")
        btn_reg.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reg.setStyleSheet(f"""
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
        btn_reg.clicked.connect(self.enviar_registro)

        btn_back = QPushButton("Inicia sesión")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {PRIMARY};
                font-size: 13px;
                border: none;
            }}
            QPushButton:hover {{ color: #9370db; }}
        """)
        btn_back.clicked.connect(self.go_login.emit)

        box.addWidget(logo)
        box.addWidget(sub)
        box.addSpacing(6)
        box.addWidget(self.user)
        box.addWidget(self.passw)
        box.addWidget(self.passw2)
        box.addWidget(self.error_lbl)
        box.addWidget(btn_reg)
        box.addWidget(btn_back)

        layout.addWidget(card)

    def enviar_registro(self):
        if self.passw.text() != self.passw2.text():
            self.error_lbl.setText("Las contraseñas no coinciden.")
            return
        if len(self.passw.text()) < 4:
            self.error_lbl.setText("La contraseña es muy corta.")
            return
        self.error_lbl.setText("")
        self.registro_intento.emit(self.user.text(), self.passw.text())