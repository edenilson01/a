#!/usr/bin/env python3
'''
Modulo articulo: Contiene todos los datos necesarios para las clases que se necesitaran
a la hora de utilizar los distintod articulos con los que cuenta la 'Despensa Pan y Azucar'

- Autor: Edenilson Osnar Dominguez Amarilla
- Paradigmas de la Programacion
'''
from abc import ABCMeta, abstractmethod


class Vendible(metaclass = ABCMeta):
    '''Clase abstracta que representa que un articulo puede venderse'''
    @abstractmethod
    def vender(self):
        pass

    @abstractmethod
    def reponer(self):
        pass


class Articulo(Vendible):
    '''Clase que representa de forma general los diferentes tipos de articulos con los que cuenta
    la despensa'''
    def __init__(self, codigo_articulo, descripcion, precio_unitario, unidad_medida):
        self.__codigo_articulo = codigo_articulo
        self.__descripcion = descripcion
        self.__precio_unitario = precio_unitario
        self.__unidad_medida = unidad_medida

    def get_codigo_articulo(self):
        return self.__codigo_articulo

    def set_codigo_articulo(self, codigo_articulo):
        self.__codigo_articulo = codigo_articulo

    def get_descripcion(self):
        return self.__descripcion

    def set_descripcion(self, descripcion):
        self.__descripcion = descripcion

    def get_precio_unitario(self):
        return self.__precio_unitario

    def set_precio_unitario(self, precio_unitario):
        self.__precio_unitario = precio_unitario

    def get_unidad_medida(self):
        return self.__unidad_medida

    def vender(self):
        '''Metodo el cual retorna en una cadena todos los atributos del articulo, aunque sin el codigo articulo'''
        return '{:<45s} {:<9s}'.format(self.__descripcion + '(' + self.__unidad_medida +') ', str(self.__precio_unitario))

    def reponer(self):
        pass

    def __eq__(self, codigo_articulo):
        '''Metodo para determinar si dos articulos son iguales'''
        return self.__codigo_articulo == codigo_articulo

    def __str__(self):
        return '{:<13s} {:<45s} {:>9s}'.format(self.__codigo_articulo, self.__descripcion + '(' + self.__unidad_medida +')', str(self.__precio_unitario))


class ArticuloBebida(Articulo):
    '''Clase que representa los articulos que son bebidas dentro de la despensa'''
    def __init__(self, codigo_articulo, descripcion, precio_unitario, unidad_medida = 'und'):
        Articulo.__init__(self, codigo_articulo, descripcion, precio_unitario, unidad_medida)

    def __eq__(self, articulo):
        return Articulo.__eq__(self, articulo.get_codigo_articulo())



class ArticuloComestible(Articulo):
    '''Clase que representa los articulos que son comestibles dentro de la despensa'''
    def __init__(self, codigo_articulo, descripcion, precio_unitario, unidad_medida = 'und'):
        Articulo.__init__(self, codigo_articulo, descripcion, precio_unitario, unidad_medida)

    def __eq__(self, articulo):
        return Articulo.__eq__(self, articulo.get_codigo_articulo())


class ArticuloLimpieza(Articulo):
    '''Clase que representa los articulos que son de limpieza dentro de la despensa'''
    def __init__(self, codigo_articulo, descripcion, precio_unitario, unidad_medida = 'und'):
        Articulo.__init__(self, codigo_articulo, descripcion, precio_unitario, unidad_medida)

    def __eq__(self, articulo):
        return Articulo.__eq__(self, articulo.get_codigo_articulo())


if __name__ == '__main__':
    pass