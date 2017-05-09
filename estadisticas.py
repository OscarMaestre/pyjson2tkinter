#!/usr/bin/env python3

from django.db.transaction import atomic
from django.template.loader import render_to_string

from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("partidos")
configurador.activar_configuracion ("partidos.settings")
from resultados.models import Equipo, Resultado, PartidoPendiente, Victorias
from tabulate import tabulate


def generar_victorias_derrotas(equipos, resultados):
    Victorias.objects.all().delete()
    for e in equipos:
        victorias_local     =   0
        empates_local       =   0
        derrotas_local      =   0
        
        victorias_visitante     =   0
        empates_visitante       =   0
        derrotas_visitante      =   0
        
        victorias_totales     =   0
        empates_totales       =   0
        derrotas_totales      =   0
        
        for r in resultados:
            #print("-"+r.local.nombre+"-", "-"+e.nombre+"-")
            if r.local.nombre==e.nombre:
                if r.goles_local>r.goles_visitante:
                    victorias_local+=1
                if r.goles_local==r.goles_visitante:
                    empates_local+=1
                if r.goles_local<r.goles_visitante:
                    derrotas_local+=1
            if r.visitante.nombre==e.nombre:
                if r.goles_visitante>r.goles_local:
                    victorias_visitante+=1
                if r.goles_visitante==r.goles_local:
                    empates_visitante+=1
                if r.goles_visitante<r.goles_local:
                    derrotas_visitante+=1
        #Fin del for
        victorias_totales = victorias_local + victorias_visitante
        empates_totales = empates_local + empates_visitante
        derrotas_totales = derrotas_local + derrotas_visitante
        estadistica=Victorias(
            equipo=e,
            victorias_local=victorias_local,
            empates_local=empates_local,
            derrotas_local=derrotas_local,
            
            victorias_visitante=victorias_visitante,
            empates_visitante=empates_visitante,
            derrotas_visitante=derrotas_visitante,
            
            victorias_totales=victorias_totales,
            empates_totales=empates_totales,
            derrotas_totales=derrotas_totales
            
            )
        
        estadistica.save()


def mostrar_pendientes():
    estadisticas=Victorias.objects.all()
    lista=[]
    cabeceras_estadisticas=["Equipo", "Vict tot", "Emp tot", "Derr tot",
                            "Vict loc", "Emp loc", "Derr loc",
                            ]
    for e in estadisticas:
        lista_resultado=[]
        lista_resultado.append(e.equipo, )
        lista_resultado.append(e.victorias_totales)
        lista_resultado.append(e.empates_totales)
        lista_resultado.append(e.derrotas_totales)
        lista_resultado.append(e.victorias_local)
        lista_resultado.append(e.empates_local)
        lista_resultado.append(e.derrotas_local)
        lista.append(lista_resultado)
    cad=tabulate(lista, headers=cabeceras_estadisticas)
    #print(cad)
    
    partidos_pendientes=PartidoPendiente.objects.all()
    lista_estadisticas=[]
    contexto={}
    for p in partidos_pendientes:
        equipo_local=str(p.local)
        equipo_visitante=str(p.visitante)
        estadisticas_1=Victorias.objects.get(pk=equipo_local)
        estadisticas_2=Victorias.objects.get(pk=equipo_visitante)
        tupla=(estadisticas_1, estadisticas_2)
        lista_estadisticas.append ( tupla )
    contexto["parejas_estadisticas"]=lista_estadisticas
    cad=render_to_string("resultados/estadisticas.html", contexto, None)
    print(cad)
if __name__ == '__main__':
    equipos     = Equipo.objects.all()
    resultados  = Resultado.objects.all()
    with atomic():
        generar_victorias_derrotas(equipos, resultados)
        mostrar_pendientes()
