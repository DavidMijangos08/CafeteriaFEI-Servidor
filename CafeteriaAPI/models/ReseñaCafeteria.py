"""
   Archivo: ReseñaCafeteria.py                                                  
   Programador: Maria Elena                                                  
   Fecha de creación: 02/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo para realizar la tabla ReseñaCafeteria
   junto con sus metodos                          
"""

from sqlalchemy import null
from extensions import db

lista_reseñas_cafeteria = []

class ReseñaCafeteria(db.Model):
    __tablename__ = 'ReseñaCafeteria'

    idReseña = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(80), nullable = False)
    opinion = db.Column(db.String(500), nullable = False)
    calificacion = db.Column(db.Integer, nullable = False)
    rutaImagen = db.Column(db.BLOB, nullable = True)
    idCafeteria = db.Column(db.Integer, nullable = False)

    @classmethod
    def obtener_por_idReseña(cls, idReseña):
        return cls.query.filter_by(idReseña = idReseña).first()
    
    @classmethod
    def obtener_todos_por_idCafeteria(cls, idCafeteria):
        return cls.query.filter_by(idCafeteria = idCafeteria).order_by(cls.idReseña.desc()).limit(10).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
    