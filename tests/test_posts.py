import pytest

@pytest.mark.asyncio
async def test_create_post(client):    
    login = await client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "admin123",
        },
    )
    token = login.json()["access_token"]
    
    category_response = await client.post(
        "/categories/",
        json={
            "name": "TestCat",
            "description": "Desc",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    category_id = category_response.json()["id"]
    
    response = await client.post(
        "/posts/",
        json={
            "title": "Test Post",
            "content": "Content",
            "category_id": category_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code in (200, 201)