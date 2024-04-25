"""
   Archivo: Administrador.py                                                  
   Programador: David Alexander                                                     
   Fecha de creación: 23/May/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo para realizar la tabla Administrador
   junto con sus metodos                          
"""

from sqlalchemy import null
from extensions import db

lista = []

class Administrador(db.Model):
    __tablename__ = 'Administrador'
    
    idAdminsitrador = db.Column(db.Integer, primary_key = True)
    correoElectronico = db.Column(db.String(100), nullable = False)
    contrasenia = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(30), nullable = False)

    @classmethod
    def obtener_por_credenciales(cls, correoElectronico, contrasenia):
        return cls.query.filter_by(correoElectronico = correoElectronico, contrasenia = contrasenia).first()
    
    @classmethod
    def obtener_por_correoElectronico(cls, correoElectronico):
        return cls.query.filter_by(correoElectronico = correoElectronico).first()

    def save(self):
        db.session.add(self)
        db.session.commit()