# Lista Simplemente Enlazada
# Usada para la lista de imágenes de cada usuario

class NodoLista:
    def __init__(self, clave, valor):
        self.clave     = clave   # id de la imagen
        self.valor     = valor   # referencia al objeto Imagen
        self.siguiente = None

class ListaSimple:
    def __init__(self):
        self.cabeza  = None
        self.tamanio = 0

    # ── Insertar al final ────────────────────────────────────────────────

    def insertar(self, clave, valor):
        nuevo = NodoLista(clave, valor)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1

    # ── Buscar por clave ─────────────────────────────────────────────────

    def buscar(self, clave):
        actual = self.cabeza
        while actual:
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
        return None

    # ── Eliminar por clave ───────────────────────────────────────────────

    def eliminar(self, clave):
        actual   = self.cabeza
        anterior = None
        while actual:
            if actual.clave == clave:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                self.tamanio -= 1
                return True
            anterior = actual
            actual   = actual.siguiente
        return False

    # ── Obtener todos ────────────────────────────────────────────────────

    def todos(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append((actual.clave, actual.valor))
            actual = actual.siguiente
        return resultado

    def esta_vacia(self):
        return self.cabeza is None