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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadData(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = cf.data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        model.addEvent(analyzer, event)


def loadData2(analyzer, files2):
    '''
    Carga los datos del CSV de hastags en el modelo
    '''
    files = cf.data_dir + files2
    input_file = csv.DictReader(open(files, encoding="utf-8"),
                                delimiter=",")
    for hashtags in input_file:
        model.updateHashtag(analyzer, hashtags)


def loadData3(analyzer, files3):
    '''
    Carga los datos del CSV de hastags en el modelo
    '''
    files = cf.data_dir + files3
    input_file = csv.DictReader(open(files, encoding="utf-8"),
                                delimiter=",")
    for sentiment in input_file:
        model.updatevader(analyzer, sentiment)
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def sizeEvents(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.sizeEvents(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def leastMaxElements(analyzer):
    """
    La mayor llave del arbol
    """
    return model.leastMaxElements(analyzer)


def caracterizeRep(maps, characteristic, keylo, keyhi):
    '''
    Eventos de escucha por categoria
    '''
    return model.caracterizeReproductions(maps, characteristic, keylo, keyhi)


def partyMusic(maps, keylo1, keyhi1, keylo2, keyhi2):
    '''
    Musica para irse de farra
    '''
    return model.partyMusic(maps, keylo1, keyhi1, keylo2, keyhi2)


def studyMusic(maps, keylo1, keyhi1, keylo2, keyhi2):
    '''
    Musica para estudiar
    '''
    return model.studyMusic(maps, keylo1, keyhi1, keylo2, keyhi2)


def reggae(maps):
    '''
    Eventos de reggea
    '''
    return model.reggae(maps)


def down(maps):
    '''
    Eventos de Down-tempo
    '''
    return model.down(maps)


def chill(maps):
    '''
    Eventos de Chill-out
    '''
    return model.chill(maps)


def hiphop(maps):
    '''
    Eventos de Hip-hop
    '''
    return model.hiphop(maps)


def jazzfunk(maps):
    '''
    Eventos de Jazz and funk
    '''
    return model.jazzfunk(maps)


def pop(maps):
    '''
    Eventos de Pop
    '''
    return model.pop(maps)


def ryb(maps):
    '''
    Eventos de R&B
    '''
    return model.ryb(maps)


def rock(maps):
    '''
    Eventos de Rock
    '''
    return model.rock(maps)


def metal(maps):
    '''
    Eventos de Metal
    '''
    return model.metal(maps)


def musicInTime(maps, time1, time2):
    '''
    Musica en un rango de tiempo determinado
    '''
    return model.musicInTime(maps, time1, time2)


def getgenres(maps):
    '''
    Tabla de hash con los generos y sus reproducciones
    '''
    return model.getgenres(maps)
