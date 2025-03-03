from django.db import models

class Payment(models.Model):
    numero_tarjeta = models.CharField(max_length=20)
    data_caducitat = models.DateField()
    CVC = models.CharField(max_length=3)
    estat_pagament = models.BooleanField(default=False)
