from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    assignee: Optional[str]
    due_date: Optional[datetime]
    scheduled_time: Optional[str]
    created_at: Optional[datetime]
    
    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
            
        def parse_dt(val):
            if not val:
                return None
            if isinstance(val, datetime):
                return val
            try:
                return datetime.fromisoformat(val)
            except ValueError:
                try:
                    return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return None
        
        return cls(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            status=row['status'],
            assignee=row['assignee'],
            due_date=parse_dt(row['due_date']),
            scheduled_time=row['scheduled_time'] if 'scheduled_time' in row.keys() else None,
            created_at=parse_dt(row['created_at'])
        )
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "assignee": self.assignee,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "scheduled_time": self.scheduled_time,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
