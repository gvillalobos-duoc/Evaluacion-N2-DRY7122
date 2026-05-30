import secrets
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_FILE = "network_control.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """
    )
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            ("Prueba2", "SDN.2023"),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


@app.route("/api/v1/auth", methods=["POST"])
def login():
    token = f"dev_token_{secrets.token_hex(16)}"
    return jsonify({"token": token, "status": "authenticated"}), 200


@app.route("/api/v1/physical-network", methods=["GET"])
def get_physical_network():
    topology = {
        "controller": "DRY7122-SA-Main",
        "switches": [
            {"id": "SW-01", "type": "OpenFlow-v1.3", "status": "online"},
            {"id": "SW-02", "type": "OpenFlow-v1.3", "status": "online"},
        ],
        "links": [{"from": "SW-01", "to": "SW-02", "speed": "10Gbps"}],
    }
    return jsonify(topology), 200


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
        response = {"message": f"Usuario {username} creado exitosamente en SQLite"}
        code = 201
    except sqlite3.IntegrityError:
        response = {"error": "El usuario ya existe"}
        code = 400
    finally:
        conn.close()

    return jsonify(response), code


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)