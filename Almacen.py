import tkinter as tk
from Helpers import *
from tkinter import ttk, messagebox
import sqlite3

# Productos fijos del almacén
precios_productos = {
    "Manzana": 1200, "Naranja": 800, "Brócoli": 1500, "Zanahoria": 700, "Papa": 500,
    "Tomate": 900, "Cebolla": 600, "Lechuga": 1000, "Pimiento": 1300, "Ajo": 400,
    "Pepino": 850, "Espinaca": 950, "Berenjena": 1100, "Repollo": 1200, "Calabacín": 1250,
    "Apio": 700, "Remolacha": 1000, "Rábano": 600, "Perejil": 500, "Chayote": 900,
    "Maíz": 750, "Yuca": 850, "Aguacate": 2000
}

conn = sqlite3.connect("Tienda.db")
cursor = conn.cursor()

# Insertar si no existe
for nombre, precio in precios_productos.items():
    cursor.execute("SELECT 1 FROM productos WHERE nombre = ?", (nombre,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        print(f"Insertado: {nombre}")
conn.commit()

# Funciones CRUD
def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    cursor.execute("SELECT id_producto, nombre, precio FROM productos")
    for id_, nombre, precio in cursor.fetchall():
        tabla.insert("", tk.END, values=(id_, nombre, int(precio)))

def seleccionar_fila(event):
    item = tabla.focus()
    if item:
        valores = tabla.item(item, "values")
        entrada_nombre.set(valores[1])
        entrada_precio.set(valores[2])
        etiqueta_id.config(text=valores[0])

def crear_producto():
    nombre = entrada_nombre.get()
    try:
        precio = int(entrada_precio.get())
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()
        actualizar_tabla()
        limpiar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El producto ya existe.")
    except ValueError:
        messagebox.showerror("Error", "Precio inválido.")

def actualizar_producto():
    id_ = etiqueta_id.cget("text")
    nombre = entrada_nombre.get()
    try:
        precio = int(entrada_precio.get())
        cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE id_producto = ?", (nombre, precio, id_))
        conn.commit()
        actualizar_tabla()
        limpiar_campos()
    except ValueError:
        messagebox.showerror("Error", "Precio inválido.")

def eliminar_producto():
    id_ = etiqueta_id.cget("text")
    if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este producto?"):
        cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_,))
        conn.commit()
        actualizar_tabla()
        limpiar_campos()

def limpiar_campos():
    entrada_nombre.set("")
    entrada_precio.set("")
    etiqueta_id.config(text="")

# -----------------------------------------------
# Volver a Pantalla Principal
def Home():
    ventana.destroy()
    import Proyecto

# -----------------------------------------------
# Mover Ventana
def iniciar_movimiento(event):
    ventana.x = event.x
    ventana.y = event.y

def mover_ventana(event):
    x = event.x_root - ventana.x
    y = event.y_root - ventana.y
    ventana.geometry(f"+{x}+{y}")

# Interfaz
ventana = tk.Tk()
ventana.title("Almacén de Verduras")
ventana.configure(bg="#e8f5e9")
ventana.overrideredirect(True)
ventana.resizable(True, True)
centrar_ventana(ventana, 1100, 450)

# -----------------------------------------------
# Barra superior
barra_superior = tk.Frame(ventana, bg="#2e7d32", height=30)
barra_superior.pack(fill="x")
tk.Label(barra_superior, text="🍅 Tienda de Verduras", bg="#2e7d32", fg="white", font=("Bookman Old Style", 12, "italic")).pack(side="left", padx=10)
tk.Button(barra_superior, text=" X ", bg="#c62828", fg="white", font=("Bookman Old Style", 12), command=ventana.destroy).pack(side="right", padx=10)
tk.Button(barra_superior, text=" 🏠 ", bg="#0a497b", fg="white", font=("Bookman Old Style", 12), command=Home).pack(side="right", padx=10)

barra_superior.bind("<ButtonPress-1>", iniciar_movimiento)
barra_superior.bind("<B1-Motion>", mover_ventana)

# Formulario
entrada_nombre = tk.StringVar()
entrada_precio = tk.StringVar()

frame_formulario = ttk.Frame(ventana, padding=10)
frame_formulario.pack()

etiqueta_id = ttk.Label(frame_formulario, text="")
etiqueta_id.pack()

fila1 = ttk.Frame(frame_formulario)
fila1.pack(pady=5)
ttk.Label(fila1, text="Nombre:").pack(side="left", padx=5)
ttk.Entry(fila1, textvariable=entrada_nombre, width=20).pack(side="left", padx=5)

ttk.Label(fila1, text="Precio:").pack(side="left", padx=5)
ttk.Entry(fila1, textvariable=entrada_precio, width=10).pack(side="left", padx=5)

fila2 = ttk.Frame(frame_formulario)
fila2.pack(pady=5)
ttk.Button(fila2, text="Crear", command=crear_producto).pack(side="left", padx=5)
ttk.Button(fila2, text="Actualizar", command=actualizar_producto).pack(side="left", padx=5)
ttk.Button(fila2, text="Eliminar", command=eliminar_producto).pack(side="left", padx=5)
ttk.Button(fila2, text="Limpiar", command=limpiar_campos).pack(side="left", padx=5)

# Tabla
frame_tabla = ttk.Frame(ventana)
frame_tabla.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scroll_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Precio"), show="headings", yscrollcommand=scroll_y.set)
scroll_y.config(command=tabla.yview)

tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Precio", text="Precio")

tabla.column("ID", anchor="center")
tabla.column("Nombre", anchor="center")
tabla.column("Precio", anchor="center")

tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

actualizar_tabla()
ventana.mainloop()
