from Estructuras.lista_simple import ListaEnlazada
from Estructuras.lista_circular import PaginadeAplicacion
from Estructuras.lista_doble import ListaDoblementeEnlazada
from Modelos.modelos import Publicacion

class Sistema:
    def __init__(self):
        self.usuarios = ListaEnlazada()
        self.feed = PaginadeAplicacion()
        self.feed_doble = ListaDoblementeEnlazada()
        self.usuario_actual = None

    def registrar_usuario(self, nombre, contrasenia, usuario):
        self.usuarios.registrar_usuario(nombre, contrasenia, usuario)

    def iniciar_sesion(self, usuario, contrasenia):
        actual = self.usuarios.cabeza
        while actual is not None:
            if actual.dato.usuario == usuario and actual.dato.contrasenia == contrasenia:
                self.usuario_actual = actual.dato
                return True
            actual = actual.siguiente
        return False

    def cerrar_sesion(self):
        self.usuario_actual = None

    def publicar(self, contenido):
        if self.usuario_actual is None:
            print("Debe de iniciar sesion")
            return
        pub = Publicacion(self.usuario_actual.usuario, contenido)
        self.feed.insertar(pub)
        self.feed_doble.insertar(pub)

    def dar_like(self, nodo):
        if self.usuario_actual:
            nodo.dato.verificar_like(self.usuario_actual.usuario)

    def comentar_post(self, nodo, texto):
        if self.usuario_actual:
            nodo.dato.agregar_comentario(self.usuario_actual.usuario, texto)

    def favorito(self, nodo):
        if self.usuario_actual:
            nodo.dato.marcar_favorito()

    def estadisticas(self):
        likes = 0
        comentarios = 0
        actual = self.feed.cabeza
        if actual:
            start = actual
            while True:
                likes += actual.dato.lista_likes.tamaño()
                comentarios += actual.dato.lista_comentarios.tamaño()
                actual = actual.siguiente
                if actual == start:
                    break
        return likes, comentarios

    def ranking(self):
        if not self.feed.cabeza:
            return None
        max_likes = -1
        top_post = None
        actual = self.feed.cabeza
        start = actual
        while True:
            if actual.dato.likes > max_likes:
                max_likes = actual.dato.likes
                top_post = actual.dato
            actual = actual.siguiente
            if actual == start:
                break
        return top_post

    def buscar_publicacion_doble(self, palabra):
        nodo = self.feed_doble.buscar(palabra)
        if nodo:
            print(f"Publicacion buscada: {nodo.dato.contenido}")
            return nodo
        return None

    def siguiente_publicacion(self):
        nodo = self.feed_doble.siguiente()
        if nodo:
            print(f"Siguiente publicacion: {nodo.dato.contenido}")
            return nodo
        else:
            print("No existe una publicacion siguiente")
            return None

    def anterior_publicacion(self):
        nodo = self.feed_doble.anterior()
        if nodo:
            print(f"Publicación anterior: {nodo.dato.contenido}")
            return nodo
        else:
            print("No existe una publicacion anterior")
            return None

    def publicacion_actual(self):
        nodo = self.feed_doble.publicacion_actual()
        if nodo:
            return nodo
        return None

    def eliminar_publicacion_doble(self, palabra):
        if self.feed_doble.eliminar(palabra):
            self.feed.eliminar(palabra)
            return True
        return False