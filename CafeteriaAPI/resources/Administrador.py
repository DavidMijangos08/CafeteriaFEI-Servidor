"""
   Archivo: Administrador.py                                                  
   Programador: David Alexander                                                
   Fecha de creación: 05/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo con los recursos para hacer
   request y guardar datos en la BD                        
"""

from re import A
from tabnanny import check
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from utils import check_password, hash_password
from models.Administrador import Administrador, lista

class ListaAdministradores(Resource):
    def post(self):
        json_data = request.get_json()
        correoElectronico = json_data.get('correoElectronico')
        contraseniaNoHash = json_data.get('contrasenia')
        contraseniaHash = hash_password(contraseniaNoHash)
        cargo = json_data.get('cargo')
        
        administrador = Administrador(
            correoElectronico = correoElectronico,
            contrasenia = contraseniaHash,
            cargo = cargo
        )
        lista.append(administrador)
        administrador.save()

        data = {
            'correoElectronico': administrador.correoElectronico
        }
        return data, HTTPStatus.CREATED

class RecursoAdministrador(Resource):
    def post(self, correoElectronico):
        json_data = request.get_json()
        administrador = Administrador.obtener_por_correoElectronico(correoElectronico)
        contraseniaNoHash = json_data.get('contrasenia')
        if check_password(contraseniaNoHash, administrador.contrasenia) is False:
            return {'message': 'Datos incorrectos'}, HTTPStatus.NOT_FOUND
        data = {
            'correoElectronico': administrador.correoElectronico
        }
        return data, HTTPStatus.OK