# Una imagen tiene un id y una lista de capas (en orden de superposición)
# Cada nodo de la lista apunta directamente al objeto Capa en el árbol (no es copia)

class NodoCapaImagen:
    def __init__(self, capa):
        self.capa      = capa    # referencia directa al objeto Capa
        self.siguiente = None

class Imagen:
    def __init__(self, id_imagen):
        self.id_imagen  = id_imagen
        self.cabeza_capas = None   # lista simple de capas en orden de inserción
        self.total_capas  = 0

    # ── Agregar capa al final de la lista ────────────────────────────────

    def agregar_capa(self, capa):
        nuevo = NodoCapaImagen(capa)
        if self.cabeza_capas is None:
            self.cabeza_capas = nuevo
        else:
            actual = self.cabeza_capas
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.total_capas += 1

    # ── Obtener capas en orden de superposición ──────────────────────────

    def obtener_capas(self):
        """Retorna lista de objetos Capa en orden de superposición (primero = abajo)"""
        capas = []
        actual = self.cabeza_capas
        while actual:
            capas.append(actual.capa)
            actual = actual.siguiente
        return capas

    def tiene_capas(self):
        return self.cabeza_capas is not None

    def __str__(self):
        ids = [str(c.id_capa) for c in self.obtener_capas()]
        return f"Imagen(id={self.id_imagen}, capas=[{', '.join(ids)}])"