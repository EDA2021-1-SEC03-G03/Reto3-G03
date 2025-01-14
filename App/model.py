﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import random
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.Algorithms.Sorting import shellsort as she
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import listiterator as ite
from DISClib.DataStructures import mapentry as me
assert cf
# from DISClib.Algorithms.Sorting import shellsort as sa

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos lists,
una para los videos, otra para las categorias de
los mismos.
"""

# ==============================
# API del TAD Catalogo de Libros
# ==============================


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todas las pistas
    Se crean indices (Maps) por los siguientes criterios:
    -track_id

    Retorna el analizador inicializado.
    """
    analyzer = {'event': None,
                'tracks': None,
                'artists': None,
                'instrumentalness': None,
                'acousticness': None,
                'liveness':  None,
                'speechiness': None,
                'energy': None,
                'danceability': None,
                'valence': None,
                'tempo': None,
                'time': None,
                'hashtag': None,
                'vader': None
                }
    # Cambiar el nombre porque son eventos de escucha

    analyzer['event'] = lt.newList('ARRAY_LIST')

    analyzer['tracks'] = om.newMap(omaptype='RBT')

    analyzer['artists'] = om.newMap(omaptype='RBT')

    analyzer['instrumentalness'] = om.newMap(omaptype='RBT')

    analyzer['acousticness'] = om.newMap(omaptype='RBT')

    analyzer['liveness'] = om.newMap(omaptype='RBT')

    analyzer['speechiness'] = om.newMap(omaptype='RBT')

    analyzer['energy'] = om.newMap(omaptype='RBT')

    analyzer['danceability'] = om.newMap(omaptype='RBT')

    analyzer['valence'] = om.newMap(omaptype='RBT')

    analyzer['tempo'] = om.newMap(omaptype='RBT')

    analyzer['time'] = om.newMap(omaptype='RBT')

    analyzer['hashtag'] = mp.newMap(numelements=100000,
                                    maptype='PROBING',
                                    loadfactor=0.5)

    analyzer['vader'] = mp.newMap(numelements=100000,
                                  maptype='PROBING',
                                  loadfactor=0.5)

    return analyzer


# ==============================
# Funciones para agregar informacion al catalogo
# ==============================


def addEvent(analyzer, event):
    """
    Añade cada uno de los eventos de escucha con toda su información
    a una estructura de tipo ARRAY_LIST
    """
    lt.addLast(analyzer['event'], event)
    updateIdIndex(analyzer['tracks'], event)
    updateartistsIndex(analyzer['artists'], event)
    updateContCara(analyzer, event)
    return analyzer


def updateIdIndex(maps, event):
    """
    Se toma El track_id de cada evento y se adiciona al map. 
    Si el track_id del evento ya esta en el arbol, se adiciona
    a su lista respectiva y se actualiza el index.
    Si no se encuentra creado un nodo para ese id en el arbol
    se crea y se actualiza el indice del id de las pistas.
    """
    eventId = event['track_id']
    entry = om.get(maps, eventId)
    if entry is None:
        datantry = newDataEntry(event)
        om.put(maps, eventId, datantry)
    else:
        datantry = me.getValue(entry)
        addEntry(datantry, event)
    return maps


def updateartistsIndex(maps, event):
    """
    Se toma El track_id de cada evento y se adiciona al map
    . Si el track_id del evento ya esta en el arbol, se adiciona
    a su lista respectiva y se actualiza el index.

    Si no se encuentra creado un nodo para ese id en el arbol
    se crea y se actualiza el indice del id de las pistas.
    """
    eventId = event['artist_id']
    entry = om.get(maps, eventId)
    if entry is None:
        datantry = newDataEntry(event)
        om.put(maps, eventId, datantry)
    else:
        datantry = me.getValue(entry)
        addEntry(datantry, event)
    return maps


def updateContCara(maps, event):
    '''
    Actualiza los arboles de cada una de las carateristicas de
    contenido. Agrega una lista con todos los eventos de escucha
    al arbol dependiendo del valor que estos tienen en esa caracteristica.
    '''
    # Cada una de las caracteristicas de contenido es un arbol

    characteristics = ['instrumentalness', 'acousticness',
                       'liveness', 'speechiness', 'energy',
                       'danceability', 'valence', 'tempo', 'time']
    for i in characteristics:
        if i == 'time':
            time = event['created_at'].split(' ')
            timeinseconds = seconds(time[1])
            entry = om.get(maps[i], timeinseconds)

            if entry is None:
                datantry = newDataEntry(event)
                om.put(maps[i], timeinseconds, datantry)
            else:
                datantry = me.getValue(entry)
                addEntry(datantry, event)
        else:
            entry = om.get(maps[i], float(event[i]))

            if entry is None:
                datantry = newDataEntry(event)
                om.put(maps[i], float(event[i]), datantry)
            else:
                datantry = me.getValue(entry)
                addEntry(datantry, event)
    return maps


