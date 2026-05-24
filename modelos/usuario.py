from estructuras.lista_simple import ListaSimple

class Usuario:
    def __init__(self, nombre):
        self.nombre  = nombre
        self.imagenes = ListaSimple()   # lista de imágenes del usuario

    # ── Agregar imagen a la lista del usuario ────────────────────────────

    def agregar_imagen(self, imagen):
        # imagen es un objeto Imagen (referencia, no copia)
        if self.imagenes.buscar(imagen.id_imagen) is not None:
            print(f"  [!] La imagen {imagen.id_imagen} ya está registrada en {self.nombre}")
            return False
        self.imagenes.insertar(imagen.id_imagen, imagen)
        return True

    # ── Eliminar imagen de la lista del usuario ──────────────────────────

    def eliminar_imagen(self, id_imagen):
        return self.imagenes.eliminar(id_imagen)

    # ── Obtener todas las imágenes del usuario ───────────────────────────

    def obtener_imagenes(self):
        return [img for _, img in self.imagenes.todos()]

    def tiene_imagenes(self):
        return not self.imagenes.esta_vacia()

    def __str__(self):
        ids = [str(img.id_imagen) for img in self.obtener_imagenes()]
        return f"Usuario(nombre={self.nombre}, imagenes=[{', '.join(ids)}])"