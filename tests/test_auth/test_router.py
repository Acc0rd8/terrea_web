import pytest
from httpx import AsyncClient, ASGITransport
from auth.schemas import UserCreate

from src.main import app


async def test_register_user(user: UserCreate):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test', follow_redirects=True) as ac:
        response = await ac.post('/auth/register', json={
            'username': 'mark',
            'email': 'example1@gmail.com',
            'password': 'admin'
        })
        
        assert response.status_code == 200
        assert response.json() == {'message': 'Вы успешно зарегистрированы'}