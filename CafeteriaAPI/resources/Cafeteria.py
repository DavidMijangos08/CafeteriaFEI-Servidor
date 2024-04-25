"""
   Archivo: Cafeteria.py                                                  
   Programador: David Alexander                                                
   Fecha de creación: 05/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo con los recursos para hacer
   request y guardar datos en la BD                        
"""

from tabnanny import check
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.Cafeteria import Cafeteria, lista_cafeterias

class ListaCafeterias(Resource):
    
    def get(self):
        data = []
        cafeterias = Cafeteria.obtener_todas_las_cafeterias()
        for cafeteria in cafeterias:
            if cafeteria.activo is True:
                data.append({
                    'idCafeteria': cafeteria.idCafeteria,
                    'nombreCafeteria': cafeteria.nombreCafeteria,
                    'facultadPerteneciente': cafeteria.facultadPerteneciente,
                    'direccion': cafeteria.direccion,
                    'horaInicio': cafeteria.horaInicio,
                    'horaFin': cafeteria.horaFin
                })
        return data, HTTPStatus.OK

    def post(self):
        json_data = request.get_json()
        nombreCafeteria = json_data.get('nombreCafeteria')
        facultadPerteneciente = json_data.get('facultadPerteneciente')
        direccion = json_data.get('direccion')
        horaInicio = json_data.get('horaInicio')
        horaFin = json_data.get('horaFin')
        activo = True
        if Cafeteria.obtener_por_nombre(nombreCafeteria):
            return {'message': 'El nombre de la cafetería ya está registrado'}, HTTPStatus.BAD_REQUEST

        cafeteria = Cafeteria(
            nombreCafeteria = nombreCafeteria,
            facultadPerteneciente = facultadPerteneciente,
            direccion = direccion,
            horaInicio = horaInicio,
            horaFin = horaFin,
            activo = activo
        )
        lista_cafeterias.append(cafeteria.nombreCafeteria)
        cafeteria.save()

        data = {
            'idCafeteria': cafeteria.idCafeteria,
            'nombreCafeteria': cafeteria.nombreCafeteria,
            'facultadPerteneciente': cafeteria.facultadPerteneciente,
            'direccion': cafeteria.direccion,
            'horaInicio': cafeteria.horaInicio,
            'horaFin': cafeteria.horaFin,
            'activo': cafeteria.activo
        }
        return data, HTTPStatus.CREATED

class ListaCafeteriasPorFacultad(Resource):
    def get(self, facultadPerteneciente):
        data = []
        cafeterias = Cafeteria.obtener_todas_las_cafeterias_por_facultad(facultadPerteneciente)
        for cafeteria in cafeterias:
            if cafeteria.activo is True:
                data.append({
                    'idCafeteria': cafeteria.idCafeteria,
                    'nombreCafeteria': cafeteria.nombreCafeteria,
                    'facultadPerteneciente': cafeteria.facultadPerteneciente,
                    'direccion': cafeteria.direccion,
                    'horaInicio': cafeteria.horaInicio,
                    'horaFin': cafeteria.horaFin
                })
        return data, HTTPStatus.OK

class RecursoCafeteria(Resource):
    def get(self, idCafeteria):
        cafeteria = Cafeteria.obtener_por_id(idCafeteria)
        if cafeteria is None:
            return {'message': 'Cafeteria no encontrada'}, HTTPStatus.NOT_FOUND
        data = {
            'idCafeteria': cafeteria.idCafeteria,
            'nombreCafeteria': cafeteria.nombreCafeteria,
            'facultadPerteneciente': cafeteria.facultadPerteneciente,
            'direccion': cafeteria.direccion,
            'horaInicio': cafeteria.horaInicio,
            'horaFin': cafeteria.horaFin,
            'activo': cafeteria.activo
        }
        return data, HTTPStatus.OK
    
    def patch(self, idCafeteria):
        cafeteria = Cafeteria.obtener_por_id(idCafeteria)
        if cafeteria is None:
            return {'message': 'Cafeteria no encontrada'}, HTTPStatus.NOT_FOUND
        if cafeteria.activo is True:
            cafeteria.activo = False
        else:
            cafeteria.activo = True
        data = {
            'idCafeteria': cafeteria.idCafeteria,
            'nombreCafeteria': cafeteria.nombreCafeteria,
            'facultadPerteneciente': cafeteria.facultadPerteneciente,
            'direccion': cafeteria.direccion,
            'horaInicio': cafeteria.horaInicio,
            'horaFin': cafeteria.horaFin,
            'activo': cafeteria.activo
        }
        cafeteria.save()
        return data, HTTPStatus.OK


