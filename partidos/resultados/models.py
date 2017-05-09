from django.db import models

# Create your models here.

class Equipo(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    
    def __str__(self):
        return self.nombre
    
class Resultado(models.Model):
    jornada             =   models.IntegerField()
    local               =   models.ForeignKey(Equipo, related_name="local")
    visitante           =   models.ForeignKey(Equipo, related_name="visitante")
    goles_local         =   models.IntegerField()
    goles_visitante     =   models.IntegerField()
    
    
class PartidoPendiente(models.Model):
    jornada             =   models.IntegerField()
    local               =   models.ForeignKey(Equipo, related_name="equipolocal")
    visitante           =   models.ForeignKey(Equipo, related_name="equipovisitante")
    
class Victorias(models.Model):
    equipo              =   models.ForeignKey(Equipo, primary_key=True)
    victorias_local     =   models.IntegerField()
    empates_local       =   models.IntegerField()
    derrotas_local      =   models.IntegerField()
    
    victorias_visitante     =   models.IntegerField()
    empates_visitante       =   models.IntegerField()
    derrotas_visitante      =   models.IntegerField()
    
    victorias_totales     =   models.IntegerField()
    empates_totales       =   models.IntegerField()
    derrotas_totales      =   models.IntegerField()
    