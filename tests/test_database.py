import unittest
import copy
import helpers
import database as db
import config
import csv

class TestDataBase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('15H','Pedro', 'Pascal'),
            db.Cliente('35K','Keanu', 'Reeves'),
            db.Cliente('40B','Brad','Pitt'),
        ]

    def test_buscar_clientes(self):
        cliente_existente = db.Clientes.buscar('15H')
        cliente_inexistente = db.Clientes.buscar('16H')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
    
    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('39X','Kanye','West')
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.dni, '39X')
        self.assertEqual(nuevo_cliente.nombre, 'Kanye')
        self.assertEqual(nuevo_cliente.apellido, 'West')

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('40B'))
        cliente_modificado = db.Clientes.modificar('40B','Juan','Pitt')  
        self.assertEqual(cliente_a_modificar.nombre, 'Brad')
        self.assertEqual(cliente_modificado.nombre, 'Juan')
    
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('35K')
        cliente_rebuscado = db.Clientes.buscar('35K')
        self.assertEqual(cliente_borrado.dni, '35K')
        self.assertIsNone(cliente_rebuscado)
    
    def test_dni_valido(self):
        self.assertTrue(helpers.dni_validate('00A',db.Clientes.lista))
        self.assertFalse(helpers.dni_validate('00A1123',db.Clientes.lista))
        self.assertFalse(helpers.dni_validate('F23',db.Clientes.lista))
        self.assertFalse(helpers.dni_validate('15H',db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('15H')
        db.Clientes.borrar('35K')
        db.Clientes.modificar('40B','Leo','Dicaprio')

        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline='\n') as fichero:
            reader = csv.reader(fichero,delimiter=';')
            dni, nombre, apellido = next(reader)
        
        self.assertEqual(dni,'40B')
        self.assertEqual(nombre,'Leo')
        self.assertEqual(apellido,'Dicaprio')