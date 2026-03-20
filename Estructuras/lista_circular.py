from Modelos.modelos import Nodo
class Publicacion():
    def __init__(self,usuario, contenido):
        self.usuario = usuario
        self.contenido = contenido
        self.likes = 0
class ListaCircular():
    def __init__(self):
        self.cabeza = None

