
from Modelos.modelos import Nodo


class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None

    def insertar(self, dato):
        nuevo = Nodo(dato) 
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            self.actual = nuevo
            return
        self.cola.siguiente = nuevo
        nuevo.anterior = self.cola
        self.cola = nuevo

    def tamaño(self):
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def buscar(self, palabra):
        actual = self.cabeza
        while actual:
            if palabra in actual.dato.contenido:
                self.actual = actual
                return actual
            actual = actual.siguiente
        return None

    def siguiente(self):
        if self.actual and self.actual.siguiente:
            self.actual = self.actual.siguiente
            return self.actual
        return None

    def anterior(self):
        if self.actual and self.actual.anterior:
            self.actual = self.actual.anterior
            return self.actual
        return None

    def publicacion_actual(self):
        return self.actual

    def establecer_publicacion_actual(self, nodo):
        self.actual = nodo

    def eliminar(self, palabra):
        actual = self.cabeza
        while actual:
            if palabra in actual.dato.contenido:
                if actual == self.cabeza:
                    self.cabeza = actual.siguiente
                    if self.cabeza:
                        self.cabeza.anterior = None
                    else:
                        self.cola = None
                elif actual == self.cola:
                    self.cola = actual.anterior
                    if self.cola:
                        self.cola.siguiente = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                if self.actual == actual:
                    self.actual = actual.siguiente if actual.siguiente else actual.anterior
                return True
            actual = actual.siguiente
        return False
