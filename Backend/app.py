from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os

app = Flask(__name__)
# ¡IMPORTANTE! Cambia esto por una clave compleja y segura en un proyecto real
app.secret_key = 'mi_clave_secreta_super_segura_123' 

# Nombre del archivo JSON donde se guardarán los usuarios
USERS_FILE = 'users.json'

def load_users():
    """Carga los datos de los usuarios desde el archivo JSON."""
    if not os.path.exists(USERS_FILE) or os.stat(USERS_FILE).st_size == 0:
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Guarda los datos de los usuarios en el archivo JSON."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# --- Rutas de Autenticación (Login/Registro) ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # La solicitud viene de JavaScript (AJAX)
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        users = load_users()
        
        if username in users:
            # Devuelve una respuesta JSON al frontend
            return jsonify({'success': False, 'message': 'El usuario ya existe.'}), 400
        
        # En un proyecto real, DEBES hashear la contraseña (ej: con `werkzeug.security`)
        users[username] = {'password': password} 
        save_users(users)

        # Devuelve una respuesta JSON al frontend
        return jsonify({'success': True, 'message': 'Registro exitoso. Ya puedes iniciar sesión.'})

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        users = load_users()

        if username in users and users[username]['password'] == password:
            # Login exitoso
            # En un proyecto real, aquí establecerías una sesión (ej: con `flask-login`)
            return jsonify({'success': True, 'message': 'Inicio de sesión exitoso.'})
        else:
            return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos.'}), 401

    return render_template('login.html')

@app.route('/')
def home():
    # En un proyecto real, aquí verificarías si el usuario está logueado
    return render_template('home.html')

if __name__ == '__main__':
    # Crea el archivo users.json si no existe
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    app.run(debug=True)