#!/usr/bin/env python
# 
# Script para generar la tabla con los deportes y los torneos disponibles.

import json
import codecs
import challonge

fich_data = '../data/data_am2019.json'
fich_output = '../data/_torneos.txt'

# Conexion con Challonge
# TODO: check conexion con challonge.
f=open("../data/challonge_credentials","r")
lines=f.readlines()
username=lines[0]
password=lines[1]
f.close()
challonge.set_credentials(username, password)

# Importamos el fichero con los datos generales
# TODO: check fichero y estructura del mismo.
json_data = open(fich_data, encoding='utf-8')
data = json.load(json_data)

output_torneos = open(fich_output, mode='w', encoding="utf-8")

# Por cada categoría de deporte generamos un torneo.
for deporte in data:
    if data[deporte]["generar_torneo"] == "Y":
        categorias = data[deporte]['categorias']
        for torneo in categorias:
            # Comprobamos un minimo de 2 equipos
            if len(data[deporte]['categorias'][torneo]['equipos']) < 2: break
            url = "amz2019_" + torneo
            t = challonge.tournaments.create(torneo, url.replace("+", ""), "double elimination")
            challonge.tournaments.update(t["id"],description=data[deporte]['categorias'][torneo]["descripcion"]) 
            challonge.tournaments.update(t["id"],grand_finals_modifier="skip")
            challonge.tournaments.update(t["id"],show_rounds="true")
            challonge.tournaments.update(t["id"],game_name=deporte)
            log = "id: " + str(t["id"]) + "\tDescription: " + torneo
            print (log)
            output_torneos.write(log)
            output_torneos.write("\t\t")
            
            # Añadimos los equipos
            for equipo in data[deporte]['categorias'][torneo]['equipos']:
                challonge.participants.create(t["id"],equipo)
                print ("-- Añadido equipo: " + equipo)
                output_torneos.write(" " + equipo)

            output_torneos.write("\n")
            
            # Arrancamos el torneo para generar los partidos
            challonge.tournaments.start(t["id"])
            print ("Abriendo torneo para generar partidos... ")
            #break
        #break

