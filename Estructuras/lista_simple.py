from Modelos.modelos import Nodo
class Comentario:
    def __init__(self, usuario, texto):
        self.usuario = usuario
        self.texto = texto

class Publicacion():
    def __init__(self,usuario, contenido):
        self.usuario = usuario
        self.contenido = contenido
        self.likes = 0
        self.favorito = False

class Usuario:
    def __init__(self,nombre, contrasenia, usuario):
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.usuario = usuario

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def buscar(self, usuario):
        actual = self.cabeza
        while actual:
            if actual.dato.nombre.lower() == usuario.lower():
                return True
            actual = actual.siguiente
        return False
    
    def registrar_usuario(self,nombre,contrasenia, usuario):
        if self.buscar(usuario):
            print ("No se puede")
            return False
        nuevo_usuario = Usuario(nombre,contrasenia,usuario)
        nuevo = Nodo(nuevo_usuario)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo

    
    def iniciar_sesion(self,nombre, contrasenia):
        actual = self.cabeza
        while actual is not None:
            usuario_actual = actual.dato
            if usuario_actual.nombre == nombre and usuario_actual.contrasenia == contrasenia:
                print ("No se puede")
                return True
            actual = actual.siguiente
        return False
    
    def registrar_publicacon(self,usuario, contenido):
        nuevo_publicacon = Publicacion(usuario,contenido)
        nuevo  = Nodo(nuevo_publicacon)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo

    def buscar_publicacion(self,palabra):
        actual = self.cabeza
        while actual:
            if palabra in actual.dato.contenido:
                return actual.dato
            actual = actual.siguiente
        return None
    
    def eliminar_publicacion(self,palabra):
        actual = self.cabeza
        anterior = None
        while actual:
            if palabra in actual.dato.contenido:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        return False
    
    def dar_like():
        pass
                
def menu():
    metodos = ListaEnlazada()
    feed = ListaEnlazada() 
    
    while True:
        print ("1. Registrar Usuario")
        print ("2. Iniciar sesion.")
        print ("3. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            nombre = input("Ingrese su nombre: ")
            usuario = input("Ingrese su usuario: ")
            contrasenia = input('Ingrese su contrasenia: ')
            metodos.registrar_usuario(nombre, contrasenia, usuario)
        elif opcion == "2":
            nombre = input("Ingrese su nombre: ")
            contrasenia = input('Ingrese su contrasenia: ')
            if metodos.iniciar_sesion(nombre, contrasenia):
                print(f"Bienvenido {nombre}")
                while True:
                    print("\n1. registrar publicacon")
                    print("2. buscar publicacion")
                    print("3. eliminar publicacion")
                    print("4. Cerrar sesion")
                    opcion_post = input("Ingrese una opcion: ")
                    if opcion_post == "1":
                        contenido = input("Ingrese el contenido: ")
                        feed.registrar_publicacon(nombre, contenido)
                    elif opcion_post == "2":
                        palabra = input("Ingrese palabra a buscar: ")
                        post = feed.buscar_publicacion(palabra)
                        if post:
                            print(f"Post encontrado: {post.contenido}")
                        else:
                            print("No se encontro")  
                    elif opcion_post == "3":
                        palabra = input("Ingrese palabra para eliminar: ")
                        if feed.eliminar_publicacion(palabra):
                            print("Eliminado con exito")
                        else:
                            print("No se pudo")        
                    elif opcion_post == "4":
                        break
            else:
                print("No se pudo iniciar sesion")
        elif opcion == "3":
            break
        else:
            print ("Ingres una opcion valida")

menu()