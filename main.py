from .models import Empresa, Historia, Proyecto, Tickets, Usuario
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for
from . import bd

main = Blueprint('main', __name__)

@main.route('/', methods=['POST','GET'])
@login_required
def index():
    if request.method == 'POST':
        if 'abre_editar' in request.form:
            id = request.form.get("id")
            tickets = Tickets.query.filter(Tickets.Id == id)
            return redirect(url_for('main.index'))
        elif 'cancelar_ticket' in request.form:
            tick_id = int(request.form.get("tick_id"))
            ticket = bd.session.query(Tickets).filter(Tickets.Id == tick_id).one()
            ticket.Estado = "Cancelado"
            bd.session.commit()
            return redirect(url_for('main.index'))
        elif 'editar_ticket' in request.form:
            tick_id = int(request.form.get("tick_id"))
            descr = request.form.get('nueva_descripcion')
            estado = request.form.get('nuevo_estado')
            id_historia = request.form.get('nueva_historia')
            ticket = bd.session.query(Tickets).filter(Tickets.Id == tick_id).one()
            ticket.Estado = estado
            ticket.Descr = descr
            ticket.Id_Historia = id_historia
            bd.session.commit()
            return redirect(url_for('main.index'))

        elif 'crear_tick' in request.form:
            descr = request.form.get('descripcion')
            estado = request.form.get('estado')
            id_historia = request.form.get('historia')
            nuevo_ticket = Tickets(Descr=descr,Estado=estado,Id_Historia=id_historia)
            bd.session.add(nuevo_ticket)
            bd.session.commit()
            bd.session.close()
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.index'))
    else:
        tickets = bd.session.query(Tickets).join(Historia, Tickets.Id_Historia == Historia.Id).join(Usuario, Historia.Id_Usuario==current_user.Cc)
        historias = Historia.query.filter(Historia.Id_Usuario == current_user.Cc)
        return render_template('index.html', historias=historias,tickets=tickets)

@main.route('/historias', methods=['POST','GET'])
@login_required
def historias():
    if request.method == 'POST':
        descr = request.form.get('descr')
        proyecto = request.form.get('proyecto')
        id_usu = current_user.Cc
        nueva_historia = Historia(Descr=descr, Id_Proyecto=proyecto, Id_Usuario = id_usu)
        bd.session.add(nueva_historia)
        bd.session.commit()

        descr = request.form.get('descripcion_ticket')
        estado = request.form.get('estado_ticket')
        id_historia = nueva_historia.Id
        nuevo_ticket = Tickets(Descr=descr,Estado=estado,Id_Historia=id_historia)
        bd.session.add(nuevo_ticket)
        bd.session.commit()
        bd.session.close()
        return redirect(url_for('main.historias'))
    else:
        proyectos = Proyecto.query.filter(Proyecto.Nit_empresa == current_user.Nit_empresa)
        historias = Historia.query.filter(Historia.Id_Usuario == current_user.Cc)
        tickets = Tickets.query.all()
        return render_template('historias.html', proyectos=proyectos, historias=historias, tickets=tickets)


@main.route('/proyectos')
@login_required
def proyectos():
    proyectos = Proyecto.query.filter(Proyecto.Nit_empresa == current_user.Nit_empresa)
    empresas = Empresa.query.filter(Empresa.Nit == current_user.Nit_empresa)
    historias = Historia.query.all()
    return render_template('proyectos.html',proyectos=proyectos, empresas=empresas,historias=historias)
    

@main.route('/registrar_emp', methods=['GET','POST'])
def registrar_emp():
    if current_user.is_authenticated and current_user.Nombre == "Admin":
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

@main.route('/crear_proyecto', methods=['GET','POST'])
def crear_proyecto():
    if current_user.is_authenticated and current_user.Nombre == "Admin":
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            nit_empresa = request.form.get('nit_empresa')

            nuevo_proyecto = Proyecto(Nit_empresa=nit_empresa, Nombre=nombre)
            bd.session.add(nuevo_proyecto)
            bd.session.commit()
            bd.session.close()

            return redirect(url_for('main.index'))

        else:
            Empresas = Empresa.query.all()
            return render_template('crea_proys.html', Empresas=Empresas)
    else:
        return redirect(url_for('main.index'))