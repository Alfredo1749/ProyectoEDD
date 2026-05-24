from estructuras.matriz_dispersa import MatrizDispersa

class Capa:
    def __init__(self, id_capa):
        self.id_capa = id_capa
        self.matriz  = MatrizDispersa()   # aquí viven los píxeles

    def agregar_pixel(self, fila, columna, color):
        self.matriz.insertar(fila, columna, color)

    def obtener_pixel(self, fila, columna):
        return self.matriz.obtener(fila, columna)

    def dimensiones(self):
        return self.matriz.dimensiones()

    def todos_los_pixeles(self):
        return self.matriz.todos_los_nodos()

    def __str__(self):
        return f"Capa(id={self.id_capa})"