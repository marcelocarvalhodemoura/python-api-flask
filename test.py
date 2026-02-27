import pytest
import requests

# CRUD Test
BASE_URL = "http://127.0.0.1:5000"
tasks=[]

def test_create_task():
    new_task_data={
        "title":"Nova Tarefa",
        "description":"Descrição da nova tarefa",
    }
    response=requests.post(f"{BASE_URL}/tasks",json=new_task_data)
    assert response.status_code == 200 # valida o status code, caso seja diferente de 200, o teste falha
    response_json=response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json["id"])

def test_get_tasks():
    response=requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json=response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json
       
def test_get_task():
    if tasks:
        task_id=tasks[0]
        response=requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json=response.json()
        assert "id" in response_json
        assert "title" in response_json
        assert "description" in response_json
        assert "completed" in response_json
        
def test_update_task():
    if tasks:
        task_id=tasks[0]
        update_task_data={
            "title":"Tarefa Atualizada",
            "description":"Descrição da tarefa atualizada",
            "completed":True
        }
        response=requests.put(f"{BASE_URL}/tasks/{task_id}",json=update_task_data)
        assert response.status_code == 200
        response_json=response.json()
        assert "message" in response_json
        assert "task" in response_json
        assert response_json["task"]["title"] == update_task_data["title"]
        assert response_json["task"]["description"] == update_task_data["description"]
        assert response_json["task"]["completed"] == update_task_data["completed"]

def test_delete_task():
    if tasks:
        task_id=tasks[0]
        response=requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json=response.json()
        assert "message" in response_json
        tasks.remove(task_id)
    

    