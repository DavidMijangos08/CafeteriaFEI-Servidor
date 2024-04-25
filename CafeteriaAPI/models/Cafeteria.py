"""
   Archivo: Cafeteria.py                                                  
   Programador: David Alexander                                                     
   Fecha de creación: 23/May/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo para realizar la tabla Cafeteria
   junto con sus metodos                          
"""

from sqlalchemy import null
from extensions import db

lista_cafeterias = [] 

class Cafeteria(db.Model):
    __tablename__ = 'Cafeteria'

    idCafeteria = db.Column(db.Integer, primary_key = True)
    nombreCafeteria = db.Column(db.String(80), nullable = False)
    facultadPerteneciente = db.Column(db.String(100), nullable = False)
    direccion = db.Column(db.String(250), nullable = False)
    horaInicio = db.Column(db.String(10), nullable = False)
    horaFin = db.Column(db.String(10), nullable = False)
    activo = db.Column(db.Boolean(), default = True)
    
    @classmethod
    def obtener_por_nombre(cls, nombreCafeteria):
        return cls.query.filter_by(nombreCafeteria = nombreCafeteria).first()
    
    @classmethod
    def obtener_por_id(cls, idCafeteria):
        return cls.query.filter_by(idCafeteria = idCafeteria).first()
    
    @classmethod
    def obtener_todas_las_cafeterias(cls):
        return cls.query.all()

    @classmethod
    def obtener_todas_las_cafeterias_por_facultad(cls, facultadPerteneciente):
        return cls.query.filter_by(facultadPerteneciente = facultadPerteneciente).all()
    
    def save(self):
        db.session.add(self)
        db.session.commit()