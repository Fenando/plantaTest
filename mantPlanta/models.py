from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Planta(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

class Area(models.Model):
    nombre = models.CharField(max_length=30)
    planta = models.ForeignKey(Planta, blank=True , null=True,)
    def __str__(self):
        return self.nombre

class Tipo(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

class Componente(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Informacion(models.Model):
    nombre = models.CharField(max_length=30)
    marca = models.CharField(max_length=30,blank=True, null=True)
    tension = models.IntegerField(blank=True, null=True)
    info = models.TextField(max_length=500,blank=True, null=True)
    imagen = models.ImageField(upload_to= "media",blank=True, null=True)
    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=30)
    tipo = models.ForeignKey(Tipo)
    area = models.ForeignKey(Area)
    info = models.ForeignKey(Informacion, blank=True , null=True,)


    imagen = models.ImageField(blank= True , null=True)
    componente = models.ManyToManyField(Componente,  blank=True)
    def __str__(self):
        return self.nombre


class Mantencion(models.Model):
    equipos = models.ForeignKey(Equipo)
    causa = models.TextField(max_length=500)
    fecha = models.DateField()
    realizada = models.BooleanField(default=False)
    aprobada = models.BooleanField(default=False)
    rechazada = models.BooleanField(default=False)
    fecha_aprec = models.DateField(null=True,blank=True)
    usuario = models.ForeignKey(User)
    solicitante = models.CharField(max_length=30)
    numero_ot = models.IntegerField()
    correo = models.EmailField()
    imagen = models.ImageField(upload_to='media/images/',null=True,blank=True)
    def __str__(self):
        return self.equipos.nombre

class Comentario(models.Model):
    comentario = models.TextField(max_length=200)
    mantencion = models.ForeignKey(Mantencion)
    fecha = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.comentario


class Acciones(models.Model):
    mantencion = models.ForeignKey(Mantencion)
    accion = models.TextField(max_length=500)
    fecha = models.DateField()
    usuario = models.ForeignKey(User)
    realizador = models.CharField(max_length=30)
    imagen = models.ImageField(upload_to='media/imagesReport/',null=True,blank=True)
    def __str__(self):
        return self.mantencion.equipos.nombre





