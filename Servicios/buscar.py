class BuscadorFeed:
    @staticmethod
    def contar_publicacones(lista):
        if lista.cabeza is None: #Cuenta total de nodos
            return 0
        
        contador = 0
        actual = lista.cabeza
        nodos_visibles = set()

        while actual is not None: #evita ciclos infinitos 
            if id(actual) in nodos_visibles:
                break

            nodos_visibles.add(id(actual))
            contador += 1
            actual = actual.siguiente

        return contador
    
    @staticmethod
    def buscar_por_palabra(lista, palabra_clave):
        resultados = []
        if lista.cabeza is None:
            return resultados
        
        actual = lista.cabeza
        nodos_visitados = set()
        palabra_clave = palabra_clave.lower()

        while actual is not None:
            if id(actual) in nodos_visitados:
                break

            nodos_visitados.add(id(actual))

            if palabra_clave in actual.texto.lower():
                resultados.append(actual)

            actual = actual.siguiente

        return resultados