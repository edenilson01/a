#!/usr/bin/env python3
'''
Modulo controlador: encargado de realizar toda la logica del negocio,
en este caso la 'Despensa Pan y Azucar'

- Autor: Edenilson Osnar Dominguez Amarilla
- Paradigmas de la Programacion
'''
from abc import ABCMeta, abstractmethod
from Modulos.articulo import *
from Modulos.cliente import *
from Modulos.comprobante import *
from model import *
from view import *
from datetime import *

class Empresa(metaclass = ABCMeta):
    '''Clase abstracta el cual hace referencia al negocio'''
    def __init__(self, nombre):
        self.__nombre = nombre


class Despensa(Empresa):
    '''Clase que representa la despensa y por tanto la actividad que realiza'''
    def __init__(self):
        Empresa.__init__(self, 'Despensa Pan y Azucar')
        self.model = Model()
        #directorio en donde se encuentra la base de datos de articulos
        self.directorio_articulo = './Persistencia/BaseArticulos/Articulos.fs'
        #directorio en donde se encuentra la base de datos de boletas generadas
        self.directorio_boleta = './Persistencia/BaseBoletas/Boletas.fs'
        #directorio en donde se encuentra la base de datos de los clientes
        self.directorio_cliente = './Persistencia/BaseClientes/Clientes.fs'
        #cliente por defecto
        self.cliente = ClienteMostrador()
        self.__articulos = self.model.generar_lista(self.directorio_articulo)
        self.__boletas = self.model.generar_lista(self.directorio_boleta)
        self.__clientes = self.model.generar_lista(self.directorio_cliente)
        if self.__boletas: #si es que se encuentran boletas almacenadas recupera el ultimo numero de boleta generado, para continuar a partir de ese numero
            BoletaVenta.numero_boleta = self.__boletas[-1].get_numero_boleta()

    def generar_boleta(self, articulos_ingresados, cantidades, nombre_cliente='', apellido_cliente='', ruc_cliente=''):
        '''Metodo encargado de generar por primera vez una boleta de venta
        Recibe como paramentros:
            - Una lista de los articulos que se desea agregar a la boleta
            - Una lista de cantidades correspondientes a la lista de articulos
            - El nombre, apellido y ruc del cliente que por defecto son vacios
        Retorna:
            1: Hubo algun error durante el proceso de creacion de la boleta y retorna un mensaje indicando el error
            0: Indicando que la operacion fue exitosa y retorna la boleta generada'''
        articulos_a_vender = []
        articulos = []
        indice_cantidad_articulo = 0
        #se recorre la lista de articulos que recibe como paramentro
        for articulo in articulos_ingresados:
            for cantidad in range(int(cantidades[indice_cantidad_articulo])):
                #se genera la cantidad de un articulo
                articulos.append(articulo)

            indice_cantidad_articulo+=1
            #se agrega los articulos generados en cantidad, a una lista de articulos
            articulos_a_vender.append(articulos)
        try:
            #buscar el cliente en la base de datos mediante su ruc
            cliente = self.model.obtener_objeto_base(self.directorio_cliente, ruc_cliente)
        except KeyError:
            #si no se encontro el cliente en la base de datos, se verifican los posibles errores
            self.model.base_datos.close()
            if not nombre_cliente and not apellido_cliente and not ruc_cliente:
                #si no se ingreso ningun de los datos del cliente, se utiliza el cliente por defecto
                cliente = self.cliente
            #si no ingreso alguno de los datos del cliente, retorna 1 indicando un error, y el error
            elif not ruc_cliente:
                return 1, 'NO SE INGRESO EL RUC DEL CLIENTE'
            elif not nombre_cliente:
                return 1, 'NO SE INGRESO EL NOMBRE DEL CLIENTE'
            elif not apellido_cliente:
                return 1, 'NO SE INGRESO EL APELLIDO DEL CLIENTE'
            else:
                '''si no se encontro el cliente almacenado, y todos los campos se encuentran completos,
                se crea un objeto del tipo cliente para posteriormente crear la boleta'''
                cliente = ClienteRuc(nombre_cliente, apellido_cliente, ruc_cliente)
        boleta_venta = BoletaVenta(cliente, articulos_a_vender) #se genera la boleta de venta
        return 0, boleta_venta #retorna 0 y la boleta, indicando una operacion existosa

    def actualizar_articulo_boleta(self, boleta, articulos_ingresados, cantidades):
        '''Metodo encargado de actualizar los articulos con el que cuenta la boleta, junto con sus cantidades
        Recibe como paramentro:
            - La boleta que se desea actualiza
            - Una lista de articulos que se desean que aparezcan en la boleta
            - Una lista de cantidades, correspondiente a la cantidad de cada articulo
        Retorna la boleta con los articulos actualizados'''
        articulos_a_vender = []
        articulos = []
        indice_cantidad_articulo = 0
        #se recorre la lista de articulos que recibe como paramentro
        for articulo in articulos_ingresados:
            for cantidad in range(int(cantidades[indice_cantidad_articulo])):
                #se genera la cantidad de un articulo
                articulos.append(articulo)

            indice_cantidad_articulo+=1
            #se agrega los articulos generados en cantidad, a una lista de articulos
            articulos_a_vender.append(articulos)
            articulos = []
        #se actualiza la boleta de venta, con los nuevos articulos generados
        boleta.set_articulo(articulos_a_vender)
        return boleta

    def vender(self, boleta_venta, cliente_ingresado):
        '''Metodo encargado de guardar la boleta generada, y en todo caso el cliente (si es que este no se encuentra alamcenado) 
        en al base de datos indicando que la venta fue realizada
        Recibe como paramentro:
            - La boleta que se desea almacenar
            - El cliente bajo el cual se encuentra registrado la boleta'''
        
        if not isinstance (cliente_ingresado, ClienteMostrador): #se verifica que el cliente, no sea el cliente por defecto
            try:
                #se trata de obtener el cliente a partir de su ruc, para verificar si es que el cliente se encuentra alamcenado en la base de datos
                cliente = self.model.obtener_objeto_base(self.directorio_cliente, cliente_ingresado.get_ruc())
            except KeyError:
                self.model.base_datos.close() 
                #si no se encuentra almacenado, se guarda el cliente en la base de datos
                self.model.guardar_objeto(self.directorio_cliente, cliente_ingresado, cliente_ingresado.get_ruc())
                self.__clientes = self.model.generar_lista(self.directorio_cliente) #se actualiza la lista de clientes

        self.model.guardar_objeto(self.directorio_boleta, boleta_venta, str(boleta_venta.numero_boleta))
        #se guarda la boleta de venta en la base de datos
        self.__boletas = self.model.generar_lista(self.directorio_boleta)
        #se actualiza la lista de boletas

    def validar_cantidad_articulo(self, cantidad):
        '''Metodo encargado de validar una cantidad ingresada que corresponde a un articulo
        Recibe como parametro la cantidad del articulo
        Retorna:
            1: La cantidad ingresada no es correcta
            0: La cantidad ingresada es correcta'''
        if not cantidad:
            return 1, 'CANTIDAD NO INGRESADA'
        try:
            cantidad = int(cantidad)
            if cantidad<1: #se verificar que se halla ingresado una cantidad valida
                raise ValueError
            else:
                return 0, 'CORRECTO'
        except ValueError:
            return 1, 'CANTIDAD NO VALIDA'

    def modificar_articulo_descripcion(self, codigo_articulo, descripcion_articulo):
        '''Metodo encargado de modificar la descripcion de un articulo
        Recibe como paramentro:
            - El codigo del articulo que se desea modificar, el cual previamente ya se verifico que se encuentra
                almacenado un articulo con ese codigo
            - La nueva descripcion que se desea que tenga el articulo
        Retorna:
            1: Hubo algun error al momento de querer modificar la descripcion del articulo, y retorna un mensaje indicando el error
            0: La operacion fue realizada con exito, y retorna una cadena con los nuevos datos del articulo'''
        #se obtiene el articulo a partir de su codigo
        articulo = self.model.obtener_objeto_base(self.directorio_articulo, codigo_articulo)
        if not descripcion_articulo: #se verifica que se halla ingresado la nueva descripcion del articulo
            return 1, 'NO SE INGRESO LA DESCRIPCION DEL ARTIULO'

        articulo.set_descripcion(descripcion_articulo) #se actualiza la descripcion del articulo
        self.model.guardar_objeto(self.directorio_articulo, articulo, articulo.get_codigo_articulo())
        #se actualiza el articulo de la base de datos
        self.__articulos = self.model.generar_lista(self.directorio_articulo)
        #se actualiza la lista de articulos de la despensa
        return 0, ('Descripcion: ' + articulo.get_descripcion() + '  Precio: ' + str(articulo.get_precio_unitario()))

    def modificar_articulo_precio(self, codigo_articulo, precio):
        '''Metodo encargado de modificar el precio de un articulo
        Recibe como paramentro:
            - El codigo del articulo que se desea modificar, el cual previamente ya se verifico que se encuentra
                almacenado un articulo con ese codigo
            - el nuevo precio que se desea que tenga el articulo
        Retorna:
            1: Hubo algun error al momento de querer modificar el precio del articulo, y retorna un mensaje indicando el error
            0: La operacion fue realizada con exito, y retorna una cadena con los nuevos datos del articulo'''
        #se obtiene el articulo a partir de su codigo
        articulo = self.model.obtener_objeto_base(self.directorio_articulo, codigo_articulo)
        #se verifica que se halla ingresado el precio del articulo
        if not precio:
            return 1, 'NO SE INGRESO EL PRECIO DEL ARTICULO'
        
        try: #trata de convertir el precio del articulo a numerico para verificar que no se halla ingresado caracter erroneos
            precio_articulo = int(precio)
        except ValueError:
            return 1, 'PRECIO INCORRECTO'
        
        try: #verifica que el precio no sea negativo, ni 0
            if precio_articulo<1:
                raise ValueError
        except ValueError:
            return 1, 'PRECIO INCORRECTO'

        articulo.set_precio_unitario(precio_articulo) #se actualiza el precio del articulo
        self.model.guardar_objeto(self.directorio_articulo, articulo, articulo.get_codigo_articulo())
        #se actualiza el articulo de la base de datos
        self.__articulos = self.model.generar_lista(self.directorio_articulo)
        #se actualiza la lista de articulos de la despensa
        return 0, ('Descripcion: ' + articulo.get_descripcion() + '  Precio: ' + str(articulo.get_precio_unitario()))

    def registrar_articulo(self, codigo_articulo, descripcion_articulo, precio, tipo, unidad_medida):
        '''Metodo para registrar un nuevo articulo en la base de datos
        Recibe como paramentro:
            - El codigo del articulo 
            - La descripcion del articulo
            - El precio del articulo
            - El tipo del articulo: 1,2 o 3 dependiendo si se refiere a un ArticuloBebida, ArticuloComestible, ArticuloLimpieza, correspondientemente
            - La unidad de medida: 1, refiriendose a un articulo que se vendera en unidades; 2 refiriendo a un articulo que se vendera a granel
        Retorna:
            1: indicando que hubo algun error durante el proceso de registrar el articulo, y retorna un mensaje indicando el error
            0: el proceso fue realizado con exito, y retorna el articulo registrado'''
        
        if not codigo_articulo: #se verifica que se halla ingresado el codigo del articulo
            return 1, 'NO SE INGRESO EL CODIGO DEL ARTICULO'
        
        for articulo in self.__articulos:
            if articulo.get_codigo_articulo() == codigo_articulo: #se verifica si es que existe ya registrado ese articulo
                return 1, 'EL ARTICULO YA SE ENCUENTRA ALMACENADO'

        tipo_articulo = {1: ArticuloBebida, 2: ArticuloComestible, 3: ArticuloLimpieza}
        if not descripcion_articulo: #se verifica que se halla ingresado la descripcion del articulo
            return 1, 'NO SE INGRESO LA DESCRIPCION DEL ARTIULO'

        try: #se verifica que el precio ingresado sea valido
            precio_articulo = int(precio)
            if precio_articulo<1:
                raise ValueError
        except ValueError:
            return 1, 'PRECIO INCORRECTO'

        if not unidad_medida or not tipo: #si verifica que se cuente con los datos de unidade de medida y tipo de articulo
            return 1, 'DATOS INCOMPLETOS'
        else: #si se cuentan con todos los datos
            if unidad_medida == 2:
                '''si es que la unidad de medida es kilogramo, se crea un articulo con esa unidad, sino
                    por defecto el articulo es a unidades'''
                articulo = tipo_articulo[tipo](codigo_articulo, descripcion_articulo, precio_articulo, 'kg')
            else:
                articulo = tipo_articulo[tipo](codigo_articulo, descripcion_articulo, precio_articulo)
                #se crea el objeto dependiendo del tipo de articulo elegido
            self.model.guardar_objeto(self.directorio_articulo, articulo, codigo_articulo)
            #se guarda en la base de datos
            self.__articulos = self.model.generar_lista(self.directorio_articulo)
            #se actualiza la lista de articulos
            return 0, articulo

    def eliminar_articulo(self, codigo_articulo):
        '''Metodo encargado de eliminar un articulo a traves de su codigo_articulo, el cual previamente ya se verifico
        que el articulo con ese codigo ya se encuentra almacenado en la base de datos'''
        #se elimina el articulo
        mensaje_correcto = self.model.eliminar_objeto(self.directorio_articulo, codigo_articulo)
        self.model.base_datos.close()
        self.__articulos = self.model.generar_lista(self.directorio_articulo)

    def buscar_articulo(self, codigo_articulo):
        '''Metodo encargado de buscar un articulo en la base de datos a traves de su codigo, el cual 
        recibe como paramentro
        Retorna:
            1: indicando que no se ingreso el codigo del articulo
            2: indicando que el articulo no se encuentra almacenado
            0: el proceso fue realizado con exito; y retorna una cadena con los atribusto del articulo, y el objeto articulo'''

        if not codigo_articulo: #se verifica que se ingreso el codigo del articulo
            return 1, 'NO SE INGRESO EL CODIGO DEL ARTICULO'
        try: #verifica que el articulo se encuentre guardado
            articulo = self.model.obtener_objeto_base(self.directorio_articulo, codigo_articulo)
            return 0, ('Descripcion: ' + articulo.get_descripcion() + '\nPrecio: ' + str(articulo.get_precio_unitario())), articulo
        except KeyError:
            self.model.base_datos.close()
            return 2, 'ESE ARTICULO NO SE ENCUENTRA ALMACENADO'

    def visualizar_boletas(self, fecha_ingresada):
        '''Metodo encargado de retornar todas las boletas generadas, o todas las boletas generadas en una determinada
        fecha, la cual recibe como parametro
        Retorna:
            1: indicando que hubo algun error durante el proceso de obtener las boletas de ventas generadas, 
                y retorna un mensaje indicando el error
            0: el proceso fue realizado con exito, y retorna una lista el cual contiene todas las boletas generadas'''

        if not self.__boletas: #verifica que se encuentren boletas guardadas
            return 1,'NO SE ENCUENTRAN BOLETAS GENERADAS'
        else:
            if fecha_ingresada: #se verifica que el formato de la fecha sea correcto para realizar correstamente la comparacion
                try:
                    datetime.strptime(fecha_ingresada,"%d/%m/%y")
                except ValueError:
                    return 1, 'FECHA NO VALIDA'
        
            boletas = []
            bandera = 0
            if fecha_ingresada: #si se ingreso la fecha, busca todas las boletas generadas en esa fecha
                for boleta in self.__boletas:                    
                    if boleta.get_fecha() == fecha_ingresada: #compara si la fecha ingresada es igual a la fecha en el que se genero la boleta
                        boletas.append(boleta) #agrega a la lista de boletas
                        bandera = 1
            else: #si no se ingreso la fecha, la lista son todas las boletas generadas con las que se cuenta
                boletas = self.__boletas
                bandera = 1
        
            if bandera == 0:
                return 1, 'NO SE ENCUENTRAN BOLETAS CON ESA FECHA'
            else:
                return 0, boletas

    def visualizar_articulos(self):
        '''Metodo encargado de retornar los articulos con los que cuenta la despensa
        Retorna:
            1: indicando que hubo algun error durante el proceso de obtener los articulos con los que se cuenta
            0: indicando que la operacion fue realizada con exito, y retorna los articulos con los que se cuenta'''
        if not self.__articulos: #verifica que se encuentran articulos almancenados
            return 1, 'NO SE ENCUENTRAN ARTICULOS ALMACENADOS'
        else:
            return 0, self.__articulos

    def visualizar_clientes(self):
        '''Metodo para visualizar todos los clientes registrados en la despensa
        Retorna:
            1: indicando que hubo algun error durante el proceso de obtener los clientes con los que se cuenta
            0: indicando que la operacion fue realizada con exito, y retorna los clientes con los que se cuenta'''
        if not self.__clientes: #verifica que se encuentren clientes almancendos
            return 1,'NO SE ENCUENTRAN CLIENTES ALMACENADOS'
        else:
            return 0, self.__clientes

    def modificar_nombre_cliente(self, ruc_cliente, nombre_cliente):
        '''Metodo encargado de modificar el nombre de un cliente especifico
        Recibe como paramentro:
            - El ruc del cliente del cual se desea modificar el nombre, previamente verificado que
                el cliente se encuentre almacenado
            - El nuevo nombre con el cual se desea que cuente el cliente
        Retorna:
            1: indicando que hubo un error durante la modificacion del nombre, y retorna un mensaje indicando el error
            0: indicando que la operacion fue exitosa; y retona una cadena con los datos del cliente'''
        #se obtiene el cliente a traves de su ruc
        cliente = self.model.obtener_objeto_base(self.directorio_cliente, ruc_cliente)
        if not nombre_cliente: #se verifica que se halla ingresado el nombre del cliente
            return 1, 'NO SE INGRESO EL NOMBRE DEL CLIENTE'
        #se modifica el nombre del cliente
        cliente.modificar_cliente_nombre(nombre_cliente)
        #se actualiza la base de datos
        self.model.guardar_objeto(self.directorio_cliente, cliente, cliente.get_ruc())
        #se actualiza la lista de clientes con el que cuenta la despensa
        self.__clientes = self.model.generar_lista(self.directorio_cliente)
        
        return 0, ('Nombre: ' + cliente.get_nombre() + '  Apellido: ' + cliente.get_apellido())

    def modificar_apellido_cliente(self, ruc_cliente, apellido_cliente):
        '''Metodo encargado de modificar el apellido de un cliente especifico
        Recibe como paramentro:
            - El ruc del cliente del cual se desea modificar el nombre, previamente verificado que
                el cliente se encuentre almacenado
            - El nuevo apellido con el cual se desea que cuente el cliente
        Retorna:
            1: indicando que hubo un error durante la modificacion del apellido, y retorna un mensaje indicando el error
            0: indicando que la operacion fue exitosa; y retona una cadena con los datos del cliente'''
        #se obtiene el cliente a traves de su ruc
        cliente = self.model.obtener_objeto_base(self.directorio_cliente, ruc_cliente)
        if not apellido_cliente: #se verifica que se halla ingresado el apellido del cliente
            return 1, 'NO SE INGRESO EL APELLIDO DEL CLIENTE'
        #se modifica el apellido del cliente
        cliente.modificar_cliente_apellido(apellido_cliente) 
        #se actualiza la base de datos
        self.model.guardar_objeto(self.directorio_cliente, cliente, cliente.get_ruc())
        #se actualiza la lista de clientes con el que cuenta la despensa
        self.__clientes = self.model.generar_lista(self.directorio_cliente)
        return 0, ('Nombre: ' + cliente.get_nombre() + '  Apellido: ' + cliente.get_apellido())

    def buscar_cliente(self, ruc_cliente):
        '''Metodo encargado de buscar un cliente mediante su ruc, el cual recibe como parametro
        Retorna:
            1: indicando que no se ingreso el ruc del cliente
            2: indicando que el cliente no se encuentra almacenado
            0: indicando que la operacion fue realiza con exito; y retorna una cadena con todos los datos del cliente, y el objeto cliente'''
        if not ruc_cliente:
            return 1, 'NO SE INGRESO EL RUC DEL CLIENTE'

        try: #verifica que el articulo se encuentre guardado
            cliente = self.model.obtener_objeto_base(self.directorio_cliente, ruc_cliente)
            return 0, ('Nombre: ' + cliente.get_nombre() + '\nApellido: ' + cliente.get_apellido()), cliente
        except KeyError:
            self.model.base_datos.close()
            return 2, 'ESE CLIENTE NO SE ENCUENTRA ALMACENADO'


if __name__ == '__main__':
    pass