
import datetime
from typing import List, Dict

class ScheduleValidator:
    """Service for validating schedules and detecting conflicts"""
    
    @staticmethod
    def validate_tasks(tasks: List[Dict]) -> List[str]:
        """Validate tasks and return list of errors"""
        errors = []

        for i, task in enumerate(tasks):
            if not task.get('name', '').strip():
                errors.append(f"Task {i+1} has no name")

            if task.get('duration', 0) < 15:
                errors.append(f"Task '{task.get('name', f'Task {i+1}')}' duration is too short")

            if task.get('duration', 0) > 480:  # 8 hours
                errors.append(f"Task '{task.get('name', f'Task {i+1}')}' duration is too long")

        return errors

    @staticmethod
    def detect_schedule_conflicts(schedule: List[Dict]) -> List[str]:
        """Detect time conflicts in schedule"""
        conflicts = []

        for i, task1 in enumerate(schedule):
            for j, task2 in enumerate(schedule[i + 1:], i + 1):
                start1 = datetime.datetime.strptime(task1.get('start_time', '00:00'), '%H:%M').time()
                end1 = datetime.datetime.strptime(task1.get('end_time', '00:00'), '%H:%M').time()
                start2 = datetime.datetime.strptime(task2.get('start_time', '00:00'), '%H:%M').time()
                end2 = datetime.datetime.strptime(task2.get('end_time', '00:00'), '%H:%M').time()

                # Check for overlap
                if (start1 < end2 and start2 < end1):
                    conflicts.append(
                        f"Time conflict between '{task1.get('task_name')}' and '{task2.get('task_name')}'"
                    )

        return conflicts
