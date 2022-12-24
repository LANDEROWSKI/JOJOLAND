from flask import Flask, render_template, request, redirect, session
from helpers import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import sqlite3

db = sqlite3.connect('database.db', check_same_thread=False)

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'


Session(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        Email = request.form.get('Email')
        Password = request.form.get('Password')
        if not Email or not Password:
            mensaje = 'campos vacios'

            return render_template('error.html', MESSAGE=mensaje)

        consulta = db.execute('select * from usuarios where correo=?',
                              (Email,)).fetchall()

        if len(consulta) <= 0 or not check_password_hash(consulta[0][3], Password):
            mensaje = 'Correo y Contraseña Incorrecta!'
            return render_template('error.html', MESSAGE=mensaje)
        print(consulta)
        session['user_id'] = consulta[0][0]
        session['nombre'] = consulta[0][1]
        print(session['user_id'], session['nombre'])
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    session.clear()
    if request.method == "POST":
        Username = request.form.get('Username')
        Email = request.form.get('email')
        Password = request.form.get('password')
        Password2 = request.form.get('password2')
        if not Username or not Email or not Password or not Password2:
            mensaje = 'campos vacios'

            return render_template('error.html', MESSAGE=mensaje)

        if Password != Password2:
            mensaje = 'Contraseña no Coinciden Oni-chan'
            return render_template('error.html', MESSAGE=mensaje)

        hashtag = generate_password_hash(Password)

        consulta = db.execute('select * from usuarios where correo=?',
                              (Email,)).fetchall()
        if len(consulta) > 0:
            mensaje = 'Correo no disponible'
            return render_template('error.html', MESSAGE=mensaje)
        db.execute('insert into usuarios(user, correo, password) values(?,?,?)',
                   (Username, Email, hashtag))

        db.commit()

        consulta = db.execute('select * from usuarios where correo=?',
                              (Email,)).fetchone()
        print(consulta)

        session['user_id'] = consulta[0]
        session['nombre'] = consulta[1]
        print(session['user_id'], session['nombre'])

        return redirect('/')
    else:
        return render_template('registro.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')


@app.route('/comentarios', methods=['POST', 'GET'])
@login_required
def comentarios():
    if request.method == 'POST':
        joestar = request.form.get('rating')
        descripcion = request.form.get('descrip')
        db.execute("Insert into comentarios(user_id, stars, descripcion) values (?,?,?)",
                   (session['user_id'], joestar, descripcion))
        db.commit()
        return redirect('/comentarios')
    else:
        resenias = db.execute(
            """select usuarios.user, comentarios.stars, comentarios.descripcion from comentarios join usuarios on comentarios.user_id=usuarios.id """).fetchall()
        return render_template('comentarios.html', resenias=resenias)
