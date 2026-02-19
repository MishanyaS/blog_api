import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "user@test.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    
    login = await client.post(
        "/auth/login",
        data={
            "username": "user@test.com",
            "password": "password123",
        }
    )
    
    assert login.status_code == 200
    tokens = login.json()
    assert "access_token" in tokens