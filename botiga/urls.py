from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('cart.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('catalog.urls')),
    path('api/', include('payment.urls')),

]
