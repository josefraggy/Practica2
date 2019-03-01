# Programa que lee notas de un csv, las convierte a frecuencia y
# las reproduce como senial utilizando la libreria PyAudio
# la cancion es: Minuet in G Major.
#
# Se sacaron las notas del piano de este video
# https://www.youtube.com/watch?time_continue=30&v=ssbGk-hbk9A
# Se saco la idea de como reproducir una nota en frecuencia de este link
# https://askubuntu.com/questions/202355/how-to-play-a-fixed-frequency-sound-using-python
#
# @author: Jose Fraggy y Pablo Viramontes
# @since: 28 de febrero de 2019
# @version: 1.1
from __future__ import division #Avoid division problems in Python 2
import math
import csv
from pyaudio import PyAudio

# TODO: Codigo Modular, optimizar codigo.

# Abrimos el canal del audio
calidad = 16000 # number of fps/frameset.
p = PyAudio()
stream = p.open(
    format = p.get_format_from_width(1),
    channels = 1,
    rate = calidad,
    output = True,
    )
# Declaramos los saltos que hay entre La y las otras notas.
natural = {'Do':-9, 'Re':-7, 'Mi':-5, 'Fa':-4, 'Sol':-2, 'La':0, 'Si':2, 'C':-9, 'D':-7, 'E':-5, 'F':-4, 'G':-2, 'A':0, 'B':2}
sostenido = {'Do':-8, 'Re':-6, 'Fa':-4, 'Sol':-3, 'La':1, 'C':-8, 'D':-6, 'F':-4, 'G':-3, 'A':1}
bemol = {'Re':-8, 'Mi':-6, 'Sol':-4, 'La':-3, 'Si':1, 'D':-8, 'E':-6, 'G':-4, 'A':-3, 'B':1}

# Variables para calcular la frecuencia de la nota
nota = ''
accidente = ''
numero_octava = 0 #num nota
duracion = 0 #segundos
count = 0
reference = 0
# Hacemos la repeticion
for count in range (0, 2):
    with open('bach2.txt') as csvarchivo:
        entrada = csv.DictReader(csvarchivo)
        for head in entrada:
            reference = int(head['bloque'])
            if (count == reference) or (count+1 == reference):
                nota = head['nombre_nota']
                accidente = head['accidente']
                numero_octava = int(head['numero_octava'])
                duracion = int(head['duracion'])

                # Buscamos los pasos que hay entre nota dependiendo del accidente
                if accidente == 'sostenido':
                    for i in sostenido.keys():
                        if nota == i:
                            separacion = sostenido[i]
                elif accidente == 'bemol':
                    for i in bemol.keys():
                        if nota == i:
                            separacion = bemol[i]
                else:
                    for i in natural.keys():
                        if nota == i:
                            separacion = natural[i]

                pasos = separacion + ((-1 * (4 - numero_octava)) * 12)
                frecuencia = 440 * (2 ** (1/12)) ** pasos # Formula de la Frecuencia
                muestras = int(calidad * duracion/4)
                signal = ''

                for x in xrange(muestras):
                   signal += chr(int(math.sin(x / ((calidad / frecuencia) / math.pi)) * 127 + 128))
                # Convertimos la nota en una senial y la reproducimos
                stream.write(signal)
# Cerramos el canal de audio
stream.stop_stream()
stream.close()
p.terminate()
