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
import os
import config as cf
import sys
import controller
from DISClib.DataStructures import listiterator as ite
from DISClib.ADT import list as lt
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
files2 = 'user_track_hashtag_timestamp-small.csv'
files3 = 'sentiment_values.csv'
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
    print("4- Consultar Música para irse de farra")
    print("5- Consultar Música para estudiar ")
    print("6- Consultar eventos por genero")
    print("7- Género musical más escuchado en el tiempo")
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
    print("=" * columns)
    print("\nRsultados: \n\t",
          charact.capitalize(), " is between ", str(keylo), " and", str(keyhi),
          "\n\tTotal of reproductions: ", str(numbers[0]),
          "\n\tTotal of unique artists: ", str(numbers[1], '\n'))
    print("=" * columns)


def printreq2(keylo1, keyhi1, keylo2, keyhi2, unique, lista):
    print("=" * columns)
    print("\nRsultados: "
          "\n\tEnergy is between", str(keylo1), "and", str(keyhi1),
          "\n\tDanceability is between", str(keylo2), "and", str(keyhi2),
          "\n\tTotal of unique tracks in events: ", str(unique))
    print("\n------ Some artists ------")
    pos = 1
    for i in lista['elements']:
        print("Track", str(pos) + ":", i['track_id'], "with",
              'energy of', i['energy'], 'and danceability of',
              i['danceability'])
        pos += 1
    print("=" * columns)


def printreq3(keylo1, keyhi1, keylo2, keyhi2, unique, lista):
    print("=" * columns)
    print("\nRsultados: "
          "\n\tInstrumentalness is between", str(keylo1), "and", str(keyhi1),
          "\n\tTempo is between", str(keylo2), "and", str(keyhi2),
          "\n\tTotal of unique tracks in events: ", str(unique))
    print("\n------ Some artists ------")
    if lista == 0:
        print("No hay suficientes elementos para imprimir")
    else:
        pos = 1
        for i in lista['elements']:
            print("Track", str(pos) + ":", i['track_id'], "with",
                  'instrumentalness of', i['instrumentalness'],
                  'and a tempo of', i['tempo'])
            pos += 1
    print("=" * columns)


def printreq4(gender, keylo, keyhi, rep, artists, artlist):
    print("================ ", gender.upper(), " ================")
    print("For", gender, "the tempo is between", float(keylo), "and",
          float(keyhi), " BPM")
    print(gender, " reproductions:", rep, "with", artists,
          " different artists")
    print("\n------ Some artists for", gender, " ------")
    pos = 1
    for i in artlist['elements']:
        print("Artist", str(pos) + ":", i)
        pos += 1


