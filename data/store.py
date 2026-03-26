# data/store.py

usuarios = {}  # { "username": {"password": ..., "bio": ..., "unirse": ...} }
posts = []     # [ { "autor": ..., "texto": ..., "likes": 0, "comentarios": [] } ]


def registrar_usuario(username, password):
    if username.strip() == "" or username in usuarios:
        return False
    usuarios[username] = {"password": password, "bio": "Sin bio aún.", "unirse": "Marzo 2026"}
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


def crear_post(autor, texto):
    if texto.strip() == "":
        return False
    posts.append({"autor": autor, "texto": texto, "likes": 0, "comentarios": []})
    return True


def obtener_posts():
    return list(reversed(posts))


def contar_posts(username):
    return sum(1 for p in posts if p["autor"] == username)

def dar_like(indice_real):
    if 0 <= indice_real < len(posts):
        posts[indice_real]["likes"] += 1