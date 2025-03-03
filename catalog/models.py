from django.db import models

class Product(models.Model):
    nom = models.CharField(max_length=100)
    descripcio = models.CharField(max_length=1000)
    preu = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.CharField(max_length=100)
    imatge = models.CharField(max_length=500)

