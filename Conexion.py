import tkinter as tk
from Helpers import *
from DB_Almacen import *

# -----------------------------------------------
# Crear ventana principal
ventana = tk.Tk()
ventana.title("Conexiones DB")
ventana.config(bg="#e8f5e9")
ventana.overrideredirect(True)
ventana.resizable(True, True)  # Barra de Windows

# -----------------------------------------------
# Volver a Pantalla Principal
def Home():
    ventana.destroy()
    import Proyecto

# -----------------------------------------------
# Pasar a DB Clientes
def Clientes():
    ventana.destroy()
    import DB_Clientes

# -----------------------------------------------
# Pasar a DB Almacen
def Almacen():
    ventana.destroy()
    iniciar_interfaz_almacen()

# -----------------------------------------------
# Mover Ventana
def iniciar_movimiento(event):
    ventana.x = event.x
    ventana.y = event.y

def mover_ventana(event):
    x = event.x_root - ventana.x
    y = event.y_root - ventana.y
    ventana.geometry(f"+{x}+{y}")

# -----------------------------------------------
# Barra superior usando pack
barra_superior = tk.Frame(ventana, bg="#2e7d32", height=30)
barra_superior.pack(fill="x")

# -----------------------------------------------
# Etiqueta en la barra superior (Alineada a la izquierda)
tk.Label(barra_superior, text="🍅 Tienda de Verduras", bg="#2e7d32", fg="white", font=("Bookman Old Style", 12, "italic")).pack(side="left", padx=10)

# -----------------------------------------------
# Botones en la barra superior (Alineados a la derecha)
tk.Button(barra_superior, text=" X ", bg="#c62828", fg="white", font=("Bookman Old Style", 12), command=ventana.destroy).pack(side="right", padx=10)
tk.Button(barra_superior, text=" 🏠 ", bg="#0a497b", fg="white", font=("Bookman Old Style", 12), command=Home).pack(side="right", padx=10)

barra_superior.bind("<ButtonPress-1>", iniciar_movimiento)
barra_superior.bind("<B1-Motion>", mover_ventana)

# -----------------------------------------------
# Crear un label para el título
titulo = tk.Label(ventana, text="Bases de Datos", font=("Bookman Old Style", 20, "italic"), bg="#e8f5e9", fg="#43a047")
titulo.pack(pady=10)  # Usamos pack aquí para mantener la simplicidad

# -----------------------------------------------
# Crear un Frame para los botones y distribuirlos en 2x2
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=20)

# -----------------------------------------------
# Crear los botones y agregarlos al frame
boton1 = tk.Button(frame_botones, text="Clientes", bg="#43a047", fg="white", width=14, height=6, command=Clientes)
boton2 = tk.Button(frame_botones, text="Almacen", bg="#43a047", fg="white", width=14, height=6, command=Almacen)
boton3 = tk.Button(frame_botones, text="Facturas", bg="#43a047", fg="white", width=14, height=6)
boton4 = tk.Button(frame_botones, text="...", bg="#43a047", fg="white", width=14, height=6)

# -----------------------------------------------
# Empaquetamos los botones en un 2x2
boton1.grid(row=0, column=0, padx=10, pady=10)
boton2.grid(row=0, column=1, padx=10, pady=10)
boton3.grid(row=1, column=0, padx=10, pady=10)
boton4.grid(row=1, column=1, padx=10, pady=10)

# -----------------------------------------------
# Configuración de la cuadrícula para centrar los botones
frame_botones.grid_columnconfigure(0, weight=1)
frame_botones.grid_columnconfigure(1, weight=1)
frame_botones.grid_rowconfigure(0, weight=1)
frame_botones.grid_rowconfigure(1, weight=1)

centrar_ventana(ventana, 400, 350)

# Iniciar la ventana
ventana.mainloop()
