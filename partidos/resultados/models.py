from django.db import models

# Create your models here.

class Equipo(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    
class Resultado(models.Model):
    jornada             =   models.IntegerField()
    local               =   models.ForeignKey(Equipo, related_name="local")
    visitante           =   models.ForeignKey(Equipo, related_name="visitante")
    goles_local         =   models.IntegerField()
    goles_visitante     =   models.IntegerField()