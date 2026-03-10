import json
from backend.services.task_service import TaskService

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_task(client):
    response = client.post('/tasks/', json={
        'title': 'Test Task',
        'description': 'Description for test task',
        'assignee': 'John Doe'
    })
    assert response.status_code == 201
    data = response.json
    assert data['title'] == 'Test Task'
    assert data['status'] == 'pending'
    assert 'id' in data

def test_get_tasks(client):
    # First create a task
    client.post('/tasks/', json={'title': 'Another Task'})
    
    response = client.get('/tasks/')
    assert response.status_code == 200
    assert len(response.json['tasks']) >= 1

def test_update_task_status(client):
    create_response = client.post('/tasks/', json={'title': 'Status Task'})
    task_id = create_response.json['id']
    
    response = client.patch(f'/tasks/{task_id}/status', json={'status': 'completed'})
    assert response.status_code == 200
    assert response.json['status'] == 'completed'
    
def test_extract_tasks(client):
    response = client.post('/tasks/extract', json={
        'notes': 'We need to build the frontend components by Friday.'
    })
    assert response.status_code == 200
    data = response.json
    assert 'extracted_tasks' in data
    assert len(data['extracted_tasks']) > 0
