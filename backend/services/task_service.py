import logging
from typing import List, Optional
from ..database import get_db
from ..models import Task

logger = logging.getLogger(__name__)

class TaskService:
    @staticmethod
    def get_all_tasks() -> List[Task]:
        db = get_db()
        rows = db.execute(
            'SELECT * FROM tasks ORDER BY created_at DESC'
        ).fetchall()
        return [Task.from_row(row) for row in rows]

    @staticmethod
    def get_task(task_id: int) -> Optional[Task]:
        db = get_db()
        row = db.execute(
            'SELECT * FROM tasks WHERE id = ?', (task_id,)
        ).fetchone()
        
        return Task.from_row(row)

    @staticmethod
    def create_task(title: str, description: Optional[str] = None, 
                   assignee: Optional[str] = None, due_date: Optional[str] = None) -> Task:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            'INSERT INTO tasks (title, description, assignee, due_date, status) VALUES (?, ?, ?, ?, ?)',
            (title, description, assignee, due_date, 'pending')
        )
        db.commit()
        
        task_id = cursor.lastrowid
        return TaskService.get_task(task_id)
        
    @staticmethod
    def update_task_status(task_id: int, status: str) -> Optional[Task]:
        db = get_db()
        db.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (status, task_id)
        )
        db.commit()
        return TaskService.get_task(task_id)

    @staticmethod
    def delete_task(task_id: int) -> bool:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()
        return cursor.rowcount > 0
