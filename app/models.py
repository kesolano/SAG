from django.db import models

# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    calificador_riesgo = models.CharField(max_length=10)
    tipo_riesgo = models.CharField(max_length=255)
    ponderacion_calificacion = models.FloatField()
    alto_riesgo = models.BooleanField()
