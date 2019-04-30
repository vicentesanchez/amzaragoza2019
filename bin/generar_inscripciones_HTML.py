#!/usr/bin/env python
# 
# Script para generar la tabla con los deportes y los torneos disponibles.

import json
import codecs

fich_data = '../data/data_am2019.json'
fich_output = '../www/_lista_torneos.html'

# Importamos el fichero con los datos generales
# TODO: check fichero y estructura del mismo.
json_data = open(fich_data, encoding='utf-8')
data = json.load(json_data)
f = codecs.open(fich_output, "w", "utf-8")

# Por cada deporte generamos una tabla con dos columnas: codigo torneo, descripción del torneo.
for deporte in data:
    f.write ('<div class="box">\n')
    f.write ('<h2 id="content">' + deporte + '</h2>\n')
    # Imprimimos cabecera
    f.write ('<div class="table-wrapper">\n')
    f.write ('    <table>\n')
    f.write ('        <thead>\n')
    f.write ('            <tr>\n')
    f.write ('                <th>Torneo</th>\n')
    f.write ('                <th>Descripción del torneo</th>\n')
    f.write ('            </tr>\n')
    f.write ('        </thead>\n')
    f.write ('        <tbody>\n')  
    categorias = data[deporte]['categorias']
    for torneo in categorias:
        f.write ('            <tr>\n')
        f.write ('                <td>' + torneo + '</td>\n')
        f.write ('                <td>' + data[deporte]['categorias'][torneo]['descripcion'] + '</td>\n')
        f.write ('            </tr>\n')
    f.write ('        </tbody>\n')
    f.write ('    </table>\n')
    f.write ('</div>\n')
    f.write ('</div>\n')
               
# Imprimimos footer
f.write ('        </tbody>\n')
f.write ('    </table>\n')
f.write ('</div>\n')