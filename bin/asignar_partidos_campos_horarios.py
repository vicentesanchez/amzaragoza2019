#!/usr/bin/env python
# 
# Script para asignar partidos, campos y horarios

import sys
import json
import codecs
import challonge
import pprint

fich_data = '../data/data_am2019.json'
fich_output0 = '../data/_partidos_raw.txt'
fich_output1 = '../data/_partidos_ord.txt'
fich_output2 = '../data/_cuadrante.txt'
fich_output3 = '../www/_cuadrante.html'

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

output_partidos_raw = open(fich_output0, mode='w', encoding="utf-8")
output_partidos_ord = open(fich_output1, mode='w', encoding="utf-8")
output_cuadrante = open(fich_output2, mode='w', encoding="utf-8")
f = open(fich_output3, mode='w', encoding="utf-8")

# Creamos primero el cuadrante completo de campos y horarios sin asignación de partidos
print ("Generamos cuadrante vacio.")
cuadrante = {}
for deporte in data:
    if data[deporte]["generar_torneo"] == "Y":
        categorias = data[deporte]['categorias']
        campos = data[deporte]['campos']
        horarios = data[deporte]['horarios']

        cuadrante[deporte] = {}
        for hora in horarios:
            cuadrante[deporte][hora] = {}
            cuadrante[deporte][hora]['partidos'] = []
            for campo in campos:
                cuadrante[deporte][hora][campo] = {'libre':True,'torneo':'','partido':'','color':''}

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(cuadrante)

sys.stdout.write ("Obteniendo la lista de partidos")
sys.stdout.flush() 

# Sacamos la lista completa de partidos
partidos_raw = {}
total_partidos_raw = {}
for deporte in data:
    total_partidos_raw[deporte] = 0
    if data[deporte]["generar_torneo"] == "Y":
        categorias = data[deporte]['categorias']
        
        partidos_raw[deporte] = {}
        for torneo in categorias:
            if len(data[deporte]['categorias'][torneo]['equipos']) < 2: break
            url = "amz2019_" + torneo
            url = url.replace("+", "")
            ps = challonge.matches.index(url)
            partidos_raw[deporte][torneo]=[]
            for p in ps:
                if p['optional']==False:
                    partidos_raw[deporte][torneo].append(p)
                    total_partidos_raw[deporte] = total_partidos_raw[deporte] + 1
                    log = deporte + " " + torneo + " " + str(p["id"]) + " Partido: " + str(p['suggested-play-order']) + " Ronda: " +  str(p['round']) + " Pre: " + str(p['player1-prereq-match-id']) + " / " + str(p['player2-prereq-match-id']) 
                    output_partidos_raw.write(log + "\n")
                    sys.stdout.write('.')
                    sys.stdout.flush()  
print ("Ok")

total_todos_deportes_raw = 0
for deporte in data: 
    print ("Total partidos (sin ordenar) de " + deporte + ": " + str(total_partidos_raw[deporte]))
    total_todos_deportes_raw = total_todos_deportes_raw + total_partidos_raw[deporte]
print ("Total TODOS partidos (sin ordenar): " + str(total_todos_deportes_raw))

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(partidos_raw)

# Ordenamos los torneos por numero de partidos para empezar luego por los torneos con mas partidos.
torneo_temp = {}
torneo_ord = {}
for deporte in data:
    if data[deporte]["generar_torneo"] == "Y":
        categorias = data[deporte]['categorias']
        torneo_temp[deporte] = {}
        for torneo in categorias:
            l = len(data[deporte]['categorias'][torneo]['equipos'])
            torneo_temp[deporte][torneo] = l
            t = sorted(torneo_temp[deporte].items(), key=lambda x: x[1], reverse = True)
            torneo_ord[deporte] = [item[0] for item in t]

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(torneo_ord)

# ñapa: ponemos el torneo con menos equipos el primero
#for deporte in data:
#    if data[deporte]["generar_torneo"] == "Y":
#        t = torneo_ord[deporte].pop(-1)
#        torneo_ord[deporte].insert(0, t)

# ñapa2: a mano para ajustar
torneo_ord['Futbol'] = ['FUTBOL_FEM_2E+', 'FUTBOL_6P1E', 'FUTBOL_MAS_4E+', 'FUTBOL_4P5P', 'FUTBOL_MAS_2E3E' ]
torneo_ord['Baloncesto'] = ['BASKET_FEM_6P1E', 'BASKET_MAS_2E+']
torneo_ord['Minibasket'] = ['MINI_MAS_4P5P','MINI_FEM_4P5P', 'MINI_MAS_6P1E']
torneo_ord['Balonmano'] = ['BALONMANO_1P', 'BALONMANO_3P', 'BALONMANO_2P']

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(torneo_ord)

# Ordenamos los partidos de los torneos por orden
sys.stdout.write ("Ordenamos la lista de partidos")
sys.stdout.flush() 

partidos_por_orden = {}
total_todos_deportes_por_orden = 0

for deporte in data:
    if data[deporte]["generar_torneo"] == "Y":
        partidos_por_orden[deporte] = {}
        for torneo in torneo_ord[deporte]:
            partidos_por_orden[deporte][torneo] = sorted(partidos_raw[deporte][torneo], key=lambda item: item['suggested-play-order'])
            for p in partidos_por_orden[deporte][torneo]:
                total_todos_deportes_por_orden = total_todos_deportes_por_orden + 1
                log = deporte + " " + torneo + " " + str(p["id"]) + " Partido: " + str(p['suggested-play-order']) + " Ronda: " +  str(p['round']) + " Pre: " + str(p['player1-prereq-match-id']) + " / " + str(p['player2-prereq-match-id']) 
                output_partidos_ord.write(log + "\n")
                sys.stdout.write('.')
                sys.stdout.flush() 
