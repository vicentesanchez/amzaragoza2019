#!/usr/bin/env python
# 
# Script para generar la tabla con los deportes y los torneos disponibles.

import json
import codecs

fich_data = '../data/data_am2019.json'
fich_output_CHALLONGE = '../www/_lista_torneos_CHALLONGE.html'

# Importamos el fichero con los datos generales
# TODO: check fichero y estructura del mismo.
json_data = open(fich_data, encoding='utf-8')
data = json.load(json_data)

f = open(fich_output_CHALLONGE, mode='w', encoding="utf-8")

# Generamos el HTML para los torneos
for deporte in data:
    if data[deporte]["generar_torneo"] == "Y":
        f.write ('<div class="box">\n')
        f.write ('  <h4 align=left id="content">' + deporte + '</h4>\n')
        if data[deporte]["generar_torneo"] == "Y":
            categorias = data[deporte]['categorias']
            for torneo in categorias:
                if len(data[deporte]['categorias'][torneo]['equipos']) < 2: break
                url = "amz2019_" + torneo
                f.write('    <font size="2"><a href="http://challonge.com/' + url.replace("+", "") +
                        '/module?show_standings=1&show_final_results=1" target="_blank" align="middle" class="button special">' + torneo + '</a></font>\n')
        f.write ('</div>\n')

