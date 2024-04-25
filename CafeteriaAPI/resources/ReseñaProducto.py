"""
   Archivo: ReseñaProducto.py                                                  
   Programador: Maria Elena                                             
   Fecha de creación: 05/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo con los recursos para hacer
   request y guardar datos en la BD                        
"""

from tabnanny import check
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.ReseñaProducto import ReseñaProducto, lista_reseñas_productos

class ListaReseñasProducto(Resource):
    def get(self, idProducto):
        data = []
        reseñasProducto = ReseñaProducto.obtener_todos_por_idProducto(idProducto)
        for reseñaProducto in reseñasProducto:
            data.append({
                'idReseña': reseñaProducto.idReseña,
                'titulo': reseñaProducto.titulo,
                'opinion': reseñaProducto.opinion,
                'calificacion': reseñaProducto.calificacion,
                'idProducto': reseñaProducto.idProducto,
                'rutaImagen': reseñaProducto.rutaImagen.decode("utf-8")
            })
        return data, HTTPStatus.OK

    def post(self, idProducto):
        json_data = request.get_json()
        titulo = json_data.get('titulo')
        opinion = json_data.get('opinion')
        calificacion = json_data.get('calificacion')
        idProducto = json_data.get('idProducto')
        rutaImagen = bytes (json_data.get('rutaImagen'), 'utf-8')

        reseñaProducto = ReseñaProducto(
            titulo = titulo,
            opinion = opinion,
            calificacion = calificacion,
            idProducto = idProducto,
            rutaImagen = rutaImagen
        )
        lista_reseñas_productos.append(reseñaProducto)
        reseñaProducto.save()
        
        data = {
            'idReseña': reseñaProducto.idReseña,
            'titulo': reseñaProducto.titulo,
            'opinion': reseñaProducto.opinion,
            'calificacion': reseñaProducto.calificacion,
            'idProducto': reseñaProducto.idProducto,
            'rutaImagen': reseñaProducto.rutaImagen.decode("utf-8")
        }
        return data, HTTPStatus.CREATED