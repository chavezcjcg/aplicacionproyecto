from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QScrollArea, QFrame, QStackedWidget,
    QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
import data.store as store

BG      = "#1e1f2e"
SURFACE = "#2b2d42"
CARD    = "#32344a"
PRIMARY = "#7c5cbf"
TEXT    = "#e0e0f0"
SUBTEXT = "#9b9bb4"
BORDER  = "#3d3f5c"


class PostCard(QFrame):
    def __init__(self, post):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background: {CARD};
                border-radius: 12px;
                border: 1px solid {BORDER};
                padding: 14px;
                margin: 4px 2px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        autor = QLabel(f"@{post['autor']}")
        autor.setStyleSheet(f"color: {PRIMARY}; font-weight: bold; font-size: 14px;")

        texto = QLabel(post["texto"])
        texto.setWordWrap(True)
        texto.setStyleSheet(f"color: {TEXT}; font-size: 13px;")

        layout.addWidget(autor)
        layout.addWidget(texto)


class FeedPage(QWidget):
    def __init__(self, usuario_actual, on_perfil):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.scroll_infinito_activo = False
        self.setStyleSheet(f"background: {BG};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Barra superior
        topbar = QWidget()
        topbar.setStyleSheet(f"background: {SURFACE}; border-bottom: 1px solid {BORDER};")
        topbar.setFixedHeight(54)
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(16, 0, 16, 0)

        titulo = QLabel("Threads")
        titulo.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {TEXT};")

        # Botón toggle para scroll infinito
        self.btn_infinito = QPushButton("∞")
        self.btn_infinito.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_infinito.setFixedSize(40, 40)
        self.actualizar_estilo_boton_infinito()
        self.btn_infinito.clicked.connect(self.toggle_scroll_infinito)

        btn_perfil = QPushButton(f"@{usuario_actual}")
        btn_perfil.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_perfil.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY};
                color: white;
                padding: 6px 14px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{ background: #9370db; }}
        """)
        btn_perfil.clicked.connect(on_perfil)
        # barra de busqueda
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar palabra...")
        self.input_busqueda.setFixedWidth(200)
        self.input_busqueda.setStyleSheet(f"""
            QLineEdit {{
                background: {BG};
                color: {TEXT};
                border: 1px solid {BORDER};
                border-radius: 15px;
                padding: 4px 10px;
            }}
        """)
  
        self.input_busqueda.textChanged.connect(self.ejecutar_busqueda) 
        # --------------------------------

        top_layout.addWidget(titulo)
        top_layout.addStretch()
        top_layout.addWidget(self.input_busqueda) 
        top_layout.addWidget(self.btn_infinito)
        top_layout.addStretch()
        top_layout.addWidget(btn_perfil)
        layout.addWidget(topbar)

        # Cuerpo
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 16, 20, 16)
        body_layout.setSpacing(12)

        # Caja nueva publicación
        caja = QWidget()
        caja.setStyleSheet(f"""
            background: {SURFACE};
            border-radius: 12px;
            border: 1px solid {BORDER};
            padding: 12px;
        """)
        caja_layout = QVBoxLayout(caja)

        self.input_post = QTextEdit()
        self.input_post.setPlaceholderText("¿Qué estás pensando?")
        self.input_post.setMaximumHeight(80)
        self.input_post.setStyleSheet(f"""
            QTextEdit {{
                background: {BG};
                color: {TEXT};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }}
        """)

        fila_btn = QHBoxLayout()
        fila_btn.addStretch()
        btn_pub = QPushButton("Publicar")
        btn_pub.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_pub.setFixedWidth(100)
        btn_pub.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY};
                color: white;
                padding: 7px;
                border-radius: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: #9370db; }}
        """)
        btn_pub.clicked.connect(self.publicar)
        fila_btn.addWidget(btn_pub)

        caja_layout.addWidget(self.input_post)
        caja_layout.addLayout(fila_btn)
        body_layout.addWidget(caja)

        # Scroll de posts
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        self.scroll.verticalScrollBar().valueChanged.connect(self.detectar_fin_scroll)

        self.contenedor = QWidget()
        self.contenedor.setStyleSheet(f"background: {BG};")
        self.posts_layout = QVBoxLayout(self.contenedor)
        self.posts_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.contenedor)
        body_layout.addWidget(self.scroll)

        layout.addWidget(body)
        self.cargar_posts()

    def publicar(self):
        texto = self.input_post.toPlainText().strip()
        if store.crear_post(self.usuario_actual, texto):
            self.input_post.clear()
            self.cargar_posts()

    def cargar_posts(self):
        for i in reversed(range(self.posts_layout.count())):
            w = self.posts_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        posts = store.obtener_posts()
        if not posts:
            vacio = QLabel("Aún no hay publicaciones")
            vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vacio.setStyleSheet(f"color: {SUBTEXT}; font-size: 14px; padding: 30px;")
            self.posts_layout.addWidget(vacio)
        else:
            for p in posts:
                self.posts_layout.addWidget(PostCard(p))

    def ejecutar_busqueda(self, texto):
        # Limpiamos los posts actuales de la pantalla
        for i in reversed(range(self.posts_layout.count())):
            w = self.posts_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        # Si la barra está vacía, cargamos todos los posts normales
        if texto.strip() == "":
            posts = store.obtener_posts()
        else:
            posts = store.buscar_post_ui(texto)

        if not posts:
            vacio = QLabel(f"No se encontró nada con: '{texto}'")
            vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vacio.setStyleSheet(f"color: {SUBTEXT}; font-size: 14px; padding: 30px;")
            self.posts_layout.addWidget(vacio)
        else:
            for p in posts:
                self.posts_layout.addWidget(PostCard(p))

    def toggle_scroll_infinito(self):
        self.scroll_infinito_activo = not self.scroll_infinito_activo
        self.actualizar_estilo_boton_infinito()
        if self.scroll_infinito_activo:
            # Reinicia el scroll al principio cuando se activa
            self.scroll.verticalScrollBar().setValue(0)

    def actualizar_estilo_boton_infinito(self):
        if self.scroll_infinito_activo:
            self.btn_infinito.setStyleSheet(f"""
                QPushButton {{
                    background: {PRIMARY};
                    color: white;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 16px;
                    border: 2px solid {PRIMARY};
                }}
                QPushButton:hover {{ background: #9370db; }}
            """)
        else:
            self.btn_infinito.setStyleSheet(f"""
                QPushButton {{
                    background: {SURFACE};
                    color: {SUBTEXT};
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 16px;
                    border: 2px solid {BORDER};
                }}
                QPushButton:hover {{ background: {CARD}; }}
            """)

    def detectar_fin_scroll(self, valor):
        if not self.scroll_infinito_activo:
            return
        
        scrollbar = self.scroll.verticalScrollBar()
        if valor == scrollbar.maximum():
            scrollbar.setValue(0)


