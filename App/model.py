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
    analyzer = {'tracks': None,
                'idIndex': None
                }

    analyzer['tracks'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['idIndex'] = om.newMap(omaptype='RBT',
                                    comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo


def addTrack(analyzer, track):
    """
    """
    lt.addLast(analyzer['tracks'], track)
    updateIdIndex(analyzer['idIndex'], track)

    return analyzer


def updateIdIndex(maps, track):
    """
    Se toma El track id de cada track y se adiciona al map
    . Si el track ya esta en el arbol, se adiciona a su lista
    respectiva y se actualiza el index.

    Si no se encuentra creado un nodo para ese id en el arbol
    se crea y se actualiza el indice del id de las pistas.
    """
    trackId = track['track_id']
    entry = om.get(maps, trackId)
    if entry is None:
        datantry = newDataEntry(track)
        om.put(maps, trackId, datantry)
    else:
        datantry = me.getValue(entry)
    addIdIndex(datantry, track)
    return maps


def addIdIndex(datantry, track):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datantry['lsttracks']
    lt.addLast(lst, track)


def newDataEntry(track):
    """
    Crea una entrada en el indice por track_id, es decir en el arbol
    binario.
    """
    entry = {'lsttracks': None}

    entry['lsttracks'] = lt.newList('ARRAY_LIST')
    return entry


# ==============================
# Funciones de consulta
# ==============================


def sizeTracks(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['tracks'])


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

    i = lt.size(analyzer['tracks'])
    while i > lt.size(analyzer['tracks']) - 5:
        leastList.append(lt.getElement(analyzer['tracks'], i))
        i -= 1

    greaterList = []

    i = 0
    while i < 5:
        greaterList.append(lt.getElement(analyzer['tracks'], i))
        i += 1

    return (leastList, greaterList)

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
