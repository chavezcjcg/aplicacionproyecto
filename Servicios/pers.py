import json
import os
from Modelos.modelos import Nodo

class Servicio:
    def __init__(self, ruta_archivo="datos/feed.json"):
        self.ruta_archivo = ruta_archivo
        self.ruta_usuarios = "datos/usuarios.json"

    def guardar_feed(self, feed):
        datos_guardados = []
        actual = feed.cabeza

        while actual is not None:
            post_directorio = {
                "texto": actual.texto,
                "usuario": actual.usuario,
                "likes": actual.likes,
                "favorito": actual.favorito,
                "comentarios": actual.comentarios
            }
            datos_guardados.append(post_directorio)
            actual = actual.siguiente
        
        with open(self.ruta_archivo, "w", encoding="utf-8") as archivo: #se escribe el archivo Json
            json.dump(datos_guardados, archivo, indent=4, ensure_ascii=False)
        print("Feed Guardado")

    def cargar_feed(self, lista_simple):
        if not os.path.exists(self.ruta_archivo): #verificacion 
            print("No hay archivo, se iniciara un feed vacio")
            return
        
        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            datos_cargados = json.load(archivo)

            for post_data in datos_cargados:
                nuevo_nodo = Nodo(texto=post_data.get("texto", "texto no encontraddo"), usuario=post_data.get("autor", "usuario"))

                nuevo_nodo.likes = post_data["likes"]
                nuevo_nodo.favorito = post_data["favorito"]
                nuevo_nodo.comentarios = post_data["comentarios"]

                lista_simple.agregar_al_final(nuevo_nodo) #crear un nuevo metodo a las listas simple "agregar al final" para que se pueda guardar
    
    def guardar_usuarios(self, diccionario_usuarios):
        """Guarda el diccionario de usuarios en el JSON"""
        with open(self.ruta_usuarios, "w", encoding="utf-8") as archivo:
            json.dump(diccionario_usuarios, archivo, indent=4, ensure_ascii=False)

    def cargar_usuarios(self):
        """Lee el JSON y devuelve el diccionario de usuarios"""
        if not os.path.exists(self.ruta_usuarios):
            return {}
        with open(self.ruta_usuarios, "r", encoding="utf-8") as archivo:
            return json.load(archivo)