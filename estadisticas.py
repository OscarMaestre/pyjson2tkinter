#!/usr/bin/env python3

from django.db.transaction import atomic

from utilidades.basedatos.Configurador import Configurador
configurador=Configurador ("partidos")
configurador.activar_configuracion ("partidos.settings")
from resultados.models import Equipo, Resultado, PartidoPendiente, Victorias



def generar_victorias_derrotas(equipos, resultados):
    for e in equipos:
        victorias_local     =   0
        empates_local       =   0
        derrotas_local      =   0
        
        victorias_visitante     =   0
        empates_visitante       =   0
        derrotas_visitante      =   0
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
        print (e, victorias_local, empates_local, derrotas_local,
               victorias_visitante, empates_visitante, derrotas_visitante)
                
if __name__ == '__main__':
    equipos     = Equipo.objects.all()
    resultados  = Resultado.objects.all()
    with atomic():
        generar_victorias_derrotas(equipos, resultados)

