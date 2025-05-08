import sqlite3
import tkinter as tk
from Helpers import *
from tkinter import messagebox, ttk

DB_NAME = "Tienda.db"

def insertar_clientes(cedula, nombre):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (cedula, nombre) VALUES (?, ?)", (cedula, nombre))
    conn.commit()
    conn.close()
    mostrar_clientes()

def eliminar_cliente():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un cliente para eliminar.")
        return
    item = tabla.item(seleccionado)
    cedula = item["values"][0]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE cedula=?", (cedula,))
    conn.commit()
    conn.close()
    mostrar_clientes()

def actualizar_clientes():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un cliente para actualizar.")
        return
    item = tabla.item(seleccionado)
    id_cedula = item["values"][0]
    nueva_cedula = entrada_cedula.get()
    nuevo_nombre = entrada_nombre.get()
    if not nuevo_nombre or not nueva_cedula:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET nombre=? WHERE cedula=?",
                   (nuevo_nombre, id_cedula,))
    conn.commit()
    conn.close()
    mostrar_clientes()

def mostrar_clientes():
    for fila in tabla.get_children():
        tabla.delete(fila)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    filas = cursor.fetchall()
    for fila in filas:
        tabla.insert("", tk.END, values=fila)
    conn.close()

def seleccionar_clientes(event):
    seleccionado = tabla.selection()
    if seleccionado:
        item = tabla.item(seleccionado)
        valores = item["values"]
        entrada_cedula.delete(0, tk.END)
        entrada_cedula.insert(0, valores[0])
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[1])

def Home():
    root.withdraw()
    import Proyecto

def iniciar_movimiento(event):
    root.x = event.x
    root.y = event.y

def mover_ventana(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

# Interfaz
root = tk.Tk()
root.title("Gestor de Productos - Tienda.db")
root.geometry("700x450")
root.configure(bg="#e8f5e9")
root.overrideredirect(True)
root.resizable(True, True) # ---- Barra de Windows

# -----------------------------------------------
# Barra superior
barra_superior = tk.Frame(root, bg="#2e7d32", height=30)
barra_superior.pack(fill="x")
tk.Label(barra_superior, text="🍅 Tienda de Verduras", bg="#2e7d32", fg="white", font=("Bookman Old Style", 12, "italic")).pack(side="left", padx=10)
tk.Button(barra_superior, text=" X ", bg="#c62828", fg="white", font=("Bookman Old Style", 12), command=root.destroy).pack(side="right", padx=10)
tk.Button(barra_superior, text=" 🏠 ", bg="#0a497b", fg="white", font=("Bookman Old Style", 12), command=Home).pack(side="right", padx=10)

barra_superior.bind("<ButtonPress-1>", iniciar_movimiento)
barra_superior.bind("<B1-Motion>", mover_ventana)

# Formulario
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Cedula").grid(row=0, column=0)
entrada_cedula = tk.Entry(frame_form)
entrada_cedula.grid(row=0, column=1)

tk.Label(frame_form, text="Nombre").grid(row=1, column=0)
entrada_nombre = tk.Entry(frame_form)
entrada_nombre.grid(row=1, column=1)

# Botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Agregar", command=lambda: insertar_clientes(
    entrada_cedula.get(), entrada_nombre.get() 
)).grid(row=0, column=0, padx=5)

tk.Button(frame_botones, text="Actualizar", command=actualizar_clientes).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Eliminar", command=eliminar_cliente).grid(row=0, column=2, padx=5)

# Tabla
tabla = ttk.Treeview(root, columns=("Cedula", "Nombre"), show="headings")
tabla.heading("Cedula", text="Cedula")
tabla.heading("Nombre", text="Nombre")
tabla.bind("<<TreeviewSelect>>", seleccionar_clientes)
tabla.pack(expand=True, fill="both")

mostrar_clientes()

root.update_idletasks()
centrar_ventana(root, 700, 450)

root.mainloop()
