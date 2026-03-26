class Nodo():
    def __init__(self,texto, usuario="Usuario"):
        self.texto = texto
        self.usuario = usuario
        self.siguiente = None
        self.anterior = None
        self.likes = 0
        self.favorito = 0
        self.comentarios = []

'''Modifique el nodo para probar lo que implemente'''