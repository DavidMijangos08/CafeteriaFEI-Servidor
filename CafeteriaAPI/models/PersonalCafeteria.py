"""
   Archivo: PersonalCafeteria.py                                                  
   Programador: David Alexander                                                    
   Fecha de creación: 01/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo para realizar la tabla PersonalCafeteria
   junto con sus metodos                          
"""

from sqlalchemy import null
from extensions import db

lista_personal = []

class PersonalCafeteria(db.Model):
    __tablename__ = 'PersonalCafeteria'

    idPersonal = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    CURP = db.Column(db.String(18), nullable = False)
    correoElectronico = db.Column(db.String(100), nullable = False)
    cargo = db.Column(db.String(30), nullable = False)
    idCafeteria = db.Column(db.Integer, nullable = False)
    contrasenia = db.Column(db.String(50), nullable = False)
    token = db.Column(db.String(300), nullable = True)

    @classmethod
    def obtener_por_nombre(cls, nombre):
        return cls.query.filter_by(nombre = nombre).first()

    @classmethod
    def obtener_por_correoElectronico(cls, correoElectronico):
        return cls.query.filter_by(correoElectronico = correoElectronico).first()

    @classmethod
    def obtener_por_CURP(cls, CURP):
        return cls.query.filter_by(CURP = CURP).first()
        
    @classmethod
    def obtener_por_id(cls, idPersonal):
        return cls.query.filter_by(idPersonal = idPersonal).first()
    
    @classmethod
    def obtener_por_credenciales(cls, correoElectronico, contrasenia):
        return cls.query.filter_by(correoElectronico = correoElectronico, contrasenia = contrasenia).first()
    
    @classmethod
    def obtener_todos_los_personales(cls):
        return cls.query.all()
    
    @classmethod
    def obtener_todo_el_personal_por_cafeteriaAsociada(cls, idCafeteria):
        return cls.query.filter_by(idCafeteria=idCafeteria).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    