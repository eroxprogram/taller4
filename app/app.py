from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)


@app.route('/')
def index_():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register.html', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        edad = request.form["edad"]
        nac = request.form["nac"]
        email= request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT email FROM user WHERE email= %s ", (email,))
        result = cursor.fetchone()
        if result:
            flash("Este correo ya esta registrado")
            return render_template('register.html')
        
        cursor.execute("INSERT INTO user (nombre, apellidos, edad, nac, email, password) VALUES (%s, %s, %s, %s, %s, %s)", 
        (nombre, apellidos, edad, nac, email, password))
        mysql.connection.commit()
        flash("Tu cuenta se creo con exito")
    return render_template('register.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email= %s AND password= %s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['email'] = user['email']
            session['nombre'] = user['nombre']
            return render_template('dashboard.html')
        else:
            flash("Correo o Contraseñas Incorrectas")
    return render_template('login.html')
        
@app.route('/dashboard.html')
def dashboard():
    if 'email' in session:
        email = session['correo']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT nombre FROM user WHERE email=%s', (email,))
        user = cursor.fetchone()
        if user:
            nombre = user[0]
            return render_template('dashboard.html', email=email, nombre=nombre)
    return redirect(url_for('login'))

@app.route('/nosotros.html')
def nosotros():
    return render_template('nosotros.html')


@app.route('/doctores.html')
def doctores():
    return render_template('doctores.html')


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')
