"""
   Archivo: Producto.py                                                  
   Programador: Eder Ivan                                                  
   Fecha de creación: 01/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo para realizar la tabla Producto
   junto con sus metodos                          
"""

from enum import unique
from sqlalchemy import null
from extensions import db

lista_productos = []

class Producto(db.Model):
    __tablename__ = 'Producto'

    idProducto = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    descripcion = db.Column(db.String(250), nullable = False)
    precio = db.Column(db.Integer, nullable = False)
    tiempoAproximado = db.Column(db.Integer, nullable = False)
    rutaImagen = db.Column(db.BLOB, nullable = False)
    idCafeteria = db.Column(db.Integer, nullable = False)

    @classmethod
    def obtener_todos_por_idCafeteria(cls, idCafeteria):
        return cls.query.filter_by(idCafeteria = idCafeteria).all()

    @classmethod
    def obtener_por_nombre_e_idCafeteria(cls, idCafeteria, nombre):
        return cls.query.filter_by(idCafeteria = idCafeteria, nombre = nombre).first()

    @classmethod
    def obtener_por_id(cls, idProducto):
        return cls.query.filter_by(idProducto = idProducto).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()