from Modelos.modelos import Nodo

class PaginadeAplicacion:
    def __init__(self):
        self.feed = Feed()
        self.modo_automatico_activo = False

    def insertar(self, publicacion):
        self.feed.insertar(publicacion)

    def buscar(self, palabra):
        return self.feed.buscar(palabra)

    def eliminar(self, palabra):
        return self.feed.eliminar(palabra)

    @property
    def cabeza(self):
        return self.feed.cabeza

    def activar_modo_automatico(self):
        """METODOS PARA SCROLL INFINITO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
        self.modo_automatico_activo = True
    def desactivar_modo_automatico(self):
        self.modo_automatico_activo = False
        """METODOS PARA SCROLL INFINITO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    def modo_automatico(self, num_iteraciones):
        """METODOS PARA SCROLL INFINITO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
        if not self.modo_automatico_activo:
            return
        if self.feed.cabeza is None:
            return
        actual = self.feed.cabeza
        contador = 0
        for _ in range(num_iteraciones):
            print(f"Publicación {contador + 1}: {actual.dato.contenido} (Likes: {actual.dato.likes})")
            actual = actual.siguiente
            contador += 1
            if actual == self.feed.cabeza:
                break  
        

class Feed:
    def __init__(self):
        self.cabeza = None

    def insertar(self, publicacion):
        nuevo = Nodo(publicacion)
        if self.cabeza is None:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            return
        ultimo = self.cabeza.anterior
        ultimo.siguiente = nuevo
        nuevo.anterior = ultimo
        nuevo.siguiente = self.cabeza
        self.cabeza.anterior = nuevo

    def buscar(self, palabra):
        if self.cabeza is None:
            return None
        actual = self.cabeza
        while True:
            if palabra in actual.dato.contenido:
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None

    def eliminar(self, palabra):
        if self.cabeza is None:
            return False
        actual = self.cabeza
        while True:
            if palabra in actual.dato.contenido:
                if actual.siguiente == actual:
                    self.cabeza = None
                    return True
                actual.anterior.siguiente = actual.siguiente
                actual.siguiente.anterior = actual.anterior
                if actual == self.cabeza:
                    self.cabeza = actual.siguiente
                return True
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return False