from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from catalog.models import Product
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data)

    @action(detail=True, methods=['post'])
    def remove_product(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()

        return Response({"message": "Producto eliminado del carrito."})

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """Convierte el carrito en un pedido"""
        cart = self.get_object()
        if not cart.items.exists():
            return Response({"error": "El carrito está vacío."}, status=400)

        # Importamos aquí para evitar dependencia circular
        from orders.models import Order, OrderItem

        order = Order.objects.create(user=cart.user, total_price=0, status="pendiente")

        total_price = 0
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            total_price += item.product.price * item.quantity

        order.total_price = total_price
        order.save()

        cart.items.all().delete()  # Vaciamos el carrito

        return Response({"message": "Compra realizada con éxito.", "order_id": order.id})
