"""
   Archivo: ReseñaCafeteria.py                                                  
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

from models.ReseñaCafeteria import ReseñaCafeteria, lista_reseñas_cafeteria

class ListaReseñasCafeteria(Resource):
    def get(self, idCafeteria):
        data = []
        reseñasCafeteria = ReseñaCafeteria.obtener_todos_por_idCafeteria(idCafeteria)
        for reseñaCafeteria in reseñasCafeteria:
            data.append({
                'idReseña': reseñaCafeteria.idReseña,
                'titulo': reseñaCafeteria.titulo,
                'opinion': reseñaCafeteria.opinion,
                'calificacion': reseñaCafeteria.calificacion,
                'idCafeteria': reseñaCafeteria.idCafeteria,
                'rutaImagen': reseñaCafeteria.rutaImagen.decode("utf-8")
            })
        return data, HTTPStatus.OK

    def post(self, idCafeteria):
        json_data = request.get_json()
        titulo = json_data.get('titulo')
        opinion = json_data.get('opinion')
        calificacion = json_data.get('calificacion')
        idCafeteria = json_data.get('idCafeteria')
        rutaImagen = bytes (json_data.get('rutaImagen'), 'utf-8')

        reseñaCafeteria = ReseñaCafeteria(
            titulo = titulo,
            opinion = opinion,
            calificacion = calificacion,
            idCafeteria = idCafeteria,
            rutaImagen = rutaImagen
        )
        lista_reseñas_cafeteria.append(reseñaCafeteria)
        reseñaCafeteria.save()
        
        data = {
            'idReseña': reseñaCafeteria.idReseña,
            'titulo': reseñaCafeteria.titulo,
            'opinion': reseñaCafeteria.opinion,
            'calificacion': reseñaCafeteria.calificacion,
            'idCafeteria': reseñaCafeteria.idCafeteria,
            'rutaImagen': reseñaCafeteria.rutaImagen.decode("utf-8")
        }
        return data, HTTPStatus.CREATED