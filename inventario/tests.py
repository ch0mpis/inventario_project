import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from inventario.models import Producto, Categoria

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def usuario():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def token(api_client, usuario):
    response = api_client.post('/api/token/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    return response.data['access']

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