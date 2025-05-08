import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "Tienda.db"

def insertar_producto(nombre, precio):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()
    conn.close()
    mostrar_productos()

def eliminar_producto():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")
        return
    item = tabla.item(seleccionado)
    prod_id = item["values"][0]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto=?", (prod_id,))
    conn.commit()
    conn.close()
    mostrar_productos()

def actualizar_producto():
    seleccionado = tabla.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona un producto para actualizar.")
        return
    item = tabla.item(seleccionado)
    prod_id = item["values"][0]
    nuevo_nombre = entrada_nombre.get()
    nuevo_precio = entrada_precio.get()
    if not nuevo_nombre or not nuevo_precio:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=?, precio=? WHERE id_producto=?",
                   (nuevo_nombre, float(nuevo_precio), prod_id))
    conn.commit()
    conn.close()
    mostrar_productos()

def mostrar_productos():
    for fila in tabla.get_children():
        tabla.delete(fila)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    for fila in filas:
        tabla.insert("", tk.END, values=fila)
    conn.close()

def seleccionar_producto(event):
    seleccionado = tabla.selection()
    if seleccionado:
        item = tabla.item(seleccionado)
        valores = item["values"]
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[1])
        entrada_precio.delete(0, tk.END)
        entrada_precio.insert(0, valores[2])

# Interfaz
root = tk.Tk()
root.title("Gestor de Productos - Tienda.db")
root.geometry("500x400")

# Formulario
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nombre").grid(row=0, column=0)
entrada_nombre = tk.Entry(frame_form)
entrada_nombre.grid(row=0, column=1)

tk.Label(frame_form, text="Precio").grid(row=1, column=0)
entrada_precio = tk.Entry(frame_form)
entrada_precio.grid(row=1, column=1)

# Botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Agregar", command=lambda: insertar_producto(
    entrada_nombre.get(), float(entrada_precio.get())
)).grid(row=0, column=0, padx=5)

tk.Button(frame_botones, text="Actualizar", command=actualizar_producto).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Eliminar", command=eliminar_producto).grid(row=0, column=2, padx=5)

# Tabla
tabla = ttk.Treeview(root, columns=("ID", "Nombre", "Precio"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Precio", text="Precio")
tabla.bind("<<TreeviewSelect>>", seleccionar_producto)
tabla.pack(expand=True, fill="both")

mostrar_productos()
root.mainloop()
