import os
import sys
from estructuras.arbol_bb       import ArbolBB
from estructuras.lista_circular import ListaCircular
from modelos.capa               import Capa
from modelos.imagen             import Imagen
from modelos.usuario            import Usuario

# ── Graphviz ────────────────────────────────────────────────────────────
try:
    import graphviz
except ImportError:
    print("Instala graphviz: pip install graphviz")
    sys.exit(1)

# ── Estructuras globales ─────────────────────────────────────────────────
arbol_capas    = ArbolBB()
lista_imagenes = ListaCircular()
arbol_usuarios = ArbolBB()

os.makedirs("reportes", exist_ok=True)

# ════════════════════════════════════════════════════════════════════════
#  CARGA MASIVA
# ════════════════════════════════════════════════════════════════════════

def cargar_capas(ruta):
    try:
        with open(ruta, "r") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"  [!] No se encontró {ruta}")
        return

    id_capa = None
    capa    = None

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        # Si la línea es solo un número, es el ID de la capa
        if linea.isdigit():
            # Guardar capa anterior si existe
            if capa is not None:
                arbol_capas.insertar(id_capa, capa)
                print(f"  Capa {id_capa} cargada.")
            id_capa = int(linea)
            capa    = Capa(id_capa)
        else:
            # Es una línea de píxel: fila,columna,#color
            partes = linea.split(",")
            if len(partes) == 3 and capa is not None:
                try:
                    fila  = int(partes[0])
                    col   = int(partes[1])
                    color = partes[2].strip()
                    capa.agregar_pixel(fila, col, color)
                except ValueError:
                    continue

    # Guardar la última capa
    if capa is not None:
        arbol_capas.insertar(id_capa, capa)
        print(f"  Capa {id_capa} cargada.")

def cargar_imagenes(ruta):
    try:
        with open(ruta, "r") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"  [!] No se encontró {ruta}")
        return

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        id_img = int(linea.split("{")[0])
        imagen = Imagen(id_img)
        interior = linea.split("{")[1].rstrip("}")
        if interior.strip():
            for id_capa_str in interior.split(","):
                id_capa = int(id_capa_str.strip())
                capa = arbol_capas.buscar(id_capa)
                if capa:
                    imagen.agregar_capa(capa)
                else:
                    print(f"  [!] Capa {id_capa} no encontrada para imagen {id_img}")
        lista_imagenes.insertar(id_img, imagen)
        print(f"  Imagen {id_img} cargada.")

def cargar_usuarios(ruta):
    try:
        with open(ruta, "r") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"  [!] No se encontró {ruta}")
        return

    for linea in lineas:
        linea = linea.strip().rstrip(";")
        if not linea:
            continue
        nombre, resto = linea.split(":", 1)
        usuario = Usuario(nombre.strip())
        if resto.strip():
            for id_img_str in resto.split(","):
                id_img = int(id_img_str.strip())
                img = lista_imagenes.buscar(id_img)
                if img:
                    usuario.agregar_imagen(img)
                else:
                    print(f"  [!] Imagen {id_img} no encontrada para {nombre}")
        arbol_usuarios.insertar(nombre.strip(), usuario)
        print(f"  Usuario {nombre.strip()} cargado.")

def carga_masiva():
    print("\n── Carga masiva ──")
    carpeta = "archivos_carga"

    # 1. Primero todas las capas
    cargar_capas(os.path.join(carpeta, "Prueba.cap"))
    cargar_capas(os.path.join(carpeta, "CapaUsuario2.cap"))

    # 2. Luego imágenes
    cargar_imagenes(os.path.join(carpeta, "imagenes.im"))

    # 3. Luego usuarios
    cargar_usuarios(os.path.join(carpeta, "usuarios.usr"))

    print("── Carga completa ──\n")

# ════════════════════════════════════════════════════════════════════════
#  GENERACIÓN DE IMÁGENES
# ════════════════════════════════════════════════════════════════════════

