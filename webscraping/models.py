from django.db import models

# Create your models here.


class PlantType(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Planta(models.Model):
    nombre = models.CharField(max_length=50)
    nombre_desc = models.CharField(max_length=75)
    climatologia = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagenUrl = models.CharField(max_length=200)
    plantType = models.ManyToManyField(PlantType)

    def __str__(self):
        return self.nombre

    def get_plantType(self):
        return "\n".join([p.nombre for p in self.plantType.all()])


class Cuidado(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    tipoCuidado = models.CharField(max_length=50)
    instrucciones = models.TextField()

    def __str__(self):
        return self.tipoCuidado


class Enfermedad(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    sintomas = models.TextField()
    tratamiento = models.TextField()

    def __str__(self):
        return self.nombre


class Plaga(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    sintomas = models.TextField()
    tratamiento = models.TextField()

    def __str__(self):
        return self.nombre
