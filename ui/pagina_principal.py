from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from ui.login_panel import LoginPanel
from ui.feed_panel import FeedPanel
from ui.register_panel import RegisterPanel
import data.store as store


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("threads simulacion")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()

        self.login    = LoginPanel()
        self.feed     = FeedPanel()
        self.register = RegisterPanel()

        self.stack.addWidget(self.login)
        self.stack.addWidget(self.register)
        self.stack.addWidget(self.feed)

        self.setCentralWidget(self.stack)

        # Conexiones
        self.login.login_intento.connect(self.procesar_login)
        self.login.go_register.connect(self.ir_registro)
        self.register.registro_intento.connect(self.procesar_registro)
        self.register.go_login.connect(self.volver_login)
        self.feed.on_logout_cb = self.volver_login

    def procesar_login(self, user, password):
        if store.validar_login(user, password):
            self.entrar_feed(user)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def procesar_registro(self, user, password):#si se registra entra al feed
        if store.registrar_usuario(user, password):
            self.entrar_feed(user)   
        else:
            QMessageBox.warning(self, "Error", "El usuario ya existe o es inválido.")

    def entrar_feed(self, username):
        self.feed.usuario_actual = username
        self.feed.cargar_posts()
        self.stack.setCurrentWidget(self.feed)

    def ir_registro(self):
        self.stack.setCurrentWidget(self.register)

    def volver_login(self):
        self.stack.setCurrentWidget(self.login)