import requests
from pathlib import Path

def test_create_todo():
    response = requests.post("http://localhost:8000/todos/", json={
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo"
    assert data["completed"] is False
    return data["id"]

def test_read_todo(todo_id):
    response = requests.get(f"http://localhost:8000/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo"

def test_update_todo(todo_id):
    response = requests.patch(f"http://localhost:8000/todos/{todo_id}", json={
        "title": "Updated Todo",
        "description": "This is an updated test todo",
        "completed": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["description"] == "This is an updated test todo"
    assert data["completed"] is True

def test_delete_todo(todo_id):
    response = requests.delete(f"http://localhost:8000/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True

def test_read_todos():
    response = requests.get("http://localhost:8000/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

if __name__ == "__main__":
    try:
        # Run tests in sequence
        print("Creating TODOs")
        todo_id = test_create_todo()
        print("Reading TODOs")
        test_read_todo(todo_id)
        print("Updating TODOs")
        test_update_todo(todo_id)
        print("Deleting TODOs")
        test_delete_todo(todo_id)
        print("Reading TODOs")
        test_read_todos()
        print("All tests passed successfully!")
        Path('PASSED').touch()
    except Exception as e:
        Path('FAILED').touch()
        print("A test failed:", str(e))
