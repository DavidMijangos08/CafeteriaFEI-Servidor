"""
   Archivo: Consumidor.py                                                  
   Programador: Eder Ivan                                              
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
import smtplib, ssl
import jwt

from utils import check_password, hash_password
from models.Consumidor import Consumidor, lista_consumidor

key = 'super-secret'

class Consumidores(Resource):
    def post(self):
        json_data = request.get_json()
        nombre = json_data.get('nombre')
        correoElectronico = json_data.get('correoElectronico')
        contraseniaNoHash = json_data.get('contrasenia')

        if Consumidor.obtener_por_nombre(nombre):
            return {'message': 'El nombre ya está registrado'}, HTTPStatus.BAD_REQUEST
        if Consumidor.obtener_por_correoElectronico(correoElectronico):
            return {'message': 'El correo electronico ya está registrado'}, HTTPStatus.BAD_REQUEST
        
        contraseniaHash = hash_password(contraseniaNoHash)
        consumidor = Consumidor(
            nombre = nombre,
            correoElectronico = correoElectronico,
            contrasenia = contraseniaHash
        )
        lista_consumidor.append(consumidor)
        consumidor.save()

        data = {
            'idConsumidor': consumidor.idConsumidor,
            'nombre': consumidor.nombre,
            'correoElectronico': consumidor.correoElectronico,
        }
        return data, HTTPStatus.CREATED
    
class Correo(Resource):
    def post(self):
        json_data = request.get_json()
        correoElectronico = json_data.get('correoElectronico')
        codigo = json_data.get('codigo')

        puerto = 587
        smtp_server = "smtp.gmail.com"
        email_emisor = "cafeteriaFEI@gmail.com"
        email_receptor = correoElectronico
        contrasenia = "zubvvumihqqhfwiw"
        subject = 'Codigo para verificacion de correo'
        body = 'Tu codigo es:'+ codigo
        mensaje = f'Subject: {subject}\n\n{body}'

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, puerto) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(email_emisor, contrasenia)
            server.sendmail(email_emisor, email_receptor, mensaje)
            server.quit()
        return HTTPStatus.OK

class RecursoLoginConsumidor(Resource):
    def post(self, correoElectronico):
        json_data = request.get_json()
        consumidor = Consumidor.obtener_por_correoElectronico(correoElectronico)
        contraseniaNoHash = json_data.get('contrasenia')
        if check_password(contraseniaNoHash, consumidor.contrasenia) is False:
            return {'message': 'Datos incorrectos'}, HTTPStatus.NOT_FOUND

        payload = self.crear_payload(correoElectronico)
        token = jwt.encode(payload, key, algorithm="HS256")
        self.guardar_token(token, correoElectronico)

        data = {
            'idConsumidor': consumidor.idConsumidor,
            'nombre': consumidor.nombre,
            'correoElectronico': consumidor.correoElectronico,
            'contrasenia': consumidor.contrasenia,
            'token': consumidor.token
        }            
        return data, HTTPStatus.OK
    
    def put(self, correoElectronico):
        consumidor = Consumidor.obtener_por_correoElectronico(correoElectronico)
        if consumidor is None:
            return {'message': 'Cuenta de usuario no encontrado'}, HTTPStatus.NOT_FOUND
        consumidor.token = null
        consumidor.save()
        return HTTPStatus.NO_CONTENT
    
    def crear_payload(self, correoElectronico):
        consumidor = Consumidor.obtener_por_correoElectronico(correoElectronico)
        payload = {
            'idConsumidor': consumidor.idConsumidor,
            'nombre': consumidor.nombre,
            'correoElectronico': consumidor.correoElectronico
        }
        return payload
    
    def guardar_token(self, token, correoElectronico):
        consumidor = Consumidor.obtener_por_correoElectronico(correoElectronico)
        tokenDecodificado = token.decode('utf-8')
        consumidor.token = tokenDecodificado
        consumidor.save()

class RecursoConsumidor(Resource):
    def get(self, idConsumidor):
        consumidor = Consumidor.obtener_por_id(idConsumidor)
        if consumidor is None:
            return {'message': 'Cuenta de usuario no encontrada'}, HTTPStatus.NOT_FOUND
        data = {
            'idConsumidor': consumidor.idConsumidor,
            'nombre': consumidor.nombre,
            'correoElectronico': consumidor.correoElectronico,
            'contrasenia': consumidor.contrasenia,
            'token': consumidor.token
        }            
        return data, HTTPStatus.OK

    def put(self, idConsumidor):
        json_data = request.get_json()
        consumidor = Consumidor.obtener_por_id(idConsumidor)
        if consumidor is None:
            return {'message': 'Cuenta de usuario no encontrada'}, HTTPStatus.NOT_FOUND
        nombre = json_data.get('nombre')
        correoElectronico = json_data.get('correoElectronico')
        contraseniaNoHash = json_data.get('contrasenia')
        token = bytes(json_data.get('token'), 'utf-8')

        decodeServer = jwt.decode(consumidor.token, key, algorithm="HS256")
        decodeCliente = jwt.decode(token, key, algorithm="HS256")

        if decodeServer != decodeCliente:
            return {'message': 'Error en el token'}, HTTPStatus.UNAUTHORIZED
        if Consumidor.obtener_por_nombre(nombre):
            if Consumidor.obtener_por_nombre(nombre).idConsumidor != idConsumidor:
                return {'message': 'El nombre ya está registrado'}, HTTPStatus.BAD_REQUEST
        if Consumidor.obtener_por_correoElectronico(correoElectronico):
            if Consumidor.obtener_por_correoElectronico(correoElectronico).idConsumidor != idConsumidor:
                return {'message': 'El correo electronico ya está registrado'}, HTTPStatus.BAD_REQUEST

        contraseniaHash = hash_password(contraseniaNoHash)
        consumidor.nombre = nombre
        consumidor.correoElectronico = correoElectronico
        consumidor.contrasenia = contraseniaHash
        consumidor.token = token.decode('utf-8')

        consumidor.save()
        data = {
            'idConsumidor': consumidor.idConsumidor,
            'nombre': consumidor.nombre,
            'correoElectronico': consumidor.correoElectronico,
            'token': consumidor.token
        }
        return data, HTTPStatus.OK

