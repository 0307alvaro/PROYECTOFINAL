CREATE DATABASE  presupuesto_db;
USE presupuesto_db;

CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    tipo VARCHAR(50),
    descripcion VARCHAR(100),
    monto DECIMAL(10,2)
);