from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['nom', 'descripcio', 'preu', 'stock', 'categoria', 'imatge']
