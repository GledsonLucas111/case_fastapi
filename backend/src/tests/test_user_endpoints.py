import pytest
from src.main import app  # importa o app FastAPI
from fastapi.testclient import TestClient

client = TestClient(app)
users = []

def test_create_user():
    user = {
        "name": "Teste",
        "email": "teste@example.com",
        "password": "12345",
        "role": "student",
        "registration": "12345"
    }
    response = client.post("/users", json=user)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    users.append(data["id"])
    
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    data =  response.json()
    assert isinstance(data, list)
    assert any(user["id"] in users for user in data)
    

def test_get_user():
    if users:
        user_id = users[0]
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert user_id == data["id"]


def test_update_user():
    if users:
        user_id = users[0]
        new_user = {
            "name": "teste01",
        }
        response = client.patch(f"/users/{user_id}", json=new_user)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "teste01"
        
def test_delete_user():
    if users:
        user_id = users[0]
        response = client.delete(f"/users/{user_id}")
        
        assert response.status_code == 200
        
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404