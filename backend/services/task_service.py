import logging
from datetime import datetime
from typing import List, Optional
from ..database import get_db
from ..models import Task

logger = logging.getLogger(__name__)

class TaskService:
    @staticmethod
    def get_all_tasks() -> List[Task]:
        db = get_db()
        rows = db.execute(
            '''SELECT * FROM tasks 
               ORDER BY 
                 CASE WHEN scheduled_time IS NULL OR scheduled_time = '' THEN 1 ELSE 0 END, 
                 scheduled_time ASC,
                 created_at DESC'''
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
    def get_next_default_time() -> str:
        db = get_db()
        
        # Get tasks created today with times to figure out the next slot
        today = datetime.now().strftime('%Y-%m-%d')
        rows = db.execute(
            '''SELECT scheduled_time FROM tasks 
               WHERE date(created_at) = ? AND scheduled_time IS NOT NULL AND scheduled_time != ""''', 
            (today,)
        ).fetchall()
        
        used_times = set(row['scheduled_time'] for row in rows)
        
        default_slots = ["19:00", "20:00", "21:00", "22:00"]
        for slot in default_slots:
            if slot not in used_times:
                return slot
                
        # If all slots used or something else, default to 19:00 anyway
        return "19:00"

    @staticmethod
    def create_task(title: str, description: Optional[str] = None, 
                   assignee: Optional[str] = None, due_date: Optional[str] = None,
                   scheduled_time: Optional[str] = None) -> Task:
        db = get_db()
        cursor = db.cursor()
        
        if not scheduled_time:
            scheduled_time = TaskService.get_next_default_time()
        
        cursor.execute(
            'INSERT INTO tasks (title, description, assignee, due_date, scheduled_time, status) VALUES (?, ?, ?, ?, ?, ?)',
            (title, description, assignee, due_date, scheduled_time, 'pending')
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
