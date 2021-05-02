"""
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
import os
# import random
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
#  Ruta a los archivos y tamaño consola
# ___________________________________________________

columns = os.get_terminal_size().columns

file = 'context_content_features-small.csv'
cont = None
# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*" * columns)
    print("Bienvenido")
    print("Recuerde que las opciones 1 y 2 son las principales")
    print("1- Inicializar Analizador")
    print("2- Cargar la información al Analizador")
    print("3- Consultar los eventos y artistas por una categoria")
    print("4- Req Daniel")
    print("5- Consultar Música para estudiar ")
    print("6- Aun no ")
    print("7- Esperate we ")
    print("0- Salir")
    print("*" * columns)


def printFirstsLastsElements(least5, greater5):

    print('\nThe last 5 elements are:\n')
    counter1 = 1
    for i in least5:
        print("\t", counter1, ").", i['track_id'])
        counter1 += 1

    print('\nThe first 5 elements are:\n')
    counter2 = 1
    for j in greater5:
        print("\t", counter2, ").", j['track_id'])
        counter2 += 1


def printReq1(charact, keylo, keyhi, numbers):
    print("\n\t++++++++++++ Resultados... ++++++++++++\n\t",
          charact, " is between ", str(keylo), " and", str(keyhi),
          "\n\tTotal of reproductions: ", str(numbers[0]),
          "\n\tTotal of unique artists: ", str(numbers[1]),
          "\n\t++++++++++++ Resultados... ++++++++++++")


def printreq3(keylo1, keyhi1, keylo2, keyhi2, unique):
    print("=" * columns)
    print(
          "\nRsultados: "
          "\n\tInstrumentalness is between ", str(keylo1), " and", str(keyhi1),
          "\n\tTempo is between ", str(keylo2), " and", str(keyhi2),
          "\n\tTotal of unique tracks in events: ", str(unique)
          )
    print("=" * columns)


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
        if float(keylo) < 0 or float(keyhi) < 0:
            print("\n")
            print("=" * columns)
            print("\n\tLos valores maximos o minimos son menores que 0...")
            print("\tIntente nuevamente con valores positivos")
            print("=" * columns)
            print("\n")
        else:
            tot = controller.caracterizeRep(cont, charact, keylo, keyhi)
            if tot == 0:
                print("\n")
                print("=" * columns)
                print("\n\t¡¡La categoria buscada no existe!!\n")
                print("=" * columns)
                print("\n")
            else:
                printReq1(charact, keylo, keyhi, tot)

    elif int(inputs[0]) == 4:
        print('aca va lo tuyo Daniel')

    elif int(inputs[0]) == 5:
        keylo1 = input("Inserte los valores minimos de Instrumentalness: ")
        keyhi1 = input("Inserte los valores maximos de Instrumentalness: ")
        keylo2 = input("Inserte los valores minimos de Tempo: ")
        keyhi2 = input("Inserte los valores maximos de Tempo: ")
        new1 = float(keylo1) < 0 or float(keyhi1) < 0
        new2 = float(keylo2) < 0 or float(keyhi2) < 0
        if new1 or new2:
            print("\n")
            print("=" * columns)
            print("\n\tLos valores maximos o minimos son menores que 0...")
            print("\tIntente nuevamente con valores positivos")
            print("=" * columns)
            print("\n")
        else:
            tot = controller.studyMusic(cont, keylo1, keyhi1, keylo2, keyhi2)
            printreq3(keylo1, keyhi1, keylo2, keyhi2, tot)

    else:
        sys.exit(0)
sys.exit(0)
