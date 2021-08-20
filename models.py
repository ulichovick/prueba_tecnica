from flask_login import UserMixin
from . import bd

class Empresa(UserMixin, bd.Model):
    __tablename__ = 'Empresas'
    Nit = bd.Column(bd.Integer, primary_key=True)
    Nombre = bd.Column(bd.String(50), unique=True)
    Tel = bd.Column(bd.Integer)
    Dir = bd.Column(bd.String(50))
    eMail = bd.Column(bd.String(50), unique=True)
    Usuarios = bd.relationship('Usuario')

class Usuario(UserMixin, bd.Model):
    __tablename__ = 'Usuarios'
    Cc = bd.Column(bd.Integer, primary_key=True)
    Nombre = bd.Column(bd.String(50), unique=True)
    eMail = bd.Column(bd.String(50), unique=True)
    Nit_empresa = bd.Column(bd.Integer, bd.ForeignKey('Empresas.Nit'), nullable=False)
    Contrasena = bd.Column(bd.String(100))
    def get_id(self):
        return (self.Cc)

class Proyecto(UserMixin, bd.Model):
    __tablename__ = 'Proyectos'
    Id = bd.Column(bd.Integer, primary_key=True)
    Nombre = bd.Column(bd.String(50))
    Nit_empresa = bd.Column(bd.Integer, bd.ForeignKey('Empresas.Nit'), nullable=False)

class Historia(UserMixin, bd.Model):
    __tablename__ = 'Historias'
    Id = bd.Column(bd.Integer, primary_key=True)
    Descr = bd.Column(bd.String(50))
    Id_Proyecto = bd.Column(bd.Integer, bd.ForeignKey('Proyectos.Id'), nullable=False)
    Id_Usuario = bd.Column(bd.Integer,bd.ForeignKey('Usuarios.Cc'), nullable=False)


class Tickets(UserMixin, bd.Model):
    __tablename__ = 'Tickets'
    Id = bd.Column(bd.Integer, primary_key=True)
    Descr = bd.Column(bd.String(50))
    Id_Historia = bd.Column(bd.Integer, bd.ForeignKey('Historias.Id'), nullable=False)