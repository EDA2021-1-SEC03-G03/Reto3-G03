"""
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

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todas las pistas
    Se crean indices (Maps) por los siguientes criterios:
    -track_id

    Retorna el analizador inicializado.
    """
    analyzer = {'event': None,
                'idIndex': None,
                'instrumentalness': None,
                'acousticness': None,
                'liveness':  None,
                'speechiness': None,
                'energy': None,
                'danceability': None,
                'valence': None
                }
    # Cambiar el nombre porque son eventos de escucha

    analyzer['event'] = lt.newList('ARRAY_LIST')

    analyzer['idIndex'] = om.newMap(omaptype='RBT',
                                    comparefunction=compareIds)

    analyzer['instrumentalness'] = om.newMap(omaptype='RBT',
                                             comparefunction=compareValue)

    analyzer['acousticness'] = om.newMap(omaptype='RBT',
                                         comparefunction=compareValue)

    analyzer['liveness'] = om.newMap(omaptype='RBT',
                                     comparefunction=compareValue)

    analyzer['speechiness'] = om.newMap(omaptype='RBT',
                                        comparefunction=compareValue)

    analyzer['energy'] = om.newMap(omaptype='RBT',
                                   comparefunction=compareValue)

    analyzer['danceability'] = om.newMap(omaptype='RBT',
                                         comparefunction=compareValue)

    analyzer['valence'] = om.newMap(omaptype='RBT',
                                    comparefunction=compareValue)

    return analyzer


# Funciones para agregar informacion al catalogo


def addEvent(analyzer, event):
    """
    """
    lt.addLast(analyzer['event'], event)
    updateIdIndex(analyzer['idIndex'], event)
    updateContCara(analyzer, event)
    return analyzer


def updateIdIndex(maps, event):
    """
    Se toma El track_id de cada evento y se adiciona al map
    . Si el track_id del evento ya esta en el arbol, se adiciona
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


def updateContCara(maps, event):
    '''
    Actualiza los arboles de cada una de las carateristicas de
    contenido. Agrega una lista con todos los eventos de escucha
    al arbol dependiendo del valor que estos tienen en esa carateristica.
    '''
    # Cada una de las caraccteristicas de contenido es un arbol

    caracteristics = ['instrumentalness', 'acousticness',
                      'liveness', 'speechiness', 'energy',
                      'danceability', 'valence']
    for i in caracteristics:
        entry = om.get(maps[i], event[i])

        if entry is None:
            datantry = newDataEntry(event)
            om.put(maps[i], event[i], datantry)
        else:
            datantry = me.getValue(entry)
        addEntry(datantry, event)
    return maps


def addEntry(maps, event):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = maps['lstevent']
    lt.addLast(lst, event)


def newDataEntry(event):
    """
    Crea una entrada en el indice por track_id, es decir en el arbol
    binario.
    """
    entry = {'lstevent': None}

    entry['lstevent'] = lt.newList('ARRAY_LIST')
    return entry


def caracterizeReproductions(maps, characteristic, keylo, keyhi):
    '''
    Consulta los eventos de escucho dados una caracteristica de
    contenido y un rango de valor. Retorna la cantidad de eventos
    y la cantida de artistas unicos que cumplen las caracteristicas
    pasadas por el usuario.
    '''
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
        # Se suman la cantidad de eventos para darle la informacion al usuario
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


def req2():
    return None


def studyMusic(maps, ikeylo, ikeyhi, tkelo, tkeyhi):
    '''
    Busca dentro del mapa de instrumentalness, en un rango
    especificado por el usuario, los eventos con una pista
    unica que cumplen el rango de tempo para estudiar.
    '''
    eventslist = om.values(maps['instrumentalness'], ikeylo, ikeyhi)
    return eventslist

# ==============================
# Funciones de consulta
# ==============================


def sizeEvents(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['event'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['idIndex'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['idIndex'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['idIndex'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['idIndex'])


def leastMaxElements(analyzer):

    leastList = []

    i = lt.size(analyzer['event'])
    while i > lt.size(analyzer['event']) - 5:
        leastList.append(lt.getElement(analyzer['event'], i))
        i -= 1

    greaterList = []

    i = 0
    while i < 5:
        greaterList.append(lt.getElement(analyzer['event'], i))
        i += 1

    return (leastList, greaterList)


# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos id's de los eventos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareValue(value1, value2):
    """
    Compara dos valores del evento segun la
    caracteristica de contenido
    """
    if (value1 == value2):
        return 0
    elif value1 > value2:
        return 1
    else:
        return -1
