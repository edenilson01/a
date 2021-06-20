#!/usr/bin/env python3
'''
Modulo cliente: Contiene todos los datos necesarios para las clases que se necesitaran
a la hora de tener los datos de los clientes, necesarios para crear las boletas de venta
de la 'Despensa Pan y Azucar'


- Autor: Edenilson Osnar Dominguez Amarilla
- Paradigmas de la Programacion
'''

from abc import ABCMeta, abstractmethod


class Persona(metaclass = ABCMeta):
    '''Metodo que representa las personas, se utiliza para otras clases dentro del sistema'''
    def __init__(self, nombre, apellido):
        self.__nombre = nombre
        self.__apellido = apellido

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_apellido(self, apellido):
        self.__apellido = apellido

    def __str__(self):
        '''Metodo que retorna en forma de cadena todos los datos de la persona'''
        return 'Señor/a: '+ self.__nombre + ' ' + self.__apellido


class Cliente(metaclass = ABCMeta):
    '''Clase abstrata que se utiliza para representar de forma general los clientes que puede llegar
    a tener la despensa'''
    def __init__(self, ruc):
        self.__ruc = ruc

    def get_ruc(self):
        return self.__ruc

    def set_ruc(self, ruc):
        self.__ruc = ruc

    def __eq__(self, cliente_ruc):
        return self.__ruc == cliente_ruc

    def __str__(self):
        return  'RUC: ' + self.__ruc    


class ClienteRuc(Cliente):
    '''Clase que representa los clientes que puede llegar a tener la despensa, 
    este cliente poseera todos los datos personales del cliente'''
    def __init__(self, nombre, apellido, ruc):
        Persona.__init__(self, nombre, apellido)
        Cliente.__init__(self, ruc)

    def modificar_cliente_nombre(self, nombre):
        Persona.set_nombre(self, nombre)

    def modificar_cliente_apellido(self, apellido):
        Persona.set_apellido(self, apellido)

    def get_nombre(self):
        return Persona.get_nombre(self)

    def get_apellido(self):
        return Persona.get_apellido(self)

    def __str__(self):
        return Persona.__str__(self) + '\t\t\t' + Cliente.__str__(self)


class ClienteMostrador(Cliente):
    '''Clase que representa a un cliente por defecto, este cliente será utilizado en caso
    que el cliente que solicita la boleta de venta, no desee otorgar sus datos personales'''
    cantidad = 0
    def __init__(self):
        self.__nombre = 'S/N'
        Cliente.__init__(self, 'xxx')
        self.cantidad = 1

    def __str__(self):
        return 'Señor: ' + self.__nombre + '\t\t\t' + Cliente.__str__(self)


if __name__ == '__main__':
    pass