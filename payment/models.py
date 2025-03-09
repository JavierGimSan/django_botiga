from django.db import models
from orders.models import Order

class Payment(models.Model):
    comanda = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    numero_tarjeta = models.CharField(max_length=20)
    data_caducitat = models.DateField()
    CVC = models.CharField(max_length=3)
    estat_pagament = models.BooleanField(default=False)

    def __str__(self):
        return f'Pagament {self.id} per la comanda {self.comanda.id}'
