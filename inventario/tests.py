import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from inventario.models import Producto, Categoria

# ─── PRUEBAS DE UNIDAD ───

@pytest.fixture
def api_client():
    return APIClient()

# Fixtures para crear un usuario y obtener token de autenticación

@pytest.fixture
def usuario():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

# Fixture para obtener token de autenticación
@pytest.fixture
def token(api_client, usuario):
    response = api_client.post('/api/token/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    return response.data['access']

# Fixtures para crear datos de prueba

@pytest.mark.django_db
def test_listar_productos(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.get('/api/productos/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_crear_producto(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    data = {
        'nombre': 'Laptop HP',
        'descripcion': 'Laptop para oficina',
        'marca': 'HP',
        'cantidad_min': 5,
        'cantidad_max': 50,
        'precio': '2500.00'
    }
    response = api_client.post('/api/productos/', data)
    assert response.status_code == 201

# Prueba para crear categoría

@pytest.mark.django_db
def test_crear_categoria(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    data = {'nombre': 'Electronica', 'descripcion': 'Productos electronicos'}
    response = api_client.post('/api/categorias/', data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_estadisticas(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.get('/api/estadisticas/')
    assert response.status_code == 200

# ─── PRUEBAS DE INTEGRACIÓN ───

@pytest.mark.django_db
def test_flujo_completo_producto(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # 1. Crear producto
    data = {
        'nombre': 'Laptop HP',
        'descripcion': 'Laptop para oficina',
        'marca': 'HP',
        'cantidad_min': 5,
        'cantidad_max': 50,
        'precio': '2500.00'
    }
    response_crear = api_client.post('/api/productos/', data)
    assert response_crear.status_code == 201
    producto_id = response_crear.data['id']

    # 2. Verificar que quedó en la base de datos
    response_listar = api_client.get('/api/productos/')
    assert response_listar.data['count'] == 1

    # 3. Actualizar producto
    response_actualizar = api_client.put(f'/api/productos/{producto_id}/', {
        'nombre': 'Laptop Dell',
        'descripcion': 'Laptop actualizada',
        'marca': 'Dell',
        'cantidad_min': 3,
        'cantidad_max': 30,
        'precio': '3000.00'
    })
    assert response_actualizar.status_code == 200
    assert response_actualizar.data['nombre'] == 'Laptop Dell'

    # 4. Eliminar producto
    response_eliminar = api_client.delete(f'/api/productos/{producto_id}/')
    assert response_eliminar.status_code == 204

    # 5. Verificar que se eliminó
    response_final = api_client.get('/api/productos/')
    assert response_final.data['count'] == 0


@pytest.mark.django_db
def test_flujo_completo_categoria(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # 1. Crear categoría
    response_crear = api_client.post('/api/categorias/', {
        'nombre': 'Electrónica',
        'descripcion': 'Productos electrónicos'
    })
    assert response_crear.status_code == 201
    categoria_id = response_crear.data['id']

    # 2. Crear producto con esa categoría
    response_producto = api_client.post('/api/productos/', {
        'nombre': 'Mouse',
        'descripcion': 'Mouse inalámbrico',
        'marca': 'Logitech',
        'cantidad_min': 10,
        'cantidad_max': 100,
        'precio': '150.00',
        'categoria': categoria_id
    })
    assert response_producto.status_code == 201
    assert response_producto.data['categoria'] == categoria_id

    # 3. Verificar estadísticas
    response_stats = api_client.get('/api/estadisticas/')
    assert response_stats.status_code == 200
    assert response_stats.data['total_productos'] == 1
    assert response_stats.data['total_categorias'] == 1