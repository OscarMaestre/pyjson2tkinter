#!/usr/bin/python3
#coding=utf-8

from utilidades.ficheros.GestorFicheros import GestorFicheros
import bs4

url_base="http://www.mundodeportivo.com/resultados/futbol/laliga/jornada-{0}.html"
fichero_base="resultados/fichero{0}.html"
gf=GestorFicheros()

for num in range(1, 36):
    url=url_base.format(num)
    fichero=fichero_base.format(num)
    if not gf.existe_fichero(fichero):
        gf.descargar_fichero(url, fichero)
        
        
for num in range(1, 36):
    fichero=fichero_base.format(num)
    with open(fichero, "r") as fp:
        sopa=bs4.BeautifulSoup(fp, "lxml")
        base=sopa.find_all("div", "workingday-match-body")
        for resultado in base:
            nombre_equipos=resultado.find_all("a", "workingday-match-team" )
            resultados_equipos=resultado.find_all("span", "workingday-match-text")
            equipo_1=nombre_equipos[0].text.strip()
            equipo_2=nombre_equipos[1].text.strip()
            goles_equipo_1=resultados_equipos[0].text.strip()
            goles_equipo_2=resultados_equipos[1].text.strip()
            print (num, equipo_1, goles_equipo_1, equipo_2, goles_equipo_2)