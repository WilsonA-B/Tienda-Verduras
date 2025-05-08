CREATE TABLE IF NOT EXISTS clientes (
    cedula INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS facturas (
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    fecha TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(cedula)
);

CREATE TABLE IF NOT EXISTS detalle_factura (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_factura INTEGER,
    id_producto INTEGER,
    cantidad INTEGER,
    precio_unitario REAL,
    total REAL,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
)