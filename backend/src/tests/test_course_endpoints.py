from src.main import app  # importa o app FastAPI
from fastapi.testclient import TestClient
from src.schema.course import CourseBase

client = TestClient(app)
courses = []


def test_create_course():
    new_course = {"name": "teste", "video": "teste", "teacher_id": 30}
    response = client.post("/course", json=new_course)
    
    assert response.status_code == 200
    data = response.json()
    assert "teste" in data["name"]
    courses.append(data)
    
def test_get_courses():
    response = client.get("course")
    assert response.status_code == 200
    data = response.json()
    assert any(course in courses for course in data)

def test_get_course():
    course_id = courses[0]["id"]
    response = client.get(f"/course/{course_id}")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == course_id

def test_get_course_teacher_id():
    teacher_id = courses[0]["teacher_id"]
    response = client.get(f"/course/teacher/{teacher_id}")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["teacher_id"] == teacher_id
