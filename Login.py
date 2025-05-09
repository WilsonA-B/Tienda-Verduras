import tkinter as tk
from Helpers import *
from tkinter import messagebox

USERS = {
    "admin": "1234"
}

# -----------------------------------------------
# Parametro de Ingreso
def verificar_login(usuario, contrasena):
    return USERS.get(usuario) == contrasena

# -----------------------------------------------
# Mensaje de Confirmacion y Cambio de Ventana
def iniciar_sistema():
    messagebox.showinfo("Login exitoso", "Entrando a la Base de Datos")
    ventana.destroy()
    import Conexion

# -----------------------------------------------
# Verificacion del Login
def login():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()
    if verificar_login(usuario, contrasena):
        iniciar_sistema()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# -----------------------------------------------
# Volver a Pantalla Principal
def Back():
    ventana.destroy()
    import Proyecto

# -----------------------------------------------
# Diseño Ventana Login
ventana = tk.Tk()
ventana.title("Login - Tienda")
ventana.config(bg="#e8f5e9")

tk.Label(ventana, text="Usuario").pack(pady=5)
entrada_usuario = tk.Entry(ventana)
entrada_usuario.pack()

tk.Label(ventana, text="Contraseña").pack(pady=5)
entrada_contrasena = tk.Entry(ventana, show="*")
entrada_contrasena.pack()

# -----------------------------------------------
# Configuracion de Botones
boton_ventana = tk.Frame(ventana)
boton_ventana.pack(pady=20)

tk.Button(boton_ventana, text="Ingresar", bg="#43a047", fg="white", width=6, height=1, command=login).pack(side="left", padx=10)
tk.Button(boton_ventana, text="Volver", bg="#ef5350", fg="white", width=6, height=1, command=Back).pack(side="left", padx=10)

ventana.update_idletasks()
centrar_ventana(ventana, 300, 250)

ventana.mainloop()
