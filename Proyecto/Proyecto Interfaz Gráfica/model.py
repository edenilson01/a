#!/usr/bin/env python3
'''
Modulo model: encargado de realizar la persistencia en la base de datos ZODB,
o de obtener los datos de la base de datos. El controlador se comunica con él para 

- Autor: Edenilson Osnar Dominguez Amarilla
- Paradigmas de la Programacion
'''
from Persistencia.zodb import MiZODB, transaction

class Model:
    base_datos = ''

    def obtener_objeto_base(self, directorio, clave):
        '''Metodo para obtener un objeto almancenado en la base de datos
        Toma como paramentro: el directorio en donde se encuentra la base de datos
        y la clave del objeto
        Retorna: el objeto si que es lo encuentra'''
        Model.base_datos = MiZODB(directorio)
        base_datos_root = Model.base_datos.raiz
        objeto = base_datos_root[clave]
        Model.base_datos.close()
        return objeto 

    def generar_lista(self, directorio):
        '''Metodo para generar una lista a partir de todos los objetos que se encuentran
        almacenados en la base de datos
        Toma como paramentro: el directorio en donde se encuentra la base de datos
        Retorna: la lista creada a partir de los objetos'''
        Model.base_datos = MiZODB(directorio)
        base_datos_root = Model.base_datos.raiz
        objetos = []
        for key in base_datos_root.keys():
            objeto = base_datos_root[key]
            objetos.append(objeto)
        
        Model.base_datos.close()
        return objetos

    def eliminar_objeto(self, directorio, clave):
        '''Metodo para eliminar algun objeto de la base de datos
        Toma como paramentro: el directorio en donde se encuentra la base de datos
        y la clave del objeto que se desea eliminar
        Retorna: un mensaje indicando que elimino el objeto'''
        Model.base_datos = MiZODB(directorio)
        base_datos_root = Model.base_datos.raiz
        del base_datos_root[clave]            
        transaction.commit()
        Model.base_datos.close()
        return 'Se elimino con exito los datos'


    def guardar_objeto(self, directorio, objeto, etiqueta):
        '''Metodo para guardar un objeto dentro de la base de datos
        Toma como paramentro: el directorio en donde se encuentra la base de datos en la cual
        desea persistir los datos y la etiqueta o clave que tengra el objeto
        Retorna: un mensaje indicando que se guardo el objeto'''
        Model.base_datos = MiZODB(directorio)
        base_datos_root = Model.base_datos.raiz
        base_datos_root[etiqueta] = objeto
        transaction.commit() 
        Model.base_datos.close()
        return 'Los datos se guardaron correctamente'


if __name__ == '__main__':
    pass