from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Base de datos SQLite
def inicializar_bd():
    conexion = sqlite3.connect('credenciales.db')
    cursor = conexion.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, password TEXT)')
    cursor.execute('SELECT * FROM usuarios')
    if not cursor.fetchall():
        cursor.execute("INSERT INTO usuarios (nombre, password) VALUES ('Gabriel', 'Admin.2026')")
        cursor.execute("INSERT INTO usuarios (nombre, password) VALUES ('Michel', 'Cisco.123')")
        conexion.commit()
    conexion.close()

@app.route('/')
def inicio():
    return "Servidor Flask Operativo - API DRY7122 S.A\n"
@app.route('/login', methods=['GET'])
def verificar_cuenta():
    usuario = request.args.get('user')
    contrasena = request.args.get('pass')

    if not usuario or not contrasena:
        return "Faltan parámetros. Utilice el formato ?user=NOMBRE&pass=CLAVE\n", 400

    conexion = sqlite3.connect('credenciales.db')
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        return f"Acceso concedido. Credenciales verificadas para: {usuario}\n"
    else:
        return "Acceso denegado. Credenciales incorrectas.\n", 401

if __name__ == '__main__':
    inicializar_bd()
    app.run(host='0.0.0.0', port=5000)
