#!/usr/bin/env python3
'''
Modulo app: encargado iniciar el sistema
y de que el controlador realice las acciones ingresada en la vista por
el usuario que esta utilizando el sistema

- Autor: Edenilson Osnar Dominguez Amarilla
- Paradigmas de la Programacion
'''
from controlador import *
from view import *
from tkinter import Tk
import sys


class App:
    '''Clase que se utiliza para iniciar el sistema'''
    @staticmethod
    def main():
        control = Despensa()
        root = Tk()  #raiz de la vista Tkinter
        vista = View(control, root)
        vista.mainloop()


if __name__ == '__main__':
    App.main()
