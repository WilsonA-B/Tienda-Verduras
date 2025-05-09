import tkinter as tk
from Helpers import *
from tkinter import ttk, messagebox

# -----------------------------------------------
# Conexion a la BD
import sqlite3

conn = sqlite3.connect("Tienda.db")
cursor = conn.cursor()

with open ("Estructura.sql", "r") as archivo_sql:
    cursor.executescript(archivo_sql.read())

conn.commit()
conn.close()

# -----------------------------------------------
# Funcion para pasar al Login
def Login():
    ventana.destroy()
    import Login

# -----------------------------------------------
# Crear ventana principal
ventana = tk.Tk()
ventana.title("Tienda de Verduras")
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
tk.Button(barra_superior, text=" 💻 ", bg="#0a497b", fg="white", font=("Bookman Old Style", 12), command=Login).pack(side="right", padx=10)

# -----------------------------------------------
# Cuerpo principal
cuerpo = tk.Frame(ventana, bg="#e8f5e9")
cuerpo.pack(fill="both", expand=True, padx=10, pady=10)
cuerpo.columnconfigure(1, weight=1)

# -----------------------------------------------
# Tabla productos
tabla_frame = tk.Frame(cuerpo, bg="#e8f5e9")
tabla_frame.grid(row=0, column=1, sticky="nsew")
cuerpo.grid_columnconfigure(1, weight=1)

label_tabla = tk.Label(tabla_frame, text="Canasta", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12, "bold"))
label_tabla.pack()

tabla = ttk.Treeview(tabla_frame, columns=("Producto", "Cantidad", "Precio", "Total"), show="headings", height=10)
for col in ("Producto", "Cantidad", "Precio", "Total"):
    tabla.heading(col, text=col)
    tabla.column(col, width=100,)
tabla.pack(fill="both", expand=True)

# -----------------------------------------------
# Total General
total_general_var = tk.StringVar(value="Total: $ 0")
label_total_general = tk.Label(tabla_frame, textvariable=total_general_var, font=("Arial", 12, "bold"), bg="#e8f5e9", anchor="e")
label_total_general.pack(fill="x", pady=(10, 0), padx=5)

# -----------------------------------------------
# Precios fijos por producto
precios_productos = {
    "Manzana": 1200, "Naranja": 800, "Brócoli": 1500, "Zanahoria": 700, "Papa": 500,
    "Tomate": 900, "Cebolla": 600, "Lechuga": 1000, "Pimiento": 1300, "Ajo": 400,
    "Pepino": 850, "Espinaca": 950, "Berenjena": 1100, "Repollo": 1200, "Calabacín": 1250,
    "Apio": 700, "Remolacha": 1000, "Rábano": 600, "Perejil": 500, "Chayote": 900,
    "Maíz": 750, "Yuca": 850, "Aguacate": 2000
}

productos = list(precios_productos.keys())

# -----------------------------------------------
# Funciones principales
# -----------------------------------------------

# -----------------------------------------------
# Helpers
actualizar_total_general(tabla, total_general_var)

# -----------------------------------------------
# Funcion para que muestre el precio cuando se escoja un producto
def actualizar_precio(event):
    producto = combo_productos.get()
    if producto in precios_productos:
        precio_var.set(precios_productos[producto])

# -----------------------------------------------
# Funcion para Agregar Producto a la Tabla
def agregar_producto():
    producto = combo_productos.get()
    cantidad = entrada_cantidad.get()
    if producto and cantidad:
        try:
            cantidad = int(cantidad)
            precio = precios_productos.get(producto, 0)
            total = precio * cantidad
            tabla.insert("", "end", values=(producto, cantidad, f"$ {precio}", f"$ {total}"))
            actualizar_total_general(tabla, total_general_var)
            precio_var.set(f"$ {precio}")
            cantidad = int(0)
        except ValueError:
            precio_var.set("Error")

# -----------------------------------------------
# Funcion para eliminar producto de la tabla
def eliminar_producto():
    selected = tabla.selection()
    if selected:
        tabla.delete(selected[0])
        actualizar_total_general()

# -----------------------------------------------
# Guarda el cliente y Bloquea los Labels
def guardar_cliente():
    nombre = nombre_cliente.get().strip()
    cedula = cedula_cliente.get().strip()

    if not nombre:
        messagebox.showwarning("Nombre requerido", "Necesita registrar el nombre del cliente.")
        return

    if not cedula.isdigit():
        messagebox.showerror("Error de Cédula", "La cédula debe contener solo números.")
        return

    entrada_nombre.config(state="readonly")
    entrada_cedula.config(state="readonly")

# -----------------------------------------------
# Desbloquea los Labels
def cancelar_cliente():
    entrada_nombre.config(state="normal")
    entrada_cedula.config(state="normal")
    entrada_nombre.delete(0, tk.END)
    entrada_cedula.delete(0, tk.END)

