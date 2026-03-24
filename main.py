from Estructuras.lista_simple import ListaEnlazada
from Modelos.modelos import Nodo
import sys
from PyQt6.QtWidgets import QApplication
from ui.pagina_principal import MainWindow 
from Controladores.feed import ControladorFeed

#ListaEnlazada.menu()

controlador = ControladorFeed()
lista_memoria = ListaEnlazada()

def agregar_al_iniciotemp(nodo_nuevo):
    nodo_nuevo.siguiente = lista_memoria.cabeza
    lista_memoria.cabeza = nodo_nuevo

lista_memoria.agregar_al_inicio = agregar_al_iniciotemp
controlador.iniciar_sistema(lista_memoria)

controlador.crear_publicacion("HOlaaaaaaaaaaaaaaaa prueba de publicacion")
controlador.crear_publicacion("Prueba para buscaar uan palabra. Estupendo dia xd")
controlador.crear_publicacion("Juasndkan lajsld laksj lxm")

palabra = "estupendo dia"
encontrar = controlador.buscar_publicacion(palabra)
if encontrar:
    post_actual = controlador.obtener_post_actual()
    print(f"se econtro la palabra: {palabra} en el siguiente texto: {post_actual.texto}")
else:
    print(f"No se encontro la palabra: {palabra}")

#contar post
total = controlador.obtener_total_publicaciones()
print(f"Total de publicaciones: {total}")

def main():
    app = QApplication(sys.argv)

    window = MainWindow()   
    window.show()

    sys.exit(app.exec())

main()