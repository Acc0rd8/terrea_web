from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('email, username, password, status_code', [
    ('test1@example.com', 'test1', 'test1', 200), #valid registration
    ('test1@example.com', 'test2', 'test2', 409), #email already taken
    ('test2@example.com', 'test1', 'test1', 409), #username is already taken
    ('test3', 'test3', 'test3', 422) #email is incorrect
])
async def test_register_user(ac: AsyncClient, email, username, password, status_code):
    response = await ac.post('/profile/register', json={
        'email': email,
        'username': username,
        'password': password
    })
    
    assert response.status_code == status_code