def generar_imagen_desde_capas(capas, nombre_archivo):
    try:
        from PIL import Image as PILImage
    except ImportError:
        print("  [!] Instala Pillow: pip install Pillow")
        return

    if not capas:
        print("  [!] No hay capas para generar imagen.")
        return

    max_fila = 0
    max_col  = 0
    for capa in capas:
        f, c = capa.dimensiones()
        if f > max_fila: max_fila = f
        if c > max_col:  max_col  = c

    ancho  = max_col + 1
    alto   = max_fila + 1
    escala = 20

    img = PILImage.new("RGB", (ancho * escala, alto * escala), "white")
    pixels = img.load()

    for capa in capas:
        for fila, col, color in capa.todos_los_pixeles():
            try:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
            except Exception:
                continue
            for dy in range(escala):
                for dx in range(escala):
                    pixels[col * escala + dx, fila * escala + dy] = (r, g, b)

    ruta = os.path.join("reportes", nombre_archivo + ".png")
    img.save(ruta)
    print(f"  Imagen guardada en {ruta}")

def menu_generacion():
    while True:
        print("\n── Generación de imágenes ──")
        print("  1. Por recorrido limitado (preorden/inorden/postorden)")
        print("  2. Por lista de imágenes (id de imagen)")
        print("  3. Por capa (id de capa)")
        print("  4. Por usuario")
        print("  0. Volver")
        op = input("Opción: ").strip()

        if op == "1":
            try:
                n = int(input("Número de capas a usar: "))
                print("Tipo de recorrido: 1=Inorden  2=Preorden  3=Postorden")
                t = input("Tipo: ").strip()
                if t == "1":
                    recorrido = arbol_capas.inorden()
                    nombre    = "recorrido_inorden"
                elif t == "2":
                    recorrido = arbol_capas.preorden()
                    nombre    = "recorrido_preorden"
                elif t == "3":
                    recorrido = arbol_capas.postorden()
                    nombre    = "recorrido_postorden"
                else:
                    print("  [!] Opción inválida.")
                    continue
                capas = [v for _, v in recorrido[:n]]
                generar_imagen_desde_capas(capas, nombre)
            except ValueError:
                print("  [!] Entrada inválida.")

        elif op == "2":
            try:
                id_img = int(input("ID de imagen: "))
                imagen = lista_imagenes.buscar(id_img)
                if imagen:
                    generar_imagen_desde_capas(imagen.obtener_capas(), f"imagen_{id_img}")
                else:
                    print(f"  [!] Imagen {id_img} no encontrada.")
            except ValueError:
                print("  [!] Entrada inválida.")

        elif op == "3":
            try:
                id_capa = int(input("ID de capa: "))
                capa = arbol_capas.buscar(id_capa)
                if capa:
                    generar_imagen_desde_capas([capa], f"capa_{id_capa}")
                else:
                    print(f"  [!] Capa {id_capa} no encontrada.")
            except ValueError:
                print("  [!] Entrada inválida.")

        elif op == "4":
            nombre = input("Nombre de usuario: ").strip()
            usuario = arbol_usuarios.buscar(nombre)
            if not usuario:
                print(f"  [!] Usuario {nombre} no encontrado.")
                continue
            imagenes = usuario.obtener_imagenes()
            if not imagenes:
                print("  [!] El usuario no tiene imágenes.")
                continue
            print("  Imágenes del usuario:")
            for img in imagenes:
                print(f"    - ID {img.id_imagen}")
            try:
                id_img = int(input("  ID de imagen a generar: "))
                img = usuario.imagenes.buscar(id_img)
                if img:
                    generar_imagen_desde_capas(img.obtener_capas(), f"usuario_{nombre}_img_{id_img}")
                else:
                    print(f"  [!] Imagen {id_img} no encontrada en el usuario.")
            except ValueError:
                print("  [!] Entrada inválida.")

        elif op == "0":
            break

# ════════════════════════════════════════════════════════════════════════
#  CRUD
# ════════════════════════════════════════════════════════════════════════

