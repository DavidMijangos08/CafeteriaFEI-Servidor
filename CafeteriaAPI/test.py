from cgi import test
import unittest
from http import HTTPStatus
import http.client as httpClient
import json

class Test(unittest.TestCase):

    def test_agregarAdministrador(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "correoElectronico": "administradorPrueba@gmail.com",
            "contrasenia": "SoyElAdmin",
            "cargo": "Administrador"
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/administradores",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 201) 

    def test_obtenerCafeterias(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        response = connection.request(
            "GET",
            "/cafeterias",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)

    def test_obtenerCafeteriasPorFacultad(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        response = connection.request(
            "GET",
            "/cafeterias/FEI",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)

    def test_obtenerCafeteriaPorId(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        connection.request(
            "GET",
            "/cafeterias/1",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)

    def test_agregarCafeteria(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "nombreCafeteria": "Una prueba",
            "facultadPerteneciente": "FEI",
            "direccion": "Av. Xalapa, Colonia Obrero Campesino",
            "horaInicio": "7:00",
            "horaFin": "19:00"
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/cafeterias",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 201) 
    
    def test_obtenerPersonalCafeteria(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        connection.request(
            "GET",
            "/personalCafeteria/1",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)
    
    def test_agregarConsumidor(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": "Joaquin Lopez Doriga",
            "correoElectronico": "joaquin@gmail.com",
            "contrasenia": "Joaquin123"
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/consumidores",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 201) 
    
    def test_consumidorLogin(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "contrasenia": "Joaquin123"
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/consumidor/login/joaquin@gmail.com",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200) 

    def test_agregarPersonalCafeteria(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": "Lola Lopez Martinez",
            "CURP": "LOML011008MOCJRVA4",
            "correoElectronico": "lolita@gmail.com",
            "cargo": "Responsable",
            "idCafeteria": 1,
            "contrasenia": "LOML011008MOCJRVA4"
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/personalCafeteria/1",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 201) 

    
    def test_personalCafeteriaLogin(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "contrasenia": "LOML011008MOCJRVA4"
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/personalCafeteria/login/lolita@gmail.com",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200) 

    def test_agregarProducto(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": "Chilaquiles",
            "descripcion": "Chilaquiles con salsa roja",
            "precio": 25,
            "tiempoAproximado": 10,
            "rutaImagen": "img/chilaquiles.png",
            "idCafeteria": 1
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/productos/1",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 201) 

    def test_obtenerProductosCafeteria(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        connection.request(
            "GET",
            "/productos/1",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)

    def test_obtenerProductoPorId(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        connection.request(
            "GET",
            "/productos/idProducto/1",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)
    
    def test_agregarReseñaCafeteria(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "titulo": "Buena cafe",
            "opinion": "Buenos productos en la cafeteria",
            "calificacion": 5,
            "idCafeteria": 1,
            "rutaImagen": ""
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/reseniasCafeteria/1",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 201) 

    def test_obtenerReseniasCafeteria(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        connection.request(
            "GET",
            "/reseniasCafeteria/1",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)

    def test_agregarReseñaProducto(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        data = {
            "titulo": "Buenos chilaquiles",
            "opinion": "Buenos chilaquiles rojos en la cafeteria",
            "calificacion": 5,
            "idProducto": 1,
            "rutaImagen": ""
        }
        data2 = json.dumps(data)
        connection.request(
            "POST",
            "/reseniasProducto/1",
            data2, 
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 201) 

    def test_obtenerReseniasCafeteria(self):
        connection = httpClient.HTTPConnection("172.17.0.3", 9090)
        headers = {"Content-Type": "application/json"}
        connection.request(
            "GET",
            "/reseniasProducto/1",
            "",
            headers
        )
        respuestaGeneral = connection.getresponse()
        codigoEstado = respuestaGeneral.status
        self.assertEqual(codigoEstado, 200)

if __name__ == '__main__':
    unittest.main()