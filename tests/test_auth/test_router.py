import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from auth.schemas import UserCreate

from src.main import app


client = TestClient(app)


#UNIT_TESTS
def test_register_user():
    response = client.post('/auth/register', json={
        'username': 'mark',
        'email': 'mark@example.com',
        'password': 'admin'
    })
    assert response.status_code == 200
    assert response.json() == {'message': 'Вы успешно зарегистрированы'}
