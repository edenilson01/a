#!/usr/bin/env python3
'''
Modulo Comprobante: Contiene todos los datos necesarios para las clases que se necesitaran
a la hora de utilizar las boletas de venta de la 'Despensa Pan y Azucar', posee ademas
la clase de BoletaCompra, esto para representar en un futuro las compras realizadas por la 
depensa


- Autor: Edenilson Osnar Dominguez Amarilla
- Paradigmas de la Programacion
'''

from abc import ABCMeta, abstractmethod
from Modulos.cliente import *
from Modulos.articulo import *
import time

class Comprobante(metaclass = ABCMeta):
    '''Clase abstracta que representa cualquier tipo de comprobante que podria llegar una despesa'''
    def __init__(self, cliente, articulos):
        self.__cliente = cliente
        self.__articulos = articulos

    def set_articulo(self, articulos):
        self.__articulos = articulos

    def get_cliente(self):
        return self.__cliente

    def get_articulos(self):
        return self.__articulos


class BoletaVenta(Comprobante):
    '''Representa a la boleta de venta que es emitida por la despensa como comprobante
    de compra de los clientes, hereda de Comprobante'''
    numero_boleta = 0

    def __init__(self, cliente, articulos):        
        Comprobante.__init__(self, cliente, articulos)
        self.__fecha = time.strftime('%d/%m/%y')
        BoletaVenta.numero_boleta +=1
        self.__numero_boleta = BoletaVenta.numero_boleta

    def get_fecha(self):
        return self.__fecha

    def get_numero_boleta(self):
        return self.__numero_boleta

    def calcular_subtotal(self):
        '''Metodo para obtener el subtotal de cada articulo que se encuentra registrado en la boleta,
        retorna una lista, en la cual se encuentra todos los subtotales de cada uno de los articulos registrados'''
        subtotales = []
        for articulos in Comprobante.get_articulos(self):
            subtotal = 0
            for articulo in articulos:
                subtotal += articulo.get_precio_unitario()
            subtotales.append(subtotal)

        return subtotales

    def calcular_total(self, subtotales):
        '''Metodo para calcular el total a pagar por el cliente, toma como parametro los subtotales, previamente calculados,
        retonar el total a pagar sumando cada uno de los subtotales'''
        total = 0
        for subtotal in subtotales:
            total += subtotal
        return total

    def __eq__(self, boleta_venta):
        '''Metodo para obtener si dos boletas son iguales, toma como parametro una boleta de venta 
        y compara con una su propio numero de boleta'''
        return self.__numero_boleta == boleta_venta.get_numero_boleta()


class BoletaCompra(Comprobante):
    '''Representa a la boleta de compra que es emitida por el proveedor 
    y se le entrega a la despensa como comprobante de compra, será implementada en un futuro'''
    @abstractmethod
    def __init__(self):
        pass

if __name__ == '__main__':
    pass