class PerfilPage(QWidget):
    def __init__(self, usuario_actual, on_volver, on_logout):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.setStyleSheet(f"background: {BG};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Barra superior
        topbar = QWidget()
        topbar.setStyleSheet(f"background: {SURFACE}; border-bottom: 1px solid {BORDER};")
        topbar.setFixedHeight(54)
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(16, 0, 16, 0)

        btn_volver = QPushButton("Volver")
        btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_volver.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {PRIMARY};
                font-size: 14px;
                border: none;
            }}
            QPushButton:hover {{ color: #9370db; }}
        """)
        btn_volver.clicked.connect(on_volver)

        titulo = QLabel("Perfil")
        titulo.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {TEXT};")

        btn_logout = QPushButton("Cerrar sesión")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setStyleSheet(f"""
            QPushButton {{
                background: #f04747;
                color: white;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{ background: #d63031; }}
        """)
        btn_logout.clicked.connect(on_logout)

        top_layout.addWidget(btn_volver)
        top_layout.addStretch()
        top_layout.addWidget(titulo)
        top_layout.addStretch()
        top_layout.addWidget(btn_logout)
        layout.addWidget(topbar)

        # Contenido
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(30, 30, 30, 30)
        body_layout.setSpacing(16)
        body_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        avatar = QLabel(":)")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"""
            font-size: 60px;
            background: {SURFACE};
            border-radius: 50px;
            padding: 10px;
            border: 2px solid {PRIMARY};
        """)
        avatar.setFixedSize(100, 100)

        avatar_wrap = QHBoxLayout()
        avatar_wrap.addStretch()
        avatar_wrap.addWidget(avatar)
        avatar_wrap.addStretch()

        nombre = QLabel(f"@{usuario_actual}")
        nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nombre.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {TEXT};")

        perfil = store.obtener_perfil(usuario_actual)

        fecha = QLabel(f"📅 Se unió en {perfil.get('unirse', '')}")
        fecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fecha.setStyleSheet(f"color: {SUBTEXT}; font-size: 13px;")

        num_posts = store.contar_posts(usuario_actual)
        stats = QLabel(f" {num_posts} publicaciones")
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats.setStyleSheet(f"color: {SUBTEXT}; font-size: 13px;")

        bio_label = QLabel("Bio:")
        bio_label.setStyleSheet(f"color: {SUBTEXT}; font-size: 13px;")

        self.bio_input = QTextEdit()
        self.bio_input.setPlainText(perfil.get("bio", ""))
        self.bio_input.setMaximumHeight(80)
        self.bio_input.setStyleSheet(f"""
            QTextEdit {{
                background: {SURFACE};
                color: {TEXT};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }}
        """)

        btn_bio = QPushButton("Guardar bio")
        btn_bio.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_bio.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY};
                color: white;
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: #9370db; }}
        """)
        btn_bio.clicked.connect(self.guardar_bio)

        body_layout.addLayout(avatar_wrap)
        body_layout.addWidget(nombre)
        body_layout.addWidget(fecha)
        body_layout.addWidget(stats)
        body_layout.addSpacing(10)
        body_layout.addWidget(bio_label)
        body_layout.addWidget(self.bio_input)
        body_layout.addWidget(btn_bio)

        layout.addWidget(body)

    def guardar_bio(self):
        store.actualizar_bio(self.usuario_actual, self.bio_input.toPlainText())


class FeedPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.usuario_actual = ""
        self.on_logout_cb = None
        self.setStyleSheet(f"background: {BG};")

        self.stack = QStackedWidget()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

    def cargar_posts(self):
        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()

        self.feed_page = FeedPage(self.usuario_actual, on_perfil=self.ir_perfil)
        self.perfil_page = PerfilPage(
            self.usuario_actual,
            on_volver=self.ir_feed,
            on_logout=self._logout
        )

        self.stack.addWidget(self.feed_page)
        self.stack.addWidget(self.perfil_page)
        self.stack.setCurrentWidget(self.feed_page)

    def ir_perfil(self):
        self.stack.setCurrentWidget(self.perfil_page)

    def ir_feed(self):
        self.stack.setCurrentWidget(self.feed_page)

    def _logout(self):
        if self.on_logout_cb:
            self.on_logout_cb()