def addEntry(value, event):
    """
    Añade un evento a la lista que es valor en cada uno de los
    mapas del analyzer
    """
    lst = value['lstevent']
    lt.addLast(lst, event)


def newDataEntry(event):
    """
    Crea una entrada en el indice por track_id, es decir en el arbol
    binario.
    """
    entry = {'lstevent': None}

    entry['lstevent'] = lt.newList('ARRAY_LIST')
    lt.addLast(entry['lstevent'], event)
    return entry


def updateHashtag(maps, hashtags):
    '''
    Actualiza el indice de hashtag que es una tabla de hash.
    la llave es el track id, esto se hace para poder conectar
    los diferents archivos que hay.
    '''
    entry = mp.get(maps['hashtag'], hashtags['track_id'])

    if entry is None:
        dataentry = newDataEntry(hashtags)
        mp.put(maps['hashtag'], hashtags['track_id'], dataentry)
    else:
        pair = mp.get(maps['hashtag'], hashtags['track_id'])
        dataentry = me.getValue(pair)
        addEntry(dataentry, hashtags)
    return maps


def updatevader(maps, sentiment):
    '''
    Actualiza el indice de vader que es una tabla de hash.
    La llave es el hashtag, esto se hace para poder conectar
    los diferentes archivos que hay.
    El valor es toda la informacion.
    '''
    entry = mp.get(maps['vader'], sentiment['hashtag'].lower())

    if entry is None:
        dataentry = newDataEntry(sentiment)
        mp.put(maps['vader'], sentiment['hashtag'].lower(), dataentry)
    else:
        pair = mp.get(maps['vader'], sentiment['hashtag'].lower())
        dataentry = me.getValue(pair)
        addEntry(dataentry, sentiment)
    return maps


def seconds(time):
    long = time.split(':')
    hours = int(long[0])
    minutes = int(long[1])
    seconds = int(long[2])

    return (hours * 3600) + (minutes * 60) + seconds


# ==============================
# Funciones de consulta
# ==============================


def caracterizeReproductions(maps, characteristic, keylo, keyhi):
    '''
    Consulta los eventos de escucho dados una caracteristica de
    contenido y un rango de valor. Retorna la cantidad de eventos
    y la cantida de artistas unicos que cumplen las caracteristicas
    pasadas por el usuario.
    '''
    exists = characteristic in maps
    if exists is True:
        events = om.values(maps[characteristic], keylo, keyhi)
        # creamos una tabla de has para guardar a los artistas unicos
        artistsMap = mp.newMap(34500,
                               maptype='PROBING',
                               loadfactor=0.5)
        eventsq = 0
        '''
        Debemos recorrer dos veces porque en cada posicion de los elementos
        retornados en events hay una lista con cada uno de los eventos que
        tienen los mismos valores pero que fueron publicados por una persona
        diferente en twitter.
        '''
        iterator = ite.newIterator(events)
        while ite.hasNext(iterator):
            # este elemento tiene la lista con los eventos
            eventlist = ite.next(iterator)
            # Se suman la cantidad de eventos
            eventsq += lt.size(eventlist['lstevent'])
            newiterator = ite.newIterator(eventlist['lstevent'])
            while ite.hasNext(newiterator):
                # Este ya es el evento con sus caracteristicas
                event = ite.next(newiterator)
                # Se agrega a una tabla de hash los id's de los artistas
                mp.put(artistsMap, event['artist_id'], 0)
        # Es la cantidad de artistas unicos del requerimiento
        artistsq = mp.size(artistsMap)
        return eventsq, artistsq
    else:
        return 0


def get5artists(map, lista, size):
    '''
    Funcion que me retorna 10 valores al azar de una lista de
    listas pasada por parametro
    '''
    finallist = lt.newList("ARRAY_LIST")
    eventlist = random.sample(range(size), 5)
    for i in eventlist:
        keya = lt.getElement(lista, i)
        lt.addLast(finallist, keya)
    return finallist


def get10artists(artistmap, lista, size):
    '''
    Funcion que me retorna 10 valores al azar de una lista de
    listas pasada por parametro
    '''
    finallist = lt.newList("ARRAY_LIST")
    eventlist = random.sample(range(size), 10)
    for i in eventlist:
        keya = lt.getElement(lista, i)
        lt.addLast(finallist, keya)
    return finallist


