"""
   Archivo: PersonalCafeteria.py                                                  
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
from sqlalchemy import null
import jwt

from utils import check_password, hash_password
from models.PersonalCafeteria import PersonalCafeteria, lista_personal

key = 'super-secret'

class ListaPersonalCafeteria(Resource):
    def get(self, idCafeteria):
        data = []
        personalCafeteria = PersonalCafeteria.obtener_todo_el_personal_por_cafeteriaAsociada(idCafeteria)
        for personal in personalCafeteria:
            data.append({
                'idPersonal': personal.idPersonal,
                'nombre': personal.nombre,
                'CURP': personal.CURP,
                'correoElectronico': personal.correoElectronico,
                'cargo': personal.cargo,
                'idCafeteria': personal.idCafeteria           
            })
        return data, HTTPStatus.OK
    
    def post(self, idCafeteria):
        json_data = request.get_json()
        nombre = json_data.get('nombre')
        CURP = json_data.get('CURP')
        correoElectronico = json_data.get('correoElectronico')
        cargo = json_data.get('cargo')
        idCafeteria = json_data.get('idCafeteria')
        contraseniaNoHash = json_data.get('contrasenia')

        if PersonalCafeteria.obtener_por_CURP(CURP):
            return {'message': 'La CURP del persona ya está registrado'}, HTTPStatus.BAD_REQUEST
        if PersonalCafeteria.obtener_por_correoElectronico(correoElectronico):
            return {'message': 'El correo electronico ya está registrado'}, HTTPStatus.BAD_REQUEST
        if PersonalCafeteria.obtener_por_nombre(nombre):
            return {'message': 'El nombre del personal ya está registrado'}, HTTPStatus.BAD_REQUEST

        contraseniaHash = hash_password(contraseniaNoHash)

        personalCafeteria = PersonalCafeteria(
            nombre = nombre,
            CURP = CURP,
            correoElectronico = correoElectronico,
            cargo = cargo,
            idCafeteria = idCafeteria,
            contrasenia = contraseniaHash
        )
        lista_personal.append(personalCafeteria)
        personalCafeteria.save()
        
        data = {
            'idPersonal': personalCafeteria.idPersonal,
            'nombre': personalCafeteria.nombre,
            'CURP': personalCafeteria.CURP,
            'correoElectronico': personalCafeteria.correoElectronico,
            'cargo': personalCafeteria.cargo,
            'idCafeteria': personalCafeteria.idCafeteria
        }
        return data, HTTPStatus.CREATED

class RecursoLoginPersonal(Resource):
    def post(self, correoElectronico):
        json_data = request.get_json()
        personal = PersonalCafeteria.obtener_por_correoElectronico(correoElectronico)
        contraseniaNoHash = json_data.get('contrasenia')
        if check_password(contraseniaNoHash, personal.contrasenia) is False:
            return {'message': 'Datos incorrectos'}, HTTPStatus.NOT_FOUND
        
        payload = self.crear_payload(correoElectronico)
        token = jwt.encode(payload, key, algorithm="HS256")
        self.guardar_token(token, correoElectronico)
        
        data = {
            'idPersonal': personal.idPersonal,
            'nombre': personal.nombre,
            'CURP': personal.CURP,
            'correoElectronico': personal.correoElectronico,
            'cargo': personal.cargo,
            'idCafeteria': personal.idCafeteria,
            'token': personal.token
        }            
        return data, HTTPStatus.OK

    def put(self, correoElectronico):
        consumidor = PersonalCafeteria.obtener_por_correoElectronico(correoElectronico)
        if consumidor is None:
            return {'message': 'Cuenta de usuario no encontrado'}, HTTPStatus.NOT_FOUND
        consumidor.token = null
        consumidor.save()
        return HTTPStatus.NO_CONTENT

    def crear_payload(self, correoElectronico):
        personal = PersonalCafeteria.obtener_por_correoElectronico(correoElectronico)
        payload = {
            'idPersonal': personal.idPersonal,
            'nombre': personal.nombre,
            'correoElectronico': personal.correoElectronico
        }
        return payload

    def guardar_token(self, token, correoElectronico):
        personal = PersonalCafeteria.obtener_por_correoElectronico(correoElectronico)
        tokenDecodificado = token.decode('utf-8')
        personal.token = tokenDecodificado
        personal.save()

class RecursoPersonal(Resource):
    def get(self, idPersonal):
        personal = PersonalCafeteria.obtener_por_id(idPersonal)
        if personal is None:
            return {'message': 'Personal de cafeteria no encontrado'}, HTTPStatus.NOT_FOUND
        data = {
            'idPersonal': personal.idPersonal,
            'nombre': personal.nombre,
            'CURP': personal.CURP,
            'correoElectronico': personal.correoElectronico,
            'cargo': personal.cargo,
            'idCafeteria': personal.idCafeteria,
            'token': personal.token
        }            
        return data, HTTPStatus.OK

    def put(self, idPersonal):
        json_data = request.get_json()
        personal = PersonalCafeteria.obtener_por_id(idPersonal)
        if personal is None:
            return {'message': 'Personal de cafeteria no encontrado'}, HTTPStatus.NOT_FOUND
        nombre = json_data.get('nombre')
        CURP = json_data.get('CURP')
        correoElectronico = json_data.get('correoElectronico')
        cargo = json_data.get('cargo')
        idCafeteria = json_data.get('idCafeteria')
        contraseniaNoHash = json_data.get('contrasenia')
        token = bytes(json_data.get('token'), 'utf-8')

        decodeServer = jwt.decode(personal.token, key, algorithm="HS256")
        decodeCliente = jwt.decode(token, key, algorithm="HS256")

        if decodeServer != decodeCliente:
            return {'message': 'Error en el token'}, HTTPStatus.UNAUTHORIZED
        if PersonalCafeteria.obtener_por_CURP(CURP):
            if PersonalCafeteria.obtener_por_CURP(CURP).idPersonal != idPersonal:
                return {'message': 'La CURP del persona ya está registrado'}, HTTPStatus.BAD_REQUEST
        if PersonalCafeteria.obtener_por_correoElectronico(correoElectronico):
            if PersonalCafeteria.obtener_por_correoElectronico(correoElectronico).idPersonal != idPersonal:
                return {'message': 'El correo electronico ya está registrado'}, HTTPStatus.BAD_REQUEST
        if PersonalCafeteria.obtener_por_nombre(nombre):
            if PersonalCafeteria.obtener_por_nombre(nombre).idPersonal != idPersonal:
                return {'message': 'El nombre del personal ya está registrado'}, HTTPStatus.BAD_REQUEST

        contraseniaHash = hash_password(contraseniaNoHash)
        personal.nombre = nombre
        personal.CURP = CURP
        personal.correoElectronico = correoElectronico
        personal.cargo = cargo
        personal.idCafeteria = idCafeteria
        personal.contrasenia = contraseniaHash
        personal.token = token.decode('utf-8')

        personal.save()
        data = {
            'idPersonal': personal.idPersonal,
            'nombre': personal.nombre,
            'CURP': personal.CURP,
            'correoElectronico': personal.correoElectronico,
            'cargo': personal.cargo,
            'idCafeteria': personal.idCafeteria,
            'token': personal.token
        }
        return data, HTTPStatus.OK

    def delete(self, idPersonal):
        personal = PersonalCafeteria.obtener_por_id(idPersonal)
        if personal is None:
            return {'message': 'Personal de cafeteria no encontrado'}, HTTPStatus.NOT_FOUND
        personal.delete()
        return HTTPStatus.NO_CONTENT

