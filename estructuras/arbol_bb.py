# Árbol Binario de Búsqueda genérico
# Usado para: capas (clave = id_capa) y usuarios (clave = nombre)

class NodoArbol:
    def __init__(self, clave, valor):
        self.clave    = clave    # int para capas, str para usuarios
        self.valor    = valor    # objeto Capa o Usuario
        self.izquierda = None
        self.derecha   = None

class ArbolBB:
    def __init__(self):
        self.raiz = None

    # ── Insertar ────────────────────────────────────────────────────────

    def insertar(self, clave, valor):
        if not self.raiz:
            self.raiz = NodoArbol(clave, valor)
        else:
            self._insertar_recursivo(self.raiz, clave, valor)

    def _insertar_recursivo(self, nodo, clave, valor):
        if clave < nodo.clave:
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.izquierda, clave, valor)
        elif clave > nodo.clave:
            if nodo.derecha is None:
                nodo.derecha = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.derecha, clave, valor)
        else:
            nodo.valor = valor   # actualizar si la clave ya existe

    # ── Buscar ──────────────────────────────────────────────────────────

    def buscar(self, clave):
        return self._buscar_recursivo(self.raiz, clave)

    def _buscar_recursivo(self, nodo, clave):
        if nodo is None:
            return None
        if clave == nodo.clave:
            return nodo.valor
        if clave < nodo.clave:
            return self._buscar_recursivo(nodo.izquierda, clave)
        return self._buscar_recursivo(nodo.derecha, clave)

    # ── Eliminar ────────────────────────────────────────────────────────

    def eliminar(self, clave):
        self.raiz = self._eliminar_recursivo(self.raiz, clave)

    def _eliminar_recursivo(self, nodo, clave):
        if nodo is None:
            return None
        if clave < nodo.clave:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, clave)
        elif clave > nodo.clave:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, clave)
        else:
            # Nodo encontrado
            if nodo.izquierda is None:
                return nodo.derecha
            if nodo.derecha is None:
                return nodo.izquierda
            # Tiene dos hijos: reemplazar con sucesor inorden
            sucesor = self._minimo(nodo.derecha)
            nodo.clave  = sucesor.clave
            nodo.valor  = sucesor.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.clave)
        return nodo

    def _minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    # ── Recorridos ──────────────────────────────────────────────────────

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izquierda, resultado)
            resultado.append((nodo.clave, nodo.valor))
            self._inorden(nodo.derecha, resultado)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, resultado):
        if nodo:
            resultado.append((nodo.clave, nodo.valor))
            self._preorden(nodo.izquierda, resultado)
            self._preorden(nodo.derecha, resultado)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, resultado):
        if nodo:
            self._postorden(nodo.izquierda, resultado)
            self._postorden(nodo.derecha, resultado)
            resultado.append((nodo.clave, nodo.valor))

    def esta_vacio(self):
        return self.raiz is None