#            for p in partidos_raw[deporte][torneo]:
##                partidos_por_orden[deporte][p["suggested-play-order"]] = p
#                total_todos_deportes_por_orden = total_todos_deportes_por_orden + 1
print ("Ok")
print ("Total TODOS partidos ordenados: " + str(total_todos_deportes_por_orden))

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(partidos_por_orden)

# Asignacion de horarios:
# - Nos llegan los partidos ordenados y con los torneos mas masivos primero.
# - Distribuimos un torneo completo, empezando por los mas grandes.
# - Asignamos partidos mientras podamos e intentamos que ningún equipo juego dos partidos seguidos.
# NOTA: codigo muy ineficiente

sys.stdout.write('Asignando partidos a cuadrantes')
sys.stdout.flush()
total_partidos_asignados_cuadrante = 0

for deporte in data:
    if data[deporte]["generar_torneo"] == "Y":
        campos = data[deporte]['campos']
        horarios = data[deporte]['horarios']
        for torneo in torneo_ord[deporte]:
            ultima_hora_asignada = data[deporte]['horarios'][0]
            for p in partidos_por_orden[deporte][torneo]:

                asignado = False
                #partidos_hora = []
                #for hora in horarios:
                    #print (partidos_hora)
                    #partidos_hora_antes = partidos_hora
                    #partidos_hora = []
                hora_previa = data[deporte]['horarios'][-1]
                for hora in horarios:
                    #print (hora + " " + ultima_hora_asignada + " " + str(horarios.index(hora)) + " " +
                    #       str(horarios.index(ultima_hora_asignada)))
                    if horarios.index(hora) >= horarios.index(ultima_hora_asignada):
                        for campo in campos:
                            #if (asignado == True):
                            #    print (campo + " " + hora + " " + hora_previa + " " + 
                            #       str(cuadrante[deporte][hora]['partidos']) + str(asignado) +
                            #       " " + str(cuadrante[deporte][hora_previa]['partidos']) + " " +
                            #        str(p['player1-prereq-match-id']) + " " + str(p['player2-prereq-match-id']))

                            if ((asignado == False) 
                                    & (cuadrante[deporte][hora][campo]["libre"] == True) 
                                    & (not p['player1-prereq-match-id'] in cuadrante[deporte][hora]['partidos'])
                                    & (not p['player2-prereq-match-id'] in cuadrante[deporte][hora]['partidos'])
                                    & (not p['player1-prereq-match-id'] in cuadrante[deporte][hora_previa]['partidos'])
                                    & (not p['player2-prereq-match-id'] in cuadrante[deporte][hora_previa]['partidos'])
                                    ):
                                ultima_hora_asignada = hora
                                #print (str(p['id']) + hora + " " + campo + " " + hora_previa + " " +
                                #    str(cuadrante[deporte][hora]['partidos']) + str(asignado) + " " + 
                                #    str(cuadrante[deporte][hora_previa]['partidos']) + " " +
                                #    str(p['player1-prereq-match-id']) + " " + str(p['player2-prereq-match-id']))

                                #partidos_hora.append(p['id'])
                                cuadrante[deporte][hora]['partidos'].append(p['id'])
                                cuadrante[deporte][hora][campo]["torneo"] = torneo 
                                cuadrante[deporte][hora][campo]["partido"] = str(p['suggested-play-order']) 
                                cuadrante[deporte][hora][campo]["color"] = data[deporte]['categorias'][torneo]['color']
                                cuadrante[deporte][hora][campo]["libre"] = False
                                total_partidos_asignados_cuadrante = total_partidos_asignados_cuadrante + 1
                                asignado = True 
                                sys.stdout.write('.')
                                sys.stdout.flush()  
                                log = deporte + " " + hora + " " + campo + " " + str(p['id']) + " " + torneo + " " + str(p['round']) + " " + str(p['suggested-play-order'])
                                output_cuadrante.write(log + "\n")
                    hora_previa = hora

print ("Ok")
print ("Total partidos asignados a cuadrantes : " + str(total_partidos_asignados_cuadrante))

# Generamos los cuadrantes en HTML

# Por cada deporte generamos una tabla con dos columnas: codigo torneo, descripción del torneo.
for deporte in data:
    if data[deporte]["generar_torneo"] == "Y":
        categorias = data[deporte]['categorias']
        campos = data[deporte]['campos']
        horarios = data[deporte]['horarios']

        f.write ('<div class="box">\n')
        f.write ('<h2 id="content">' + deporte + '</h2>\n')
        # Imprimimos cabecera
        f.write ('<div class="table-wrapper">\n')
        f.write ('    <table>\n')
        f.write ('        <thead>\n')
        f.write ('            <tr>\n')
        f.write ('                <th>Hora</th>\n')
    
        for campo in campos:
            f.write ('                <th>' + campo + '</th>\n')
        f.write ('            </tr>\n')
        f.write ('        </thead>\n')
        # Imprimimos el cuerpo
        f.write ('        <tbody>\n')  
    
        for hora in horarios:
            f.write ('            <tr>\n')
            f.write ('                <td>' + hora + '</td>\n')
            for campo in campos:
                color = cuadrante[deporte][hora][campo]["color"]
                f.write ('                <th><font size="1" color="' + color + '">' + cuadrante[deporte][hora][campo]["torneo"] + " - " + cuadrante[deporte][hora][campo]["partido"] + '</font></th>\n')
            f.write ('            </tr>\n')
        f.write ('        </tbody>\n')
        f.write ('    </table>\n')
        f.write ('</div>\n')
        f.write ('</div>\n')
               
# Imprimimos footer
f.write ('        </tbody>\n')
f.write ('    </table>\n')
f.write ('</div>\n')
