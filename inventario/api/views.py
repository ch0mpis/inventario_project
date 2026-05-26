from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from inventario.models import Producto
from inventario.api.serializer import ProductoSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProductoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'marca', 'precio']