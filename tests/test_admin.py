import pytest

@pytest.mark.asyncio
async def test_admin_create_category(client):
    login = await client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "admin123",
        },
    )
    
    token = login.json()["access_token"]
    
    response = await client.post(
        "/categories/",
        json={
            "name": "AdminCat",
            "description": "Admin",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200