# -----------------------------------------------
# Generar Factura y Reiniciar el Visual
def finalizar_compra():
    # Validar que haya productos en la tabla
    if not tabla.get_children():
        messagebox.showwarning("Carrito vacío", "No hay productos en la canasta.")
        return

    # Validar que se haya ingresado nombre y cédula
    if not nombre_cliente.get().strip() or not cedula_cliente.get().strip():
        messagebox.showwarning("Datos incompletos", "Por favor ingresa nombre y cédula del cliente.")
        return

    # Crear ventana de factura
    factura = tk.Toplevel(ventana)
    factura.title("Factura de Compra")
    factura.configure(bg="white")
    centrar_ventana(factura, 500, 400)

    # Datos del cliente
    tk.Label(factura, text="Factura de Compra", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
    tk.Label(factura, text=f"Nombre: {nombre_cliente.get()}", font=("Arial", 10), bg="white").pack()
    tk.Label(factura, text=f"Cédula: {cedula_cliente.get()}", font=("Arial", 10), bg="white").pack(pady=(0, 10))

    # Factura
    tabla_factura = ttk.Treeview(factura, columns=("Producto", "Cantidad", "Precio", "Total"), show="headings", height=8)
    for col in ("Producto", "Cantidad", "Precio", "Total"):
        tabla_factura.heading(col, text=col)
        tabla_factura.column(col, width=100, anchor="center")
    tabla_factura.pack(pady=5, padx=10, fill="x")

    for row in tabla.get_children():
        valores = tabla.item(row, "values")
        tabla_factura.insert("", "end", values=valores)

    # Guardar el total antes de limpiar
    total_factura = total_general_var.get()
    tk.Label(factura, text=total_factura, font=("Arial", 12, "bold"), bg="white").pack(pady=10)

    # Limpiar la tabla de productos
    for item in tabla.get_children():
        tabla.delete(item)
        total_general_var.set(f"Total: $ {0}")

    # Limpiar los campos de cliente
    nombre_cliente.set("")
    cedula_cliente.set("")
    entrada_nombre.config(state="normal")
    entrada_cedula.config(state="normal")
    entrada_nombre.delete(0, tk.END)
    entrada_cedula.delete(0, tk.END) 

    # Limpiar campos de Productos
    combo_productos.set("Selecciona un producto")
    precio_var.set("")
    entrada_cantidad.delete(0, tk.END)

    # Botón cerrar
    tk.Button(factura, text="Cerrar", command=factura.destroy, bg="#c62828", fg="white").pack(pady=5)

# -----------------------------------------------
# Mover Ventana
def iniciar_movimiento(event):
    ventana.x = event.x
    ventana.y = event.y

def mover_ventana(event):
    x = event.x_root - ventana.x
    y = event.y_root - ventana.y
    ventana.geometry(f"+{x}+{y}")

barra_superior.bind("<ButtonPress-1>", iniciar_movimiento)
barra_superior.bind("<B1-Motion>", mover_ventana)

# -----------------------------------------------
# Columna izquierda: formulario
form_frame = tk.Frame(cuerpo, bg="#e8f5e9")
form_frame.grid(row=0, column=0, sticky="nw")

tk.Label(form_frame, text="Producto:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5)
combo_productos = ttk.Combobox(form_frame, values=productos, state="readonly", width=25)
combo_productos.grid(row=0, column=1, padx=10)
combo_productos.set("Selecciona un producto")
combo_productos.bind("<<ComboboxSelected>>", actualizar_precio)

precio_var = tk.StringVar()
tk.Label(form_frame, text="Precio:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
entrada_precio = tk.Entry(form_frame, textvariable=precio_var, width=28, state="readonly")
entrada_precio.grid(row=1, column=1)

tk.Label(form_frame, text="Cantidad:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=5)
entrada_cantidad = tk.Entry(form_frame, width=28)
entrada_cantidad.grid(row=2, column=1)

# Boton Agregar Producto
tk.Button(form_frame, text="Agregar producto", bg="#66bb6a", fg="white", font=("Arial", 12, "bold"), command=agregar_producto).grid(row=3, columnspan=2, pady=10)

# -----------------------------------------------
# Datos del Cliente
nombre_cliente = tk.StringVar()
cedula_cliente = tk.StringVar()

tk.Label(form_frame, text="--- Datos del Cliente ---", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 10, "bold")).grid(row=4, columnspan=2, pady=(20, 5))

entrada_nombre = tk.Entry(form_frame, textvariable=nombre_cliente, width=28)
entrada_nombre.grid(row=5, column=1)
tk.Label(form_frame, text="Nombre:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 10)).grid(row=5, column=0, sticky="e", pady=5)

entrada_cedula = tk.Entry(form_frame, textvariable=cedula_cliente, width=28)
entrada_cedula.grid(row=6, column=1)
tk.Label(form_frame, text="Cédula:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 10)).grid(row=6, column=0, sticky="e", pady=5)

botones_frame = tk.Frame(form_frame, bg="#e8f5e9")
botones_frame.grid(row=7, columnspan=2, pady=10)


# -----------------------------------------------
# Configuracion de Botones para Cliente
tk.Button(botones_frame, text="Guardar", bg="#43a047", fg="white", command=guardar_cliente).pack(side="left", padx=5)
tk.Button(botones_frame, text="Cancelar", bg="#ef5350", fg="white", command=cancelar_cliente).pack(side="left", padx=5)

# -----------------------------------------------
# Configuracion para los botones de Facturar o Borrar Producto
botones_tabla = tk.Frame(tabla_frame, bg="#e8f5e9")
botones_tabla.pack(pady=10)

btn_carrito = tk.Button(
    botones_tabla, text="🛒", bg="#43a047", fg="white",
    font=("Arial", 12, "bold"), width=8, height=4, command=finalizar_compra
)
btn_eliminar = tk.Button(
    botones_tabla, text="❌", bg="#c62828", fg="white",
    font=("Arial", 12, "bold"), width=8, height=4, command=eliminar_producto
)
btn_carrito.pack(side="left", padx=15)
btn_eliminar.pack(side="left", padx=15)

centrar_ventana(ventana, 1100, 450)

# -----------------------------------------------
ventana.mainloop()