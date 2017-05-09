#!/usr/bin/python3
#coding=utf-8

from utilidades.ficheros.GestorFicheros import GestorFicheros
import bs4
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("partidos")
configurador.activar_configuracion ("partidos.settings")
from resultados.models import Equipo, Resultado, PartidoPendiente
from django.db.transaction import atomic


url_base="http://www.mundodeportivo.com/resultados/futbol/laliga/jornada-{0}.html"
fichero_base="resultados/fichero{0}.html"
gf=GestorFicheros()


        
def procesar_ficheros(num):

    conjunto_equipos=set()
    conjunto_resultados=set()
    fichero=fichero_base.format(num)
    print("Procesando "+fichero)
    with open(fichero, "r") as fp:
        sopa=bs4.BeautifulSoup(fp, "lxml")
        base=sopa.find_all("div", "workingday-match-body")
        for resultado in base:
            nombre_equipos=resultado.find_all("a", "workingday-match-team" )
            resultados_equipos=resultado.find_all("span", "workingday-match-text")
            equipo_1=nombre_equipos[0].text.strip()
            equipo_2=nombre_equipos[1].text.strip()
            conjunto_equipos = conjunto_equipos ^ {equipo_1, equipo_2}
            goles_equipo_1=resultados_equipos[0].text.strip()
            goles_equipo_2=resultados_equipos[1].text.strip()
            resultado=(num, equipo_1, equipo_2, goles_equipo_1, goles_equipo_2)
            conjunto_resultados = conjunto_resultados ^ {resultado}
            print (num, equipo_1, goles_equipo_1, equipo_2, goles_equipo_2)
    return (conjunto_equipos, conjunto_resultados)

def cargar_datos():
    conjunto_equipos=set()
    conjunto_resultados=set()
    for num in range(1, 39):
        url=url_base.format(num)
        fichero=fichero_base.format(num)
        if not gf.existe_fichero(fichero):
            gf.descargar_fichero(url, fichero)
        (c_equipos, c_resultados)=procesar_ficheros(num)
        #print(c_equipos)
        conjunto_equipos = conjunto_equipos ^ c_equipos
        conjunto_resultados = conjunto_resultados ^ c_resultados
    with atomic():
        for equipo in conjunto_equipos:
            print (equipo)
            equipo=Equipo(nombre=equipo)
            equipo.save()
    with atomic():
        Resultado.objects.all().delete()
        PartidoPendiente.objects.all().delete()
        for resultado in conjunto_resultados:
            print (resultado)
            equipo_1=Equipo.objects.get(pk=resultado[1])
            equipo_2=Equipo.objects.get(pk=resultado[2])
            goles_local         =   resultado[3]
            goles_visitante     =   resultado[4]
            jornada             =   resultado[0]
            if goles_local=="-" and goles_visitante=="-":
                pendiente = PartidoPendiente(
                    jornada=jornada,
                    local=equipo_1, visitante=equipo_2  )
                pendiente.save()
            else:
                resultado   = Resultado (
                    jornada=jornada,
                    local=equipo_1, visitante=equipo_2,
                    goles_local = goles_local, goles_visitante=goles_visitante
                )
                resultado.save()
        
        
if __name__ == '__main__':
    cargar_datos()