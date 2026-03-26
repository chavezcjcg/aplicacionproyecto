import json
import os
from datetime import datetime

from Controladores.feed import ControladorFeed
from Estructuras.lista_simple import ListaEnlazada
from Servicios.buscar import BuscadorFeed


controlador = ControladorFeed()
lista_memoria = ListaEnlazada()
controlador.iniciar_sistema(lista_memoria)

usuarios = controlador.servicios.cargar_usuarios()


def registrar_usuario(username, password):
    if username.strip() == "" or username in usuarios:
        return False
    
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    usuarios[username] = {"password": password, "bio": "Sin bio aún.", "unirse": fecha}
    
    controlador.servicios.guardar_usuarios(usuarios) 
    return True

def validar_login(username, password):
    if username in usuarios:
        return usuarios[username]["password"] == password
    return False


def obtener_perfil(username):
    return usuarios.get(username, {})


def actualizar_bio(username, nueva_bio):
    if username in usuarios:
        usuarios[username]["bio"] = nueva_bio
        controlador.servicios.guardar_usuarios(usuarios)


def crear_post(autor, texto):
    if texto.strip() == "":
        return False
    controlador.crear_publicacion(texto, autor)
    return True


def obtener_posts():
    lista_ui = []
    actual = controlador.lista_principal.cabeza
    while actual is not None:
        post = {
            "autor": actual.usuario,
            "texto": actual.texto,
            "likes": actual.likes,
            "comentarios": actual.comentarios
        }

        lista_ui.append(post)
        actual = actual.siguiente
    return lista_ui


def contar_posts(username):
    contador = 0
    actual = controlador.lista_principal.cabeza
    while actual is not None:
        if actual.usuario == username:
            contador += 1
        actual = actual.siguiente
    return contador

# Ya esta la funcion de agregar like, solo hay que hacer cuando el usuario haga clic en el boton, se llame a esa funcion pasando el texto del post
def agregar_like(usuario, texto):
    nuevo_like = controlador.dar_like(usuario, texto)
    return nuevo_like

def buscar_post_ui(palabra_clave):
    resultados_nodos = BuscadorFeed.buscar_por_palabra(controlador.lista_principal, palabra_clave)
    
    lista_para_ui = []

    for actual in resultados_nodos:
        post_diccionario = {
            "autor": actual.usuario, 
            "texto": actual.texto,
            "likes": actual.likes,
            "comentarios": actual.comentarios
        }
        lista_para_ui.append(post_diccionario)
        
    return lista_para_ui