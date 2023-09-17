from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..model.usuario import Usuario  # Importa la clase Usuario
from configuracion import SECRET_KEY
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['contrasena']

        # Hashea la contraseña antes de almacenarla en la base de datos
        user = Usuario.iniciar_sesion(email, password)

        if user:
            # Guarda información del usuario en la sesión
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            return redirect(url_for('auth.welcome'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']
        dia = int(request.form['dia'])
        mes = int(request.form['mes'])
        anio = int(request.form['anio'])

        existing_user = Usuario.obtener_usuario_por_correo(email)

        if existing_user:
            flash('El correo electrónico ya está en uso.', 'error')
            return redirect(url_for('auth.register'))
        else:
            # Registra al nuevo usuario
            fecha_nacimiento_str = f"{anio}-{mes:02d}-{dia:02d}"
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")
            
            # Debes proporcionar los argumentos requeridos al método registrar_usuario
            if Usuario.registrar_usuario(username, name, lastname, email, password, fecha_nacimiento):
                flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Error en el registro. Inténtalo de nuevo.', 'error')
                return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth.route('/welcome')
def welcome():
    if 'user_id' in session:
        user_id = session['user_id']

        # Aquí debes obtener información sobre los servidores a los que pertenece el usuario.
        servidores = Usuario.obtener_servidores_del_usuario(user_id)

        if not servidores:
            # Si el usuario no pertenece a ningún servidor, establece una variable de contexto para indicarlo.
            # Esto ayudará a tu plantilla a determinar si mostrar solo las dos columnas o las tres columnas.
            no_pertenece_a_servidor = True
            flash("Aún no te has unido a un servidor")
            flash("Intenta buscar uno o crea uno propio.")
        else:
            no_pertenece_a_servidor = False
            
        return render_template('welcome.html', servidores=servidores, no_pertenece_a_servidor=no_pertenece_a_servidor)
    else:
        return "Debes iniciar sesión para ver esta página."