def printreq5(init, final, reps, genrelist, genderlist, first):
    print("=" * columns)
    print('\nThere is a total of', reps, 'reproductions between',
          init, 'and', final)

    print("============= GENRES SORTED REPRODUCTIONS =============")
    i = 0
    iterator = ite.newIterator(genrelist)
    while ite.hasNext(iterator):
        pos = ite.next(iterator)
        print('TOP', str(i) + ':', pos[0], 'with', pos[1], 'reps')
        i += 1
    print('\n')
    print('The TOP GENRE is',
          first[0], 'with', first[1], 'reproductions...\n')

    print("============= GENRES SORTE REPRODUCTIONS =============")
    j = 1
    for i in genderlist['elements']:
        if j == 10:
            break
        else:
            print('TOP', j, 'track' + ':', i[0], 'with',
                  i[1], 'hashtags and VADER =', i[2])
            j += 1


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
        print('=' * columns)
        print("Cargando información de las pistas ....")
        controller.loadData(cont, file)
        controller.loadData2(cont, files2)
        controller.loadData3(cont, files3)
        print('\nTotal de eventos cargados: ' +
              str(controller.sizeEvents(cont)))
        print('\nInstrumentalness altura: ' +
              str(controller.indexHeight(cont['instrumentalness'])))
        print('Acousticness altura: ' +
              str(controller.indexHeight(cont['acousticness'])))
        print('Liveness altura: ' +
              str(controller.indexHeight(cont['liveness'])))
        print('Speechiness altura: ' +
              str(controller.indexHeight(cont['speechiness'])))
        print('Energy altura: ' +
              str(controller.indexHeight(cont['energy'])))
        print('Danceability altura: ' +
              str(controller.indexHeight(cont['danceability'])))
        print('Valence altura: ' +
              str(controller.indexHeight(cont['valence'])))
        print('Tempo altura: ' +
              str(controller.indexHeight(cont['tempo'])))
        print('\nArtistas únicos: ' +
              str(controller.indexSize(cont['artists'])))
        print('Pistas únicas: ' +
              str(controller.indexSize(cont['tracks'])))
        print('\nMenor Llave: ' +
              str(controller.minKey(cont)))
        print('Mayor Llave: ' +
              str(controller.maxKey(cont)))
        elements = controller.leastMaxElements(cont)
        printFirstsLastsElements(elements[0],
                                 elements[1])
        print('\n')
        print('=' * columns)

    elif int(inputs[0]) == 3:
        charact = input("Escriba la categoria que desea consultar: ").lower()
        keylo = input("Inserte los valores minimos: ")
        keyhi = input("Inserte los valores maximos: ")
        if1 = float(keylo) < 0
        if2 = float(keyhi) < 0
        if3 = float(keylo) > float(keyhi)
        if if1 or if2 or if3:
            print("\n")
            print("=" * columns)
            print("\n\tLos valores maximos o minimos son menores que 0...")
            print("\tIntente nuevamente con valores positivos")
            print("\n")
            print("=" * columns)

        else:
            tot = controller.caracterizeRep(cont, charact,
                                            float(keylo), float(keyhi))
            if tot == 0:
                print("\n")
                print("=" * columns)
                print("\n\t¡¡La categoria buscada no existe!!\n")
                print("=" * columns)
                print("\n")
            else:
                printReq1(charact, keylo, keyhi, tot)

    elif int(inputs[0]) == 4:
        keylo1 = input("Inserte los valores minimos de Energy: ")
        keyhi1 = input("Inserte los valores maximos de Energy: ")
        keylo2 = input("Inserte los valores minimos de Danceability: ")
        keyhi2 = input("Inserte los valores maximos de Danceability: ")
        new1 = float(keylo1) < 0 or float(keyhi1) < 0
        new2 = float(keylo2) < 0 or float(keyhi2) < 0
        new3 = float(keylo1) > float(keyhi1)
        new4 = float(keylo2) > float(keyhi2)

        if new3 or new4:
            print("\n")
            print("=" * columns)
            print("\n\tLos valores minimos son mayores que los maximos...")
            print("\tPor favor intente nuevamente")
            print("=" * columns)
            print("\n")

        elif new1 or new2:
            print("\n")
            print("=" * columns)
            print("\n\tLos valores maximos o minimos son menores que 0...")
            print("\tIntente nuevamente con valores positivos")
            print("=" * columns)
            print("\n")

        else:
            tot = controller.partyMusic(cont, float(keylo1),
                                        float(keyhi1), float(keylo2),
                                        float(keyhi2))
            if tot == 0:
                print('\n')
                print('=' * columns)
                print("\n\tNo se encontraron resultados")
                print('=' * columns)
                print('\n')
            else:
                printreq2(keylo1, keyhi1, keylo2, keyhi2, tot[0], tot[1])

    elif int(inputs[0]) == 5:
        keylo1 = input("Inserte los valores minimos de Instrumentalness: ")
        keyhi1 = input("Inserte los valores maximos de Instrumentalness: ")
        keylo2 = input("Inserte los valores minimos de Tempo: ")
        keyhi2 = input("Inserte los valores maximos de Tempo: ")
        new1 = float(keylo1) < 0 or float(keyhi1) < 0
        new2 = float(keylo2) < 0 or float(keyhi2) < 0
        new3 = float(keylo1) > float(keyhi1)
        new4 = float(keylo2) > float(keyhi2)

        if new3 or new4:
            print("\n")
            print("=" * columns)
            print("\n\tLos valores minimos son mayores que los maximos...")
            print("\tPor favor intente nuevamente")
            print("=" * columns)
            print("\n")

        elif new1 or new2:
            print("\n")
            print("=" * columns)
            print("\n\tLos valores maximos o minimos son menores que 0...")
            print("\tIntente nuevamente con valores positivos")
            print("=" * columns)
            print("\n")

        else:
            tot = controller.partyMusic(cont, float(keylo1),
                                        float(keyhi1), float(keylo2),
                                        float(keyhi2))
            if tot == 0:
                print('\n')
                print('=' * columns)
                print("\n\tNo se encontraron resultados")
                print('=' * columns)
                print('\n')
            else:
                printreq3(keylo1, keyhi1, keylo2, keyhi2, tot[0], tot[1])

    elif int(inputs[0]) == 6:
        reggae = controller.reggae(cont)
        down = controller.down(cont)
        chill = controller.chill(cont)
        hiphop = controller.hiphop(cont)
        jazzfunk = controller.jazzfunk(cont)
        pop = controller.pop(cont)
        ryb = controller.ryb(cont)
        rock = controller.rock(cont)
        metal = controller.metal(cont)
        print("=" * columns)
        print("\n")
        printreq4("Reggae", 60, 90, reggae[0], reggae[2], reggae[1])
        print("\n")
        printreq4("Down-tempo", 70, 100, down[0], down[2], down[1])
        print("\n")
        printreq4("Chill-out", 90, 120, chill[0], chill[2], chill[1])
        print("\n")
        printreq4("Hip-hop", 85, 115, hiphop[0], hiphop[2], hiphop[1])
        print("\n")
        printreq4("Jazz and Funk", 120, 125, jazzfunk[0], jazzfunk[2],
                  jazzfunk[1])
        print("\n")
        printreq4("Pop", 100, 130, pop[0], pop[2], pop[1])
        print("\n")
        printreq4("R&B", 60, 80, ryb[0], ryb[2], ryb[1])
        print("\n")
        printreq4("Rock", 110, 140, rock[0], rock[2], rock[1])
        print("\n")
        printreq4("Metal", 100, 160, metal[0], metal[2], metal[1])
        print("\n")
        print("=" * columns)

    elif int(inputs[0]) == 7:
        print('\t--- El formato es HH:MM:SS ---')
        time1 = input("Ingrese el valor minimo de la hora del dia: ")
        time2 = input("Ingrese el valor maximo de la hora del dia: ")
        tot = controller.musicInTime(cont, time1, time2)
        if tot == 0:
            print('\n')
            print('=' * columns)
            print("Por favor ingrese horas del dia positivas")
            print('\n')
            print('=' * columns)
        else:
            genres = controller.getgenres(tot[1])
            first = lt.firstElement(genres)
            values = controller.getgenre(tot[1], first, cont['hashtag'],
                                         cont['vader'])
            thelist = controller.sortreq5(values)
            printreq5(time1, time2, tot[0], genres, thelist, first)

    else:
        sys.exit(0)
sys.exit(0)
