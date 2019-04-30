#!/usr/bin/env python
# 
# Script para generar la tabla con los deportes y los torneos disponibles.

import json
import codecs
import challonge
import pprint 

# Conexion con Challonge
# TODO: check conexion con challonge.
f=open("../data/challonge_credentials","r")
lines=f.readlines()
username=lines[0]
password=lines[1]
f.close()
challonge.set_credentials(username, password)

for t in challonge.tournaments.index():
    print ("Borrando torneo " + str(t['id']) + ": " + t['name'])
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(t)
    challonge.tournaments.destroy(t["id"])
