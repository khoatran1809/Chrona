
from typing import Dict, Any, Optional
from datetime import datetime

class Task:
    """Task data model with validation"""
    
    def __init__(self, task_data: Dict[str, Any]):
        self.name = task_data.get('name', '').strip()
        self.duration = task_data.get('duration', 0)
        self.priority = task_data.get('priority', 'medium')
        self.category = task_data.get('category', 'other')
        self.preferred_time = task_data.get('preferred_time', 'No preference')
        self.notes = task_data.get('notes', '')
        self.deadline = task_data.get('deadline', None)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary format"""
        return {
            "name": self.name,
            "duration_minutes": self.duration,
            "priority": self.priority,
            "category": self.category,
            "preferred_time": self.preferred_time,
            "notes": self.notes,
            "deadline": self.deadline
        }
    
    def validate(self) -> Optional[str]:
        """Validate task data and return error message if invalid"""
        if not self.name:
            return "Task has no name"
        
        if self.duration < 15:
            return f"Task '{self.name}' duration is too short"
        
        if self.duration > 480:  # 8 hours
            return f"Task '{self.name}' duration is too long"
        
        return None
