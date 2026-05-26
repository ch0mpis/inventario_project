from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from inventario.models import Producto, Categoria 
from inventario.api.serializer import ProductoSerializer, CategoriaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventario.models import Producto, Categoria
from django.db.models import Max, Min, Sum

class ProductoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'marca', 'precio']

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

@api_view(['GET'])
def estadisticas(request):
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    stock_total = Producto.objects.aggregate(Sum('cantidad_max'))['cantidad_max__sum'] or 0
    producto_mas_caro = Producto.objects.order_by('-precio').first()
    producto_mas_barato = Producto.objects.order_by('precio').first()

    return Response({
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'stock_total': stock_total,
        'producto_mas_caro': producto_mas_caro.nombre if producto_mas_caro else None,
        'producto_mas_barato': producto_mas_barato.nombre if producto_mas_barato else None,
    })