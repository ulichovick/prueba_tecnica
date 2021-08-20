from .models import Empresa
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for
from . import bd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html',nombre=current_user.Nombre)

@main.route('/registrar_emp', methods=['GET','POST'])
def registrar_emp():
    if current_user.Nombre == "admin":
        if request.method == 'POST':
            nit = request.form.get('nit')
            nombre = request.form.get('nombre')
            tel = request.form.get('tel')
            dir = request.form.get('dir')
            email = request.form.get('email')

            nueva_empr = Empresa(Nit=nit, Nombre=nombre, eMail=email, Dir=dir, Tel=tel)
            bd.session.add(nueva_empr)
            bd.session.commit()
            bd.session.close()

            return redirect(url_for('main.index'))

        else:
            return render_template('reg_emp.html')
    else:
        return redirect(url_for('main.index'))