def menu_crud_usuarios():
    while True:
        print("\n── CRUD Usuarios ──")
        print("  1. Agregar usuario")
        print("  2. Eliminar usuario")
        print("  3. Modificar usuario (cambiar nombre)")
        print("  0. Volver")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre del nuevo usuario: ").strip()
            if arbol_usuarios.buscar(nombre):
                print(f"  [!] El usuario {nombre} ya existe.")
            else:
                arbol_usuarios.insertar(nombre, Usuario(nombre))
                print(f"  Usuario {nombre} agregado.")

        elif op == "2":
            nombre = input("Nombre del usuario a eliminar: ").strip()
            if arbol_usuarios.buscar(nombre):
                arbol_usuarios.eliminar(nombre)
                print(f"  Usuario {nombre} eliminado.")
            else:
                print(f"  [!] Usuario {nombre} no encontrado.")

        elif op == "3":
            nombre = input("Nombre del usuario a modificar: ").strip()
            usuario = arbol_usuarios.buscar(nombre)
            if not usuario:
                print(f"  [!] Usuario {nombre} no encontrado.")
                continue
            nuevo_nombre = input("Nuevo nombre: ").strip()
            arbol_usuarios.eliminar(nombre)
            usuario.nombre = nuevo_nombre
            arbol_usuarios.insertar(nuevo_nombre, usuario)
            print(f"  Usuario renombrado a {nuevo_nombre}.")

        elif op == "0":
            break

def menu_crud_imagenes():
    while True:
        print("\n── CRUD Imágenes ──")
        print("  1. Agregar imagen a usuario")
        print("  2. Eliminar imagen")
        print("  0. Volver")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre del usuario: ").strip()
            usuario = arbol_usuarios.buscar(nombre)
            if not usuario:
                print(f"  [!] Usuario {nombre} no encontrado.")
                continue
            try:
                id_img = int(input("ID de la imagen: "))
            except ValueError:
                print("  [!] ID inválido.")
                continue
            if lista_imagenes.buscar(id_img):
                print(f"  [!] El ID {id_img} ya existe en el sistema.")
                continue
            imagen = Imagen(id_img)
            lista_imagenes.insertar(id_img, imagen)
            usuario.agregar_imagen(imagen)
            print(f"  Imagen {id_img} creada y asignada a {nombre}.")

        elif op == "2":
            nombre = input("Nombre del usuario: ").strip()
            usuario = arbol_usuarios.buscar(nombre)
            if not usuario:
                print(f"  [!] Usuario {nombre} no encontrado.")
                continue
            try:
                id_img = int(input("ID de la imagen a eliminar: "))
            except ValueError:
                print("  [!] ID inválido.")
                continue
            if usuario.eliminar_imagen(id_img):
                lista_imagenes.eliminar(id_img)
                print(f"  Imagen {id_img} eliminada.")
            else:
                print(f"  [!] La imagen {id_img} no pertenece a {nombre}.")

        elif op == "0":
            break

# ════════════════════════════════════════════════════════════════════════
#  REPORTES GRAPHVIZ
# ════════════════════════════════════════════════════════════════════════

def reporte_arbol_capas():
    dot = graphviz.Digraph("arbol_capas", format="png")
    dot.attr(rankdir="TB")

    def agregar_nodos(nodo):
        if nodo is None:
            return
        dot.node(str(nodo.clave), f"Capa {nodo.clave}")
        if nodo.izquierda:
            dot.edge(str(nodo.clave), str(nodo.izquierda.clave))
            agregar_nodos(nodo.izquierda)
        if nodo.derecha:
            dot.edge(str(nodo.clave), str(nodo.derecha.clave))
            agregar_nodos(nodo.derecha)

    agregar_nodos(arbol_capas.raiz)
    dot.render(os.path.join("reportes", "arbol_capas"), cleanup=True)
    print("  Reporte árbol de capas generado en reportes/arbol_capas.png")

