from src.main import app  # importa o app FastAPI
from fastapi.testclient import TestClient

client = TestClient(app)
registration = []


def test_create_registration():
    new_course = {"student_id": 1, "course_id": 41}
    response = client.post("/registration", json=new_course)
    
    assert response.status_code == 200
    data = response.json()
    assert new_course["student_id"] == data["student_id"]
    assert new_course["course_id"] == data["course_id"]
    registration.append(data)
    
    
def test_get_registration():
    student_id = registration[0]["student_id"]
    response = client.get(f"/registration/student/{student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == student_id
