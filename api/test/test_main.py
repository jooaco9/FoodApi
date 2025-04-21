from http.client import responses

from fastapi.testclient import TestClient
from api import app


client = TestClient(app)

# Primer test
def test_read_root():
    response = client.get("/")

    # Comprobaciones
    assert response.status_code == 200
    assert response.json() == {"Hola": "Jokin"}

# Test sobre endpoint ingredientId
def test_read_ingredient_id():
    response = client.get("/ingredientes/23")
    assert response.status_code == 200

# Test sobre endpoint ingredientId
def test_read_ingredient_id_not_found():
    response = client.get("/ingredientes/2300000")
    assert response.status_code == 404
    assert response.json() == {"error": "Ingrediente 2300000 no encontrado"}

# Test sobre post de ingrediente
def test_create_ingredient():
    response = client.post(
        url="/ingredientes/",
        headers={"Content-Type": "application/json"},
        json={
            "nombre": "Prueba",
            "calorias": 3,
            "carbohidratos": 0,
            "proteinas": 0,
            "grasas": 0,
            "fibra": 0
        }
    )

    assert response.status_code == 200