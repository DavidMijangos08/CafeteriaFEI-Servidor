"""
   Archivo: Producto.py                                                  
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

from models.Producto import Producto, lista_productos

class ListaProductos(Resource):
    
    def get(self, idCafeteria):
        data = []
        productos = Producto.obtener_todos_por_idCafeteria(idCafeteria)
        for producto in productos:
            data.append({
                'idProducto': producto.idProducto,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'tiempoAproximado': producto.tiempoAproximado,
                'rutaImagen': producto.rutaImagen.decode("utf-8"),
                'idCafeteria': producto.idCafeteria
            })
        return data, HTTPStatus.OK

    def post(self, idCafeteria):
        json_data = request.get_json()
        nombre = json_data.get('nombre')
        descripcion = json_data.get('descripcion')
        precio = json_data.get('precio')
        tiempoAproximado = json_data.get('tiempoAproximado')
        rutaImagen = bytes (json_data.get('rutaImagen'), 'utf-8')
        idCafeteria = json_data.get('idCafeteria')

        if Producto.obtener_por_nombre_e_idCafeteria(idCafeteria, nombre):
            return {'message': 'El nombre del producto ya está registrado'}, HTTPStatus.BAD_REQUEST

        producto = Producto(
            nombre = nombre,
            descripcion = descripcion,
            precio = precio,
            tiempoAproximado = tiempoAproximado,
            rutaImagen = rutaImagen,
            idCafeteria = idCafeteria
        )
        lista_productos.append(producto)
        producto.save()
        
        data = {
            'idProducto': producto.idProducto,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': producto.precio,
            'tiempoAproximado': producto.tiempoAproximado,
            'rutaImagen': producto.rutaImagen.decode("utf-8"),
            'idCafeteria': producto.idCafeteria
        }
        return data, HTTPStatus.CREATED

class RecursoProducto(Resource):
    def get(self, idProducto):
        producto = Producto.obtener_por_id(idProducto)
        if producto is None:
            return {'message': 'Producto de cafeteria no encontrado'}, HTTPStatus.NOT_FOUND
        data = {
            'idProducto': producto.idProducto,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'tiempoAproximado': producto.tiempoAproximado,
            'precio': producto.precio,
            'rutaImagen': producto.rutaImagen.decode("utf-8"),
            'idCafeteria': producto.idCafeteria
        }            
        return data, HTTPStatus.OK

    def put(self, idProducto):
        json_data = request.get_json()
        producto = Producto.obtener_por_id(idProducto)
        if producto is None:
            return {'message': 'Producto de cafeteria no encontrado'}, HTTPStatus.NOT_FOUND
        nombre = json_data.get('nombre')
        descripcion = json_data.get('descripcion')
        precio = json_data.get('precio')
        tiempoAproximado = json_data.get('tiempoAproximado')
        rutaImagen = bytes (json_data.get('rutaImagen'), 'utf-8')
        idCafeteria = json_data.get('idCafeteria')

        if Producto.obtener_por_nombre_e_idCafeteria(idCafeteria, nombre):
            if Producto.obtener_por_nombre_e_idCafeteria(idCafeteria, nombre).idProducto != idProducto:
                return {'message': 'El nombre del producto ya está registrado'}, HTTPStatus.BAD_REQUEST
        
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.tiempoAproximado = tiempoAproximado
        producto.rutaImagen = rutaImagen
        producto.idCafeteria = idCafeteria

        producto.save()
        data = {
            'idProducto': producto.idProducto,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'tiempoAproximado': producto.tiempoAproximado,
            'precio': producto.precio,
            'rutaImagen': producto.rutaImagen.decode("utf-8"),
            'idCafeteria': producto.idCafeteria
        }
        return data, HTTPStatus.OK

    def delete(self, idProducto):
        producto = Producto.obtener_por_id(idProducto)
        if producto is None:
            return {'message': 'Producto de cafeteria no encontrado'}, HTTPStatus.NOT_FOUND
        producto.delete()
        return HTTPStatus.NO_CONTENT