def studyMap(maps, keylo1, keyhi1, keylo2, keyhi2, caract1, caract2):
    '''
    Busca dentro del mapa deseado, en un rango
    especificado por el usuario, los eventos con una pista
    unica que cumplen el rango especificado.
    '''
    # Aca se organizaran los eventos por segunda vez
    eventsmap = om.newMap(omaptype='RBT')
    # Es la lista con todos los eventos de instrumentalness
    eventslist = om.values(maps[caract1], keylo1, keyhi1)
    if lt.isEmpty(eventslist):
        return None
    else:
        iterator = ite.newIterator(eventslist)
        while ite.hasNext(iterator):
            events = ite.next(iterator)
            newiterator = ite.newIterator(events['lstevent'])
            while ite.hasNext(newiterator):
                event = ite.next(newiterator)
                om.put(eventsmap, float(event[caract2]), event)
        return om.values(eventsmap, keylo2, keyhi2)


def partyMusic(maps, keylo1, keyhi1, keylo2, keyhi2):
    '''
    Recorre en los index de Energy y da buscando las
    opciones dentro del rango que busca el usuario
    '''
    easylist = studyMap(maps, keylo1, keyhi1, keylo2, keyhi2,
                        'energy', 'danceability')
    if easylist is None:
        return 0
    else:
        tracksMap = mp.newMap(34500,
                              maptype='PROBING',
                              loadfactor=0.5)
        iterator = ite.newIterator(easylist)
        while ite.hasNext(iterator):
            events = ite.next(iterator)
            mp.put(tracksMap, events['track_id'], events)
        size = lt.size(tracksMap)
        if size > 5:
            tracklist = 0
        else:
            lista = mp.valueSet(tracksMap)
            tracklist = get5artists(tracksMap, lista, size)
        return size, tracklist


def studyMusic(maps, keylo1, keyhi1, keylo2, keyhi2):
    '''
    Recorre en los index de instrumentalness y tempo buscando las
    opciones dentro del rango que busca el usuario
    '''
    caract1 = 'instrumentalness'
    caract2 = 'tempo'
    easylist = studyMap(maps, keylo1, keyhi1, keylo2, keyhi2, caract1, caract2)
    if easylist is None:
        return 0
    else:
        tracksMap = mp.newMap(34500,
                              maptype='PROBING',
                              loadfactor=0.5)
        iterator = ite.newIterator(easylist)
        while ite.hasNext(iterator):
            events = ite.next(iterator)
            mp.put(tracksMap, events['track_id'], events)
        size = lt.size(tracksMap)
        if size > 5:
            tracklist = 0
        else:
            lista = mp.valueSet(tracksMap)
            tracklist = get5artists(tracksMap, lista, size)
        return size, tracklist


