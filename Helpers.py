# -----------------------------------------------
# Funcion para centrar las ventanas
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# -----------------------------------------------
# Calcular el total de la factura
def actualizar_total_general(tabla, total_general_var):
    total = 0
    for row in tabla.get_children():
        valores = tabla.item(row, "values")
        total_str = valores[3].replace("$", "").replace(",", "")
        total += float(total_str)
    total_general_var.set(f"Total: $ {total:,.0f}")
