import sys
from PyQt6.QtWidgets import QApplication
from Estructuras.lista_simple import ListaEnlazada
from Controladores.feed import ControladorFeed
from ui.pagina_principal import MainWindow


def main():
    lista = ListaEnlazada()
    controlador = ControladorFeed()
    controlador.iniciar_sistema(lista)

    app = QApplication(sys.argv)
    window = MainWindow(controlador)
    window.show()
    sys.exit(app.exec())


main()