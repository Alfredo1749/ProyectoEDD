# Lista Circular Doblemente Enlazada
# Usada para almacenar las imágenes del sistema, ordenadas por id

class NodoCircular:
    def __init__(self, clave, valor):
        self.clave    = clave    # id de la imagen
        self.valor    = valor    # objeto Imagen
        self.siguiente = None
        self.anterior  = None

class ListaCircular:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    # ── Insertar ordenado por clave ──────────────────────────────────────

    def insertar(self, clave, valor):
        nuevo = NodoCircular(clave, valor)

        if self.cabeza is None:
            nuevo.siguiente = nuevo
            nuevo.anterior  = nuevo
            self.cabeza = nuevo
            self.tamanio += 1
            return

        # Buscar posición ordenada
        actual = self.cabeza
        while True:
            if clave < actual.clave:
                # Insertar antes de actual
                anterior = actual.anterior
                anterior.siguiente = nuevo
                nuevo.anterior     = anterior
                nuevo.siguiente    = actual
                actual.anterior    = nuevo
                if actual == self.cabeza:
                    self.cabeza = nuevo
                self.tamanio += 1
                return
            if actual.siguiente == self.cabeza:
                break
            actual = actual.siguiente

        # Insertar al final
        ultimo = self.cabeza.anterior
        ultimo.siguiente    = nuevo
        nuevo.anterior      = ultimo
        nuevo.siguiente     = self.cabeza
        self.cabeza.anterior = nuevo
        self.tamanio += 1

    # ── Buscar por clave ─────────────────────────────────────────────────

    def buscar(self, clave):
        if self.cabeza is None:
            return None
        actual = self.cabeza
        while True:
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None

    # ── Eliminar por clave ───────────────────────────────────────────────

    def eliminar(self, clave):
        if self.cabeza is None:
            return False
        actual = self.cabeza
        while True:
            if actual.clave == clave:
                if self.tamanio == 1:
                    self.cabeza = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                    if actual == self.cabeza:
                        self.cabeza = actual.siguiente
                self.tamanio -= 1
                return True
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return False

    # ── Obtener todos los elementos ──────────────────────────────────────

    def todos(self):
        resultado = []
        if self.cabeza is None:
            return resultado
        actual = self.cabeza
        while True:
            resultado.append((actual.clave, actual.valor))
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return resultado

    def esta_vacia(self):
        return self.cabeza is None