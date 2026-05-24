# Nodo de la matriz dispersa
class NodoMatriz:
    def __init__(self, fila, columna, color):
        self.fila    = fila
        self.columna = columna
        self.color   = color      # string hex, ej: "#e74c3c"
        self.derecha  = None      # siguiente en la misma fila
        self.abajo    = None      # siguiente en la misma columna

# Nodo cabecera (para filas y columnas)
class NodoCabecera:
    def __init__(self, indice):
        self.indice   = indice
        self.siguiente = None     # siguiente cabecera
        self.acceso    = None     # primer nodo de datos en esta fila/columna

class MatrizDispersa:
    def __init__(self):
        self.cabeceras_filas    = None   # lista de cabeceras de filas
        self.cabeceras_columnas = None   # lista de cabeceras de columnas

    # ── Helpers para obtener o crear cabeceras ──────────────────────────

    def _obtener_cabecera_fila(self, fila, crear=True):
        actual = self.cabeceras_filas
        anterior = None
        while actual and actual.indice < fila:
            anterior = actual
            actual   = actual.siguiente
        if actual and actual.indice == fila:
            return actual
        if not crear:
            return None
        nuevo = NodoCabecera(fila)
        nuevo.siguiente = actual
        if anterior:
            anterior.siguiente = nuevo
        else:
            self.cabeceras_filas = nuevo
        return nuevo

    def _obtener_cabecera_columna(self, columna, crear=True):
        actual = self.cabeceras_columnas
        anterior = None
        while actual and actual.indice < columna:
            anterior = actual
            actual   = actual.siguiente
        if actual and actual.indice == columna:
            return actual
        if not crear:
            return None
        nuevo = NodoCabecera(columna)
        nuevo.siguiente = actual
        if anterior:
            anterior.siguiente = nuevo
        else:
            self.cabeceras_columnas = nuevo
        return nuevo

    # ── Insertar un píxel ───────────────────────────────────────────────

    def insertar(self, fila, columna, color):
        cab_fila = self._obtener_cabecera_fila(fila)
        cab_col  = self._obtener_cabecera_columna(columna)

        nuevo = NodoMatriz(fila, columna, color)

        # Insertar en la lista horizontal (fila)
        actual   = cab_fila.acceso
        anterior = None
        while actual and actual.columna < columna:
            anterior = actual
            actual   = actual.derecha
        if actual and actual.columna == columna:
            actual.color = color   # actualizar si ya existe
            return
        nuevo.derecha = actual
        if anterior:
            anterior.derecha = nuevo
        else:
            cab_fila.acceso = nuevo

        # Insertar en la lista vertical (columna)
        actual   = cab_col.acceso
        anterior = None
        while actual and actual.fila < fila:
            anterior = actual
            actual   = actual.abajo
        nuevo.abajo = actual
        if anterior:
            anterior.abajo = nuevo
        else:
            cab_col.acceso = nuevo

    # ── Obtener color de un píxel ───────────────────────────────────────

    def obtener(self, fila, columna):
        cab_fila = self._obtener_cabecera_fila(fila, crear=False)
        if not cab_fila:
            return None
        actual = cab_fila.acceso
        while actual:
            if actual.columna == columna:
                return actual.color
            if actual.columna > columna:
                break
            actual = actual.derecha
        return None

    # ── Dimensiones de la capa ──────────────────────────────────────────

    def dimensiones(self):
        max_fila = 0
        max_col  = 0
        cab = self.cabeceras_filas
        while cab:
            if cab.indice > max_fila:
                max_fila = cab.indice
            nodo = cab.acceso
            while nodo:
                if nodo.columna > max_col:
                    max_col = nodo.columna
                nodo = nodo.derecha
            cab = cab.siguiente
        return max_fila, max_col

    # ── Iterador de todos los nodos ─────────────────────────────────────

    def todos_los_nodos(self):
        """Retorna lista de (fila, columna, color)"""
        resultado = []
        cab = self.cabeceras_filas
        while cab:
            nodo = cab.acceso
            while nodo:
                resultado.append((nodo.fila, nodo.columna, nodo.color))
                nodo = nodo.derecha
            cab = cab.siguiente
        return resultado