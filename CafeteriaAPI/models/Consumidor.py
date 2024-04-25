"""
   Archivo: Consumidor.py                                                  
   Programador: Eder Ivan                                                    
   Fecha de creación: 01/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo para realizar la tabla Consumidor
   junto con sus metodos                          
"""

from lib2to3.pgen2 import token
from sqlalchemy import null
from extensions import db

lista_consumidor = []

class Consumidor(db.Model):
    __tablename__ = 'Consumidor'

    idConsumidor = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    correoElectronico = db.Column(db.String(100), nullable = False)
    contrasenia = db.Column(db.String(50), nullable = False)
    token = db.Column(db.String(300), nullable = True)

    @classmethod
    def obtener_por_nombre(cls, nombre):
        return cls.query.filter_by(nombre = nombre).first()

    @classmethod
    def obtener_por_correoElectronico(cls, correoElectronico):
        return cls.query.filter_by(correoElectronico = correoElectronico).first()
        
    @classmethod
    def obtener_por_id(cls, idConsumidor):
        return cls.query.filter_by(idConsumidor = idConsumidor).first()
        
    @classmethod
    def obtener_por_credenciales(cls, correoElectronico, contrasenia):
        return cls.query.filter_by(correoElectronico = correoElectronico, contrasenia = contrasenia).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    