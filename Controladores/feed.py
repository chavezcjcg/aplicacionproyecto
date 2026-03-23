from Modelos.modelos import Nodo
from Servicios.pers import Servicio
from Servicios.buscar import BuscadorFeed

class ControladorFeed:
    def __init__(self):
        self.lista_principal = None
        self.nodo_actual = None
        self.modo_circular = False #para el modo scroll infinito
        self.servicios = Servicio() #conexion de los servicios

    def iniciar_sistema(self, lista_base):
        self.lista_principal = lista_base
        self.servicios.cargar_feed(self.lista_principal)
        self.nodo_actual = self.lista_principal.cabeza

    def crear_publicacion(self, texto, autor="usuario"):
        nuevo_nodo = Nodo(texto, autor)
        self.lista_principal.agregar_al_inicio(nuevo_nodo) #Crear metodo "agregar al inicio"
        self.nodo_actual = self.lista_principal.cabeza
        self.servicios.guardar_feed(self.lista_principal)
        return self.nodo_actual
    
    def obtener_post_actual(self):
        return self.nodo_actual
    
    def siguiente(self):
        if self.nodo_actual is None:
            return False
        
        if self.nodo_actual is not None:
            self.nodo_actual = self.nodo_actual.siguiente
            return True
        else:
            if self.modo_circular and self.lista_principal.cola is not None:
                self.nodo_actual = self.lista_principal.cola

    def obtener_total_publicaciones(self):
        return BuscadorFeed.contar_publicacones(self.lista_principal)
    
    def buscar_publicacion(self, palabra):
        resultado = BuscadorFeed.buscar_por_palabra(self.lista_principal, palabra)
        if len(resultado):
            self.nodo_actual = resultado[0]
            return True
        return False
                   