def reporte_arbol_usuarios():
    dot = graphviz.Digraph("arbol_usuarios", format="png")
    dot.attr(rankdir="TB")

    def agregar_nodos(nodo):
        if nodo is None:
            return
        dot.node(nodo.clave, nodo.clave)
        if nodo.izquierda:
            dot.edge(nodo.clave, nodo.izquierda.clave)
            agregar_nodos(nodo.izquierda)
        if nodo.derecha:
            dot.edge(nodo.clave, nodo.derecha.clave)
            agregar_nodos(nodo.derecha)

    agregar_nodos(arbol_usuarios.raiz)
    dot.render(os.path.join("reportes", "arbol_usuarios"), cleanup=True)
    print("  Reporte árbol de usuarios generado en reportes/arbol_usuarios.png")

def reporte_lista_imagenes():
    dot = graphviz.Digraph("lista_imagenes", format="png")
    dot.attr(rankdir="LR")
    elementos = lista_imagenes.todos()
    for clave, img in elementos:
        capas_ids = [str(c.id_capa) for c in img.obtener_capas()]
        etiqueta  = f"Img {clave}\ncapas: {', '.join(capas_ids) if capas_ids else 'ninguna'}"
        dot.node(str(clave), etiqueta)
    for i in range(len(elementos)):
        actual    = elementos[i][0]
        siguiente = elementos[(i + 1) % len(elementos)][0]
        dot.edge(str(actual), str(siguiente))
        dot.edge(str(siguiente), str(actual), style="dashed")
    dot.render(os.path.join("reportes", "lista_imagenes"), cleanup=True)
    print("  Reporte lista de imágenes generado en reportes/lista_imagenes.png")

def reporte_matriz_capa():
    try:
        id_capa = int(input("ID de capa a reportar: "))
    except ValueError:
        print("  [!] ID inválido.")
        return
    capa = arbol_capas.buscar(id_capa)
    if not capa:
        print(f"  [!] Capa {id_capa} no encontrada.")
        return

    dot = graphviz.Digraph(f"matriz_capa_{id_capa}", format="png")
    dot.attr(rankdir="LR")
    dot.node("matriz", "Matriz", shape="box")

    for fila, col, color in capa.todos_los_pixeles():
        nodo_id = f"n_{fila}_{col}"
        dot.node(nodo_id, f"({fila},{col})\n{color}", style="filled", fillcolor=color)
        dot.edge("matriz", nodo_id)

    dot.render(os.path.join("reportes", f"matriz_capa_{id_capa}"), cleanup=True)
    print(f"  Reporte matriz capa {id_capa} generado en reportes/matriz_capa_{id_capa}.png")

def menu_reportes():
    while True:
        print("\n── Estado de la memoria ──")
        print("  1. Ver lista de imágenes")
        print("  2. Ver árbol de capas")
        print("  3. Ver matriz de una capa")
        print("  4. Ver árbol de usuarios")
        print("  0. Volver")
        op = input("Opción: ").strip()

        if op == "1":
            reporte_lista_imagenes()
        elif op == "2":
            reporte_arbol_capas()
        elif op == "3":
            reporte_matriz_capa()
        elif op == "4":
            reporte_arbol_usuarios()
        elif op == "0":
            break

# ════════════════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ════════════════════════════════════════════════════════════════════════

def main():
    carga_masiva()
    while True:
        print("\n╔══════════════════════════════╗")
        print("║  Generador de imágenes       ║")
        print("╠══════════════════════════════╣")
        print("║  1. Generar imagen           ║")
        print("║  2. CRUD Usuarios            ║")
        print("║  3. CRUD Imágenes            ║")
        print("║  4. Estado de la memoria     ║")
        print("║  0. Salir                    ║")
        print("╚══════════════════════════════╝")
        op = input("Opción: ").strip()

        if op == "1":
            menu_generacion()
        elif op == "2":
            menu_crud_usuarios()
        elif op == "3":
            menu_crud_imagenes()
        elif op == "4":
            menu_reportes()
        elif op == "0":
            print("  Hasta luego.")
            break
        else:
            print("  [!] Opción inválida.")

if __name__ == "__main__":
    main()