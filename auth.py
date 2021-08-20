from .models import Usuario, Empresa
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user, current_user
from . import bd

auth = Blueprint('auth', __name__)


@auth.route('/entrar', methods=['GET','POST'])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        pwwd = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = Usuario.query.filter_by(eMail=email).first()

        if not user or not check_password_hash(user.Contrasena, pwwd):
            flash('Por favor verifique las credenciales de acceso e intente ingresar de nuevo')
            return redirect(url_for('auth.entrar'))
        login_user(user, remember=remember)
        return redirect(url_for('main.perfil'))
    else:
        return render_template('entrar.html')


@auth.route('/registrarse', methods=['GET','POST'])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        cc = request.form.get('cc')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        pwwd = request.form.get('password')
        empresa = request.form.get('empresa')

        mail = Usuario.query.filter_by(eMail=email).first()
        nom = Usuario.query.filter_by(Nombre=nombre).first()
        id = Usuario.query.filter_by(Cc=cc).first()

        if id:
            flash('La cedula ya está registrada')
            return redirect(url_for('auth.registrarse'))
        elif nom:
            flash('El nombre de usuario ya está registrado')
            return redirect(url_for('auth.registrarse'))
        elif mail:
            flash('La dirección de correo ya está registrada')
            return redirect(url_for('auth.registrarse'))

        nuevo_usu = Usuario(Cc=cc, Nombre=nombre, eMail=email, Nit_empresa=empresa, Contrasena=generate_password_hash(pwwd, method='sha256'))
        bd.session.add(nuevo_usu)
        bd.session.commit()

        return redirect(url_for('auth.entrar'))

    else:
        Empresas = Empresa.query.all()
        return render_template('registrarse.html', Empresas=Empresas)

@auth.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect(url_for('main.index'))