from locust import HttpUser, task, between
from decouple import config

class InventarioUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        response = self.client.post('/api/token/', json={
            'username': config('LOCUST_USER'),
            'password': config('LOCUST_PASSWORD')
        })
        self.token = response.json()['access']

    @task(3)
    def listar_productos(self):
        self.client.get('/api/productos/', headers={
            'Authorization': f'Bearer {self.token}'
        })

    @task(2)
    def listar_categorias(self):
        self.client.get('/api/categorias/', headers={
            'Authorization': f'Bearer {self.token}'
        })

    @task(1)
    def estadisticas(self):
        self.client.get('/api/estadisticas/', headers={
            'Authorization': f'Bearer {self.token}'
        })