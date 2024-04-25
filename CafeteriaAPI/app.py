"""
   Archivo: app.py                                                  
   Programador: David Alexander                                             
   Fecha de creación: 01/Jun/2022                                        
   Fecha modificación:  11/Jun/2022                                 
   Descripción: Archivo con los recursos y
   direcciones de la api para ser llamados                     
"""

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db

from resources.Administrador import ListaAdministradores, RecursoAdministrador
from resources.Cafeteria import ListaCafeterias, ListaCafeteriasPorFacultad, RecursoCafeteria
from resources.Consumidor import Consumidores, Correo, RecursoConsumidor, RecursoLoginConsumidor
from resources.PersonalCafeteria import ListaPersonalCafeteria, RecursoLoginPersonal, RecursoPersonal
from resources.Producto import ListaProductos, RecursoProducto
from resources.ReseñaCafeteria import ListaReseñasCafeteria
from resources.ReseñaProducto import ListaReseñasProducto

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)

    api.add_resource(ListaCafeterias, '/cafeterias')
    api.add_resource(RecursoCafeteria, '/cafeterias/<int:idCafeteria>')
    api.add_resource(ListaCafeteriasPorFacultad, '/cafeterias/<string:facultadPerteneciente>')

    api.add_resource(ListaPersonalCafeteria, '/personalCafeteria/<int:idCafeteria>')
    api.add_resource(RecursoLoginPersonal, '/personalCafeteria/login/<string:correoElectronico>')
    api.add_resource(RecursoPersonal, '/personalCafeteria/idPersonal/<int:idPersonal>')

    api.add_resource(Consumidores, '/consumidores')
    api.add_resource(RecursoLoginConsumidor, '/consumidor/login/<string:correoElectronico>')
    api.add_resource(RecursoConsumidor, '/consumidor/idConsumidor/<int:idConsumidor>')
    api.add_resource(Correo, '/servicioCorreo')

    api.add_resource(ListaProductos, '/productos/<int:idCafeteria>')
    api.add_resource(RecursoProducto, '/productos/idProducto/<int:idProducto>')

    api.add_resource(ListaReseñasCafeteria, '/reseniasCafeteria/<int:idCafeteria>')
    api.add_resource(ListaReseñasProducto, '/reseniasProducto/<int:idProducto>')

    api.add_resource(ListaAdministradores, '/administradores')
    api.add_resource(RecursoAdministrador, '/administradores/<string:correoElectronico>')

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9090)
