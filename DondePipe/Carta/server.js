const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());

// Conexión a SQLite
const db = new sqlite3.Database(':memory:');
db.serialize(() => {
    // Crear tablas
    db.run("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, username TEXT, password TEXT)");
    db.run("CREATE TABLE productos (id INTEGER PRIMARY KEY, name TEXT, price REAL)");
    db.run("CREATE TABLE pedidos (id INTEGER PRIMARY KEY, details TEXT)");
});

// Rutas
app.post('/api/admin/crearUsuario', (req, res) => {
    const { username, password } = req.body;
    db.run("INSERT INTO usuarios (username, password) VALUES (?, ?)", [username, password], function(err) {
        if (err) {
            res.status(500).json({ message: 'Error al crear usuario' });
        } else {
            res.json({ message: 'Usuario creado con éxito', userId: this.lastID });
        }
    });
});

app.post('/api/admin/gestionarProductos', (req, res) => {
    const { productName, price } = req.body;
    db.run("INSERT INTO productos (name, price) VALUES (?, ?)", [productName, price], function(err) {
        if (err) {
            res.status(500).json({ message: 'Error al gestionar producto' });
        } else {
            res.json({ message: 'Producto gestionado con éxito', productId: this.lastID });
        }
    });
});

app.post('/api/cajero/aceptarPagos', (req, res) => {
    const { paymentAmount } = req.body;
    res.json({ message: `Pago de $${paymentAmount} aceptado` });
});

app.post('/api/trabajador/verMenu', (req, res) => {
    db.all("SELECT * FROM productos", (err, rows) => {
        if (err) {
            res.status(500).json({ message: 'Error al obtener el menú' });
        } else {
            res.json({ menu: rows });
        }
    });
});

app.post('/api/cliente/realizarPedidos', (req, res) => {
    const { orderDetails } = req.body;
    db.run("INSERT INTO pedidos (details) VALUES (?)", [orderDetails], function(err) {
        if (err) {
            res.status(500).json({ message: 'Error al realizar pedido' });
        } else {
            res.json({ message: 'Pedido realizado con éxito', orderId: this.lastID });
        }
    });
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
