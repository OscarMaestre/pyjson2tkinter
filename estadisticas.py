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




def get_probabilidades(lista_valores):
    cantidad_valores = len(lista_valores)
    
    suma=0
    for valor in lista_valores:
        suma += valor
    
    lista_probabilidades=[]
    for valor in lista_valores:
        probabilidad = round(valor/suma, 2)
        lista_probabilidades.append(probabilidad)
        
    return lista_probabilidades


def get_puntuacion(estadisticas_1, estadisticas_2):
    puntos_victoria_local=0
    puntos_victoria_visitante=0
    if estadisticas_1.victorias_local>estadisticas_2.victorias_local:
        puntos_victoria_local+=1
    else:
        puntos_victoria_visitante+=1
        
    if estadisticas_1.derrotas_local>estadisticas_2.derrotas_local:
        puntos_victoria_visitante+=1
    else:
        puntos_victoria_local+=1
        
    if estadisticas_1.victorias_totales>estadisticas_2.victorias_totales:
        puntos_victoria_local+=1
    else:
        puntos_victoria_visitante+=1
        
    if estadisticas_1.derrotas_totales>estadisticas_2.derrotas_totales:
        puntos_victoria_visitante+=1
    else:
        puntos_victoria_local+=1
        
    
    
    return (puntos_victoria_local, puntos_victoria_visitante)

def mostrar_pendientes():
        
    
    
    partidos_pendientes=PartidoPendiente.objects.all()
    lista_estadisticas=[]
    contexto={}
    for p in partidos_pendientes:
        
        equipo_local=str(p.local)
        equipo_visitante=str(p.visitante)
        estadisticas_1=Victorias.objects.get(pk=equipo_local)
        estadisticas_2=Victorias.objects.get(pk=equipo_visitante)
        
        probabilidades_local=get_probabilidades(
            [
                estadisticas_1.victorias_local      ,
                estadisticas_1.empates_local        ,
                estadisticas_1.derrotas_local
            ]
        )
        
        probabilidades_visitante=get_probabilidades(
            [
                estadisticas_2.victorias_visitante      ,
                estadisticas_2.empates_visitante        ,
                estadisticas_2.derrotas_visitante
            ]
        )
        
        probabilidades_local_total=get_probabilidades(
            [
                estadisticas_1.victorias_totales      ,
                estadisticas_1.empates_totales        ,
                estadisticas_1.derrotas_totales
            ]
        )
        
        probabilidades_visitante_total=get_probabilidades(
            [
                estadisticas_2.victorias_totales      ,
                estadisticas_2.empates_totales        ,
                estadisticas_2.derrotas_totales
            ]
        )
        
        
        
        
        (puntos_victoria_local,puntos_victoria_visitante)=get_puntuacion(estadisticas_1, estadisticas_2)
        
        tupla=(estadisticas_1, estadisticas_2,
               probabilidades_local, probabilidades_visitante,
               probabilidades_local_total, probabilidades_visitante_total,
               puntos_victoria_local, puntos_victoria_visitante)
        
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
