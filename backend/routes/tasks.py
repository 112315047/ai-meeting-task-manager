import logging
from flask import Blueprint, request, jsonify
from ..services.task_service import TaskService
from ..services.ai_service import AIService

logger = logging.getLogger(__name__)

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('', methods=['GET'])
def get_tasks():
    tasks = TaskService.get_all_tasks()
    return jsonify({"tasks": [t.to_dict() for t in tasks]}), 200

@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = TaskService.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    return jsonify(task.to_dict()), 200

@bp.route('', methods=['POST'])
def create_task():
    data = request.get_json()
    
    # Input validation
    if not data or 'title' not in data:
        logger.warning("Create task failed: missing title parameter")
        return jsonify({"error": "Missing required field: title"}), 400

    title = data.get('title')
    description = data.get('description')
    assignee = data.get('assignee')
    due_date = data.get('due_date')

    # Basic type checking / length constraints conceptually go here
    if not isinstance(title, str) or len(title.strip()) == 0:
        return jsonify({"error": "Title must be a non-empty string"}), 400

    new_task = TaskService.create_task(title, description, assignee, due_date)
    
    # After saving string in SQLite, we might have basic parsing logic or we simply return its dict rep
    return jsonify(new_task.to_dict()), 201
    

@bp.route('/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"error": "Missing required field: status"}), 400
        
    status = data.get('status')
    valid_statuses = ['pending', 'in_progress', 'completed']
    
    if status not in valid_statuses:
         return jsonify({"error": f"Invalid status. Must be one of: {valid_statuses}"}), 400

    updated_task = TaskService.update_task_status(task_id, status)
    
    if not updated_task:
         return jsonify({"error": "Task not found"}), 404

    return jsonify(updated_task.to_dict()), 200

@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    success = TaskService.delete_task(task_id)
    if not success:
         return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 200

@bp.route('/extract', methods=['POST'])
def extract_tasks():
    data = request.get_json()
    notes = data.get("notes")

    extracted = AIService.extract_tasks_from_notes(notes)

    created_tasks = []
    for task in extracted:
        new_task = TaskService.create_task(
            title=task.get("title"),
            description=task.get("description"),
            assignee=task.get("assignee"),
            due_date=task.get("due_date")
        )
        created_tasks.append(new_task.to_dict())

    return jsonify(created_tasks), 201
