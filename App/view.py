﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


file = 'context_content_features-small.csv'
cont = None
# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar la información al Analizador")
    print("3- Consultar los eventos y artistas por una categoria")
    print("4- Req Daniel")
    print("5- Consultar Música para estudiar ")
    print("6- Aun no ")
    print("7- Esperate we ")
    print("0- Salir")
    print("*******************************************")


def printFirstsLastsElements(least5, greater5):

    print('\nThe last 5 elements are:')
    for i in least5:
        print(i['track_id'])

    print('\nThe first 5 elements are:')
    for j in greater5:
        print(j['track_id'])


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de las pistas ....")
        controller.loadData(cont, file)
        print('pistas cargadas: ' + str(controller.sizeEvents(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        elements = controller.leastMaxElements(cont)
        printFirstsLastsElements(elements[0],
                                 elements[1])

    elif int(inputs[0]) == 3:
        charact = input("Escriba la categoria que desea consultar: ").lower()
        keylo = input("Inserte los valores minimos: ")
        keyhi = input("Inserte los valores maximos: ")
        tot = controller.caracterizeReproductions(cont, charact, keylo, keyhi)
        print(tot)

    else:
        sys.exit(0)
sys.exit(0)
