from rest_framework.routers import DefaultRouter, path
from .views import ProductoViewSet, CategoriaViewSet, estadisticas

router = DefaultRouter()
router.register('productos', ProductoViewSet, basename='producto')
router.register('categorias', CategoriaViewSet, basename='categoria')

urlpatterns = router.urls + [
    path('estadisticas/', estadisticas),
]
