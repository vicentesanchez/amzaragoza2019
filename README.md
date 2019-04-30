# amzaragoza2019 dfgsdfgds

Generador de páginas información y de torneos para Accion Marianista Zaragoza 2019

## Descripción

Colección de scripts y plantillas de páginas HTML para generar los torneos de Acción Marianista en Zaragoza.
Básicamente:
* Se configuran los deportes, equipos, horarios y campos en un sólo fichero JSON
* A partir de ese fichero se generan las páginas estáticas HTML, que luego subiremos a algún cloud público.
* Y se generan scripts que actuan sobre el servicio de torneos "Challonge" para la generación de los torneos y partidos.
* A partir de los partidos de "Challonge" se generan finalmente páginas HTML estáticas con los horarios y campos de los partidos.

## Histórico de versiones

* 0.1: Versión inicial

## Instrucciones

### Dependencias previas.

* Servicio para alojamiento de páginas HTML estáticas y dominio DNS. Ejemplo: Google Cloud
* Para la generación de torneos se usa la aplicación Challonge [challonge](https://challonge.com). Se requiere usuario en este servicio.
* Para la ejecución de scripts de python es necesaria la librería "pychallonge".

### Instrucciones

* Para la fase de inscripciones, simplemente publicamos los HTML de información:
    * www/index.html: página principal
    * www/informacion.html: información sobre Accion Marianista
    * www/inscripciones.html: información sobre dónde realizar las inscripciones
    * www/torneos.html: IMPORTANTE: usamos "torneos.CERRADO.html" porque no tenemos la información todavía de torneos y equipos.
    * www/horarios.html: IMPORTANTE: usamos "horarios.CERRADO.html" porque no tenemos la información todavía de partidos.

* Una vez cerrado el plazo de inscripción:
    * Deberemos completar de forma correcta el fichero "data/data_am2019.json" con torneos, campos, horarios y equipos.
    * Deberemos tener el usuario y password de la cuenta de challonge en "data/challonge_credentials"
    * Generamos los torneos en challonge con "generar_torneos_CHALLONGE.py"
        * Para borrar todos los torneos: "borrar_torneos_CHALLONGE.py"
    * Asignamos partidos a campos y horarios: "asignar_partidos_campos_horarios.py"
    * Genermos la lista de torneos en HTML: "generar_torneos_HTML.py"
    * Cambiamos:
        * torneos.ABIERTO.html por torneos.html
        * horarios.ABIERTO.html por horarios.html
    * publicamos los html generados por los scripts y los modificados.




