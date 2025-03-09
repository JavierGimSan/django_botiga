from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer
import re

def verificar_tarjeta(numero_tarjeta):
    pattern = re.compile(r'^\d{16}$')
    return pattern.match(numero_tarjeta)

def verificar_data_caducitat(data_caducitat):
    pattern = re.compile(r'^\d{2}/\d{2}$')
    return pattern.match(data_caducitat)

def validar_cvc(CVC):
    pattern = re.compile(r'^\d{3}$')
    return pattern.match(CVC)

@api_view(['POST'])
def pagar_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, estat='oberta')
    except ObjectDoesNotExist:
        return Response({"estat": "error", "missatge": "La comanda no existeix."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        dades = serializer.validated_data
        if not verificar_tarjeta(dades['numero_tarjeta']):
            return Response({"estat": "error", "missatge": "Número de tarjeta no valid."}, status=status.HTTP_400_BAD_REQUEST)
        if not verificar_data_caducitat(dades['data_caducitat']):
            return Response({"estat": "error", "missatge": "Fecha de caducidad no valida."}, status=status.HTTP_400_BAD_REQUEST)
        if not validar_cvc(dades['cvc']):
            return Response({"estat": "error", "missatge": "CVC no valid."}, status=status.HTTP_400_BAD_REQUEST)

        Payment.objects.create(
            order=order,
            numero_tarjeta=dades['numero_tarjeta'],
            data_caducitat=dades['data_caducitat'],
            cvc=dades['cvc']
        )

        order.estat = 'finalitzada'
        order.save()

        return Response({"estat": "éxit", "missatge": "Pagament fet correctament."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def consultar_estat_order(order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except ObjectDoesNotExist:
        return Response({"estat": "error", "missatge": "La comanda no existeix."}, status=status.HTTP_404_NOT_FOUND)

    estat = order.estat
    return Response({"estat": "éxit", "missatge": f"L'estat de la comanda és {estat}."}, status=status.HTTP_200_OK)