def reggae(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero reggae, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    reggaemap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    reggae = om.values(maps['tempo'], 60, 90)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(reggae)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(reggaemap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(reggaemap)
    size = lt.size(lista)
    artistslist = get10artists(reggaemap, lista, size)
    return reproductions, artistslist, size


def down(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero Down-tempo, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    downmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    down = om.values(maps["tempo"], 70, 100)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(down)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(downmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(downmap)
    size = lt.size(lista)
    artistslist = get10artists(downmap, lista, size)
    return reproductions, artistslist, size


def chill(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero Chill-out, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    chillmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    chill = om.values(maps["tempo"], 90, 120)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(chill)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(chillmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(chillmap)
    size = lt.size(lista)
    artistslist = get10artists(chillmap, lista, size)
    return reproductions, artistslist, size


def hiphop(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero Hip-hop, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    hiphopmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    hiphop = om.values(maps["tempo"], 85, 115)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(hiphop)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(hiphopmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(hiphopmap)
    size = lt.size(lista)
    artistslist = get10artists(hiphopmap, lista, size)
    return reproductions, artistslist, size


def jazzfunk(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero Jazz and funk, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    jazzfunkmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    jazzfunk = om.values(maps["tempo"], 120, 125)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(jazzfunk)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(jazzfunkmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(jazzfunkmap)
    size = lt.size(lista)
    artistslist = get10artists(jazzfunkmap, lista, size)
    return reproductions, artistslist, size


def pop(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero Pop, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    popmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    pop = om.values(maps["tempo"], 100, 130)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(pop)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(popmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(popmap)
    size = lt.size(lista)
    artistslist = get10artists(popmap, lista, size)
    return reproductions, artistslist, size


def ryb(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero ryb, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    rybmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    ryb = om.values(maps["tempo"], 60, 80)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(ryb)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(rybmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(rybmap)
    size = lt.size(lista)
    artistslist = get10artists(rybmap, lista, size)
    return reproductions, artistslist, size


def rock(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero rock, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    rockmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    rock = om.values(maps["tempo"], 110, 140)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(rock)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(rockmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(rockmap)
    size = lt.size(lista)
    artistslist = get10artists(rockmap, lista, size)
    return reproductions, artistslist, size


def metal(maps):
    '''
    Funcion que retorna la cantidad de de reproducciones de
    canciones de genero metal, la cantidad de artistas unicos
    y 10 id's de artistas al azar
    '''
    # Aca se agregaran los artistas unicos
    metalmap = om.newMap(omaptype='RBT')
    reproductions = 0
    # Se obtienen los eventos en el rango del genero
    metal = om.values(maps["tempo"], 100, 160)
    # Recorre el arbol y busca los valores del genero
    iterator = ite.newIterator(metal)
    while ite.hasNext(iterator):
        eventlist = ite.next(iterator)
        # agrega la cantidad de videos que hay dentro de cada valor
        reproductions += lt.size(eventlist['lstevent'])
        newiterator = ite.newIterator(eventlist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            # Agrega a los artistas a un mapa para saber los unicos
            om.put(metalmap, event['artist_id'], event)
    # Es una lista con 5 artists_id al azar
    lista = om.keySet(metalmap)
    size = lt.size(lista)
    artistslist = get10artists(metalmap, lista, size)
    return reproductions, artistslist, size


def musicInTime(maps, time1, time2):
    '''
    Funcion que busca los eventos en un rango de tiempo.
    retorna la cantidad de eventos de escucha totales y
    un mapa con los eventos
    '''
    init = seconds(time1)
    final = seconds(time2)
    if init < 0 or final < 0:
        return 0
    else:
        # thelist = lt.newList("ARRAY_LIST")
        themap = om.newMap(omaptype='RBT')
        eventsq = 0
        # Sacamos lo eventos en el rango deseado por el usuario
        getusers = om.values(maps['time'], init, final)
        # Recorremos la lista de las listas de los eventos
        iterator = ite.newIterator(getusers)
        while ite.hasNext(iterator):
            eventslist = ite.next(iterator)
            # Para encontrar el numero total de eventos en el rango
            newiterator = ite.newIterator(eventslist['lstevent'])
            while ite.hasNext(newiterator):
                event = ite.next(newiterator)
                eventsq += 1
                entry = om.get(themap, float(event['tempo']))
                if entry is None:
                    dataentry = newDataEntry(event)
                    om.put(themap, float(event['tempo']), dataentry)
                else:
                    dataentry = me.getValue(entry)
                    addEntry(dataentry, event)
        return eventsq, themap


def getgenres(maps):
    '''
    funcion que encuentra la cantidad de reproducciones por genero
    '''
    thehash = lt.newList("ARRAY_LIST")

    reggae = om.values(maps, 60, 90)
    reggaesize = getsize(reggae)
    lt.addLast(thehash, ('Reggae', reggaesize))

    down = om.values(maps, 70, 100)
    downsize = getsize(down)
    lt.addLast(thehash, ('Down-tempo', downsize))

    chill = om.values(maps, 90, 120)
    chillsize = getsize(chill)
    lt.addLast(thehash, ('Chill-out', chillsize))

    hiphop = om.values(maps, 85, 115)
    hiphopsize = getsize(hiphop)
    lt.addLast(thehash, ('Hip-hop', hiphopsize))

    jazzfunk = om.values(maps, 120, 125)
    jazzfunksize = getsize(jazzfunk)
    lt.addLast(thehash, ('Jazz and Funk', jazzfunksize))

    pop = om.values(maps, 100, 130)
    popsize = getsize(pop)
    lt.addLast(thehash, ('Pop', popsize))

    ryb = om.values(maps, 60, 80)
    rybsize = getsize(ryb)
    lt.addLast(thehash, ('R&B', rybsize))

    rock = om.values(maps, 110, 140)
    rocksize = getsize(rock)
    lt.addLast(thehash, ('Rock', rocksize))

    metal = om.values(maps, 100, 160)
    metalsize = getsize(metal)
    lt.addLast(thehash, ('Metal', metalsize))

    thehash = sortgenres(thehash)

    return thehash


def getgenre(maps, genretuple, table, table2):
    '''
    Funcion que define el genero que mas reproducciones tiene.
    despues busca los hashtags que tiene cada track dentro del
    genero top y retorna una lista con el track, la cantidad de
    hashtags que tiene y el vader promedio.
    '''
    # Se guarda la informacion de los videos por tracks_id
    newmap = om.newMap(omaptype='RBT')
    # Busca cual es el genero que es el top
    if genretuple[0] == "Reggae":
        value = om.values(maps, 60, 90)
    elif genretuple[0] == "Down-tempo":
        value = om.values(maps, 70, 100)
    elif genretuple[0] == "Chill-out":
        value = om.values(maps, 90, 120)
    elif genretuple[0] == "Hip-hop":
        value = om.values(maps, 85, 115)
    elif genretuple[0] == "Jazz and Funk":
        value = om.values(maps, 120, 125)
    elif genretuple[0] == "Pop":
        value = om.values(maps, 100, 130)
    elif genretuple[0] == "R&B":
        value = om.values(maps, 60, 80)
    elif genretuple[0] == "Rock":
        value = om.values(maps, 110, 140)
    elif genretuple[0] == "Metal":
        value = om.values(maps, 100, 160)

    # Recorre la lista de valores del genero top
    iterator = ite.newIterator(value)
    while ite.hasNext(iterator):
        eventslist = ite.next(iterator)
        newiterator = ite.newIterator(eventslist['lstevent'])
        while ite.hasNext(newiterator):
            event = ite.next(newiterator)
            entry = om.get(newmap, event['track_id'])
            if entry is None:
                dataentry = newDataEntry(event)
                om.put(newmap, event['track_id'], dataentry)
            else:
                dataentry = me.getValue(entry)
                addEntry(dataentry, event)

    # se crea una lista con todos los tracks_id
    tracksid = om.keySet(newmap)
    finallist = lt.newList("ARRAY_LIST")
    '''
    Se recorren cada uno de los id para sacar la informacion
    y compararla con el mapa de hashtags
    '''
    tracksiterator = ite.newIterator(tracksid)
    while ite.hasNext(tracksiterator):
        info = ite.next(tracksiterator)
        entry = mp.get(table, info)
        entryvalue = me.getValue(entry)
        # Es una tabla de has temporal donde se guardan los hashtags
        hasht = mp.newMap(numelements=15, maptype='PROBING',
                          loadfactor=0.5)
        newiterator = ite.newIterator(entryvalue['lstevent'])
        # Aca se comenzaran a sumar los vaders
        sumvader = 0
        while ite.hasNext(newiterator):
            trackhash = ite.next(newiterator)
            hashtag = trackhash['hashtag'].lower()
            mp.put(hasht, hashtag, 0)
            # Se saca la informacion de la tabal de vader
            vader = mp.get(table2, hashtag)
            if vader is None:
                break
            else:
                vadevalue = me.getValue(vader)
                juandiego = ite.newIterator(vadevalue['lstevent'])
                
                while ite.hasNext(juandiego):
                    pos = ite.next(juandiego)
                    # Hay valores de vader que no existen
                    if pos['vader_avg'] == '':
                        sumvader += 0
                    else:
                        averagevader = float(pos['vader_avg'])
                        sumvader += averagevader
        nohash = mp.size(hasht)
        # Se saca el promedio de vader
        avgvader = round(sumvader / nohash, 1)
        lt.addLast(finallist, (info, nohash, avgvader))
    return finallist


def sizeEvents(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['event'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer)


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer)


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['tracks'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['tracks'])


def leastMaxElements(analyzer):

    leastList = []

    i = lt.size(analyzer['event'])
    while i > lt.size(analyzer['event']) - 5:
        leastList.append(lt.getElement(analyzer['event'], i))
        i -= 1

    greaterList = []

    i = 1
    while i <= 5:
        greaterList.append(lt.getElement(analyzer['event'], i))
        i += 1

    return (leastList, greaterList)


def getsize(lista):
    '''
    Funcion que saca que size de una lista de listas de eventos
    '''
    eventsq = 0
    iterator = ite.newIterator(lista)
    while ite.hasNext(iterator):
        eventslist = ite.next(iterator)
        eventsq += lt.size(eventslist['lstevent'])
    return eventsq


def sortgenres(table):
    if lt.isEmpty(table):
        newlist = 0
    else:
        newlist = qs.sort(table, cmpGenresByreps)
    return newlist


def sortreq5(lista):
    if lt.isEmpty(lista):
        lt.newList = 0
    else:
        newlist = she.sort(lista, cmpHashtagbyGenres)
    return newlist

# ==============================
# Funciones de comparacion
# ==============================


def cmpGenresByreps(event1, event2):
    return (event1[1] > event2[1])


def cmpHashtagbyGenres(event1, event2):
    return (event1[1] > event2[1])
