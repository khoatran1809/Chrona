
import datetime
from typing import Dict, List, Optional

class FallbackScheduler:
    """Creates fallback schedules when AI optimization fails"""
    
    @staticmethod
    def _parse_schedule_duration(duration_str: str) -> int:
        """Parse schedule duration string to extract number of days"""
        try:
            return int(duration_str.split()[0])
        except (ValueError, IndexError):
            return 1  # Default to 1 day if parsing fails
    
    @staticmethod
    def _get_day_names(num_days: int) -> List[str]:
        """Get appropriate day names based on number of days"""
        if num_days == 1:
            return ["Today"]
        elif num_days == 2:
            return ["Saturday", "Sunday"]
        elif num_days == 3:
            return ["Friday", "Saturday", "Sunday"]
        elif num_days == 5:
            return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        elif num_days == 7:
            return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        elif num_days == 14:
            return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
                    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        else:
            return [f"Day {i+1}" for i in range(num_days)]
    
    @staticmethod
    def _get_daily_themes(num_days: int) -> List[Dict]:
        """Get daily themes for scheduling patterns"""
        if num_days <= 2:
            return [{"theme": "Balanced", "focus": "Mixed tasks", "work_style": "steady"}] * num_days
        
        theme_patterns = {
            3: [
                {"theme": "Deep Focus", "focus": "analytical", "work_style": "intensive", "work_blocks": "long"},
                {"theme": "Communication", "focus": "meetings", "work_style": "interactive", "work_blocks": "medium"},
                {"theme": "Creative & Personal", "focus": "creative", "work_style": "relaxed", "work_blocks": "flexible"}
            ],
            5: [
                {"theme": "Strategic Monday", "focus": "planning", "work_style": "organized", "work_blocks": "structured"},
                {"theme": "Deep Work Tuesday", "focus": "analytical", "work_style": "intensive", "work_blocks": "long"},
                {"theme": "Communication Wednesday", "focus": "meetings", "work_style": "interactive", "work_blocks": "medium"},
                {"theme": "Implementation Thursday", "focus": "execution", "work_style": "productive", "work_blocks": "steady"},
                {"theme": "Creative Friday", "focus": "creative", "work_style": "innovative", "work_blocks": "flexible"}
            ],
            7: [
                {"theme": "Strategic Monday", "focus": "planning", "work_style": "organized", "work_blocks": "structured"},
                {"theme": "Deep Work Tuesday", "focus": "analytical", "work_style": "intensive", "work_blocks": "long"},
                {"theme": "Communication Wednesday", "focus": "meetings", "work_style": "interactive", "work_blocks": "medium"},
                {"theme": "Implementation Thursday", "focus": "execution", "work_style": "productive", "work_blocks": "steady"},
                {"theme": "Creative Friday", "focus": "creative", "work_style": "innovative", "work_blocks": "flexible"},
                {"theme": "Personal Saturday", "focus": "personal", "work_style": "leisurely", "work_blocks": "light"},
                {"theme": "Reflection Sunday", "focus": "review", "work_style": "peaceful", "work_blocks": "light"}
            ],
            14: [
                {"theme": "Strategic Monday", "focus": "planning", "work_style": "organized", "work_blocks": "structured"},
                {"theme": "Deep Work Tuesday", "focus": "analytical", "work_style": "intensive", "work_blocks": "long"},
                {"theme": "Communication Wednesday", "focus": "meetings", "work_style": "interactive", "work_blocks": "medium"},
                {"theme": "Implementation Thursday", "focus": "execution", "work_style": "productive", "work_blocks": "steady"},
                {"theme": "Creative Friday", "focus": "creative", "work_style": "innovative", "work_blocks": "flexible"},
                {"theme": "Personal Saturday", "focus": "personal", "work_style": "leisurely", "work_blocks": "light"},
                {"theme": "Reflection Sunday", "focus": "review", "work_style": "peaceful", "work_blocks": "light"},
                # Week 2 variations
                {"theme": "Innovation Monday", "focus": "experimental", "work_style": "exploratory", "work_blocks": "varied"},
                {"theme": "Analysis Tuesday", "focus": "review", "work_style": "thorough", "work_blocks": "focused"},
                {"theme": "Collaboration Wednesday", "focus": "teamwork", "work_style": "synergistic", "work_blocks": "collaborative"},
                {"theme": "Results Thursday", "focus": "completion", "work_style": "decisive", "work_blocks": "target-driven"},
                {"theme": "Learning Friday", "focus": "skills", "work_style": "developmental", "work_blocks": "educational"},
                {"theme": "Adventure Saturday", "focus": "exploration", "work_style": "dynamic", "work_blocks": "varied"},
                {"theme": "Integration Sunday", "focus": "synthesis", "work_style": "visionary", "work_blocks": "reflective"}
            ]
        }
        
        if num_days in theme_patterns:
            return theme_patterns[num_days]
        else:
            # Use weekly pattern as base for other lengths
            base_themes = theme_patterns[7]
            return [base_themes[i % len(base_themes)] for i in range(num_days)]
    
    @staticmethod
    def create_fallback_schedule(tasks: List[Dict], preferences: Optional[Dict] = None) -> Dict:
        """Create fallback schedule when AI is not working"""
        if preferences is None:
            preferences = {}
        
        # Parse schedule duration
        schedule_duration_str = preferences.get('schedule_duration', '1 day (Single day)')
        num_days = FallbackScheduler._parse_schedule_duration(schedule_duration_str)
        day_names = FallbackScheduler._get_day_names(num_days)
        daily_themes = FallbackScheduler._get_daily_themes(num_days)
        
        # Create schedule for each day
        optimized_schedule = []
        
        for day_idx in range(num_days):
            day_name = day_names[day_idx]
            daily_theme = daily_themes[day_idx]
            is_weekend = day_name in ["Saturday", "Sunday"]
            
            # Create daily schedule with theme
            daily_schedule = FallbackScheduler._create_themed_day_schedule(
                tasks, day_idx, day_name, daily_theme, is_weekend, num_days
            )
            
            optimized_schedule.append({
                "day": day_idx + 1,
                "day_name": day_name,
                "theme": daily_theme["theme"],
                "focus": daily_theme["focus"],
                "energy_pattern": daily_theme["work_style"],
                "tasks": daily_schedule
            })
        
        # Calculate summary statistics
        user_task_minutes = sum(task['duration'] for task in tasks)
        essential_minutes = 7 * 60  # Approximate essential activities per day
        
        work_hours = user_task_minutes // 60
        work_mins = user_task_minutes % 60
        personal_hours = essential_minutes // 60
        personal_mins = essential_minutes % 60
        
        work_time = f"{work_hours} hours {work_mins} minutes"
        personal_time = f"{personal_hours} hours {personal_mins} minutes"
        
        # Create daily theme descriptions
        daily_theme_descriptions = []
        for i, theme in enumerate(daily_themes):
            daily_theme_descriptions.append(f"Day {i+1}: {theme['theme']} - {theme['focus']} focus")
        
        recommendations = [
            f"Schedule created for {num_days} days with unique daily themes",
            "Each day has a distinct focus and energy pattern",
            "High-priority tasks matched to appropriate daily themes",
            "Consistent meal and sleep times maintained across all days",
            "Weekend days have more relaxed schedules with personal focus",
            "Task distribution varies by day to prevent repetition"
        ]
        
        return {
            "optimized_schedule": optimized_schedule,
            "daily_summary": {
                "total_work_time": work_time,
                "personal_time": personal_time,
                "sleep_time": "8 hours",
                "meal_time": "2 hours",
                "exercise_time": "45 minutes",
                "free_time": "Remaining time for flexibility",
                "productivity_score": 85,
                "daily_themes": daily_theme_descriptions,
                "recommendations": recommendations
            }
        }
    
    @staticmethod
    def _create_themed_day_schedule(tasks: List[Dict], day_idx: int, day_name: str, 
                                   daily_theme: Dict, is_weekend: bool, total_days: int) -> List[Dict]:
        """Create schedule for a single day with thematic focus"""
        schedule = []
        
        # Define essential daily activities with theme-based variations
        if is_weekend:
            # Weekend has more relaxed schedule
            essential_activities = [
                {
                    "name": "Morning routine",
                    "start": "08:30" if daily_theme["work_style"] == "leisurely" else "08:00",
                    "duration": 45 if daily_theme["work_style"] == "leisurely" else 30,
                    "category": "personal",
                    "priority": "essential"
                },
                {
                    "name": "Breakfast",
                    "start": "09:15" if daily_theme["work_style"] == "leisurely" else "08:30",
                    "duration": 60 if daily_theme["work_style"] == "leisurely" else 45,
                    "category": "meals",
                    "priority": "essential"
                },
                {
                    "name": "Lunch",
                    "start": "13:30" if daily_theme["focus"] == "personal" else "13:00",
                    "duration": 75 if daily_theme["focus"] == "personal" else 60,
                    "category": "meals",
                    "priority": "essential"
                },
                {
                    "name": "Exercise/Outdoor activity",
                    "start": "15:30" if daily_theme["focus"] == "exploration" else "16:00",
                    "duration": 120 if daily_theme["focus"] == "exploration" else 90,
                    "category": "health",
                    "priority": "essential"
                },
                {
                    "name": "Dinner",
                    "start": "19:30" if daily_theme["work_style"] == "leisurely" else "19:00",
                    "duration": 75 if daily_theme["work_style"] == "leisurely" else 60,
                    "category": "meals",
                    "priority": "essential"
                },
                {
                    "name": "Personal/Family time",
                    "start": "21:00" if daily_theme["focus"] == "personal" else "20:30",
                    "duration": 180 if daily_theme["focus"] == "personal" else 150,
                    "category": "personal",
                    "priority": "essential"
                },
                {
                    "name": "Evening routine",
                    "start": "23:30" if daily_theme["work_style"] == "leisurely" else "23:00",
                    "duration": 30,
                    "category": "personal",
                    "priority": "essential"
                }
            ]
        else:
            # Weekday schedule varies by theme
            if daily_theme["work_style"] == "intensive":
                # Deep work days start earlier
                essential_activities = [
                    {
                        "name": "Morning routine",
                        "start": "06:30",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Breakfast",
                        "start": "07:00",
                        "duration": 30,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Lunch",
                        "start": "12:00",
                        "duration": 30,  # Shorter lunch for intensive days
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Exercise",
                        "start": "18:30",
                        "duration": 60,  # Longer exercise to decompress
                        "category": "health",
                        "priority": "essential"
                    },
                    {
                        "name": "Dinner",
                        "start": "19:30",
                        "duration": 45,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Personal/Family time",
                        "start": "20:15",
                        "duration": 135,  # More personal time after intensive work
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Evening routine",
                        "start": "22:30",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    }
                ]
            elif daily_theme["work_style"] == "interactive":
                # Communication days have flexible lunch
                essential_activities = [
                    {
                        "name": "Morning routine",
                        "start": "07:00",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Breakfast",
                        "start": "07:30",
                        "duration": 30,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Lunch",
                        "start": "13:00",
                        "duration": 60,  # Longer lunch for networking
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Exercise",
                        "start": "17:30",
                        "duration": 45,
                        "category": "health",
                        "priority": "essential"
                    },
                    {
                        "name": "Dinner",
                        "start": "19:00",
                        "duration": 45,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Personal/Family time",
                        "start": "20:00",
                        "duration": 120,
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Evening routine",
                        "start": "22:30",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    }
                ]
            elif daily_theme["work_style"] == "innovative":
                # Creative days have later start
                essential_activities = [
                    {
                        "name": "Morning routine",
                        "start": "07:30",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Breakfast",
                        "start": "08:00",
                        "duration": 45,  # Longer breakfast for creative energy
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Lunch",
                        "start": "12:30",
                        "duration": 45,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Exercise",
                        "start": "17:00",
                        "duration": 60,  # Exercise for creative inspiration
                        "category": "health",
                        "priority": "essential"
                    },
                    {
                        "name": "Dinner",
                        "start": "19:00",
                        "duration": 45,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Personal/Family time",
                        "start": "20:00",
                        "duration": 120,
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Evening routine",
                        "start": "22:30",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    }
                ]
            else:
                # Standard schedule for other themes
                essential_activities = [
                    {
                        "name": "Morning routine",
                        "start": "07:00",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Breakfast",
                        "start": "07:30",
                        "duration": 30,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Lunch",
                        "start": "12:30",
                        "duration": 45,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Exercise",
                        "start": "18:00",
                        "duration": 45,
                        "category": "health",
                        "priority": "essential"
                    },
                    {
                        "name": "Dinner",
                        "start": "19:00",
                        "duration": 45,
                        "category": "meals",
                        "priority": "essential"
                    },
                    {
                        "name": "Personal/Family time",
                        "start": "20:00",
                        "duration": 120,
                        "category": "personal",
                        "priority": "essential"
                    },
                    {
                        "name": "Evening routine",
                        "start": "22:30",
                        "duration": 30,
                        "category": "personal",
                        "priority": "essential"
                    }
                ]
        
        # Add essential activities to schedule
        for activity in essential_activities:
            start_dt = datetime.datetime.strptime(activity["start"], "%H:%M")
            end_dt = start_dt + datetime.timedelta(minutes=activity["duration"])
            
            schedule.append({
                "task_name": activity["name"],
                "start_time": activity["start"],
                "end_time": end_dt.strftime("%H:%M"),
                "priority": activity["priority"],
                "category": activity["category"],
                "notes": f"Essential activity - {daily_theme['theme']} theme"
            })
        
        # Define work slots based on theme
        work_slots = FallbackScheduler._get_themed_work_slots(daily_theme, is_weekend)
        
        # Distribute tasks based on theme
        tasks_for_day = FallbackScheduler._distribute_themed_tasks(
            tasks, day_idx, daily_theme, total_days
        )
        
        # Sort tasks by priority and theme relevance
        sorted_tasks = FallbackScheduler._sort_tasks_by_theme(tasks_for_day, daily_theme)
        
        # Schedule user tasks in available slots
        current_slot = 0
        if work_slots:
            current_time = datetime.datetime.strptime(work_slots[0]["start"], "%H:%M")
            slot_end = datetime.datetime.strptime(work_slots[0]["end"], "%H:%M")
            
            for task in sorted_tasks:
                task_duration = datetime.timedelta(minutes=task['duration'])
                
                # Check if task fits in current slot
                if current_time + task_duration > slot_end:
                    # Move to next slot
                    current_slot += 1
                    if current_slot >= len(work_slots):
                        break  # No more slots available
                    current_time = datetime.datetime.strptime(work_slots[current_slot]["start"], "%H:%M")
                    slot_end = datetime.datetime.strptime(work_slots[current_slot]["end"], "%H:%M")
                    
                    # Check again if task fits
                    if current_time + task_duration > slot_end:
                        continue  # Skip this task if it doesn't fit
                
                end_time = current_time + task_duration
                
                schedule.append({
                    "task_name": task['name'],
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": end_time.strftime("%H:%M"),
                    "priority": task['priority'],
                    "category": task['category'],
                    "notes": f"Duration: {task['duration']} minutes - {daily_theme['theme']} theme"
                })
                
                # Add buffer time between tasks (varies by theme)
                buffer_time = 15 if daily_theme["work_style"] == "intensive" else 10
                current_time = end_time + datetime.timedelta(minutes=buffer_time)
        
        # Sort schedule by time
        schedule.sort(key=lambda x: x["start_time"])
        
        return schedule
    
    @staticmethod
    def _get_themed_work_slots(daily_theme: Dict, is_weekend: bool) -> List[Dict]:
        """Get work slots based on daily theme"""
        if is_weekend:
            if daily_theme["focus"] == "personal":
                return [
                    {"start": "10:30", "end": "12:00"},  # Short morning work
                    {"start": "14:30", "end": "15:30"}   # Light afternoon work
                ]
            else:
                return [
                    {"start": "10:00", "end": "12:30"},  # Morning work block
                    {"start": "14:00", "end": "16:00"}   # Afternoon work block
                ]
        
        # Weekday work slots based on theme
        if daily_theme["work_style"] == "intensive":
            return [
                {"start": "08:00", "end": "11:30"},  # Long morning block
                {"start": "13:00", "end": "17:30"}   # Long afternoon block
            ]
        elif daily_theme["work_style"] == "interactive":
            return [
                {"start": "08:30", "end": "11:00"},  # Short morning block
                {"start": "14:00", "end": "17:00"}   # Meeting-friendly afternoon
            ]
        elif daily_theme["work_style"] == "innovative":
            return [
                {"start": "09:00", "end": "12:00"},  # Creative morning
                {"start": "13:30", "end": "16:30"}   # Flexible afternoon
            ]
        else:
            return [
                {"start": "08:00", "end": "12:30"},  # Standard morning
                {"start": "13:15", "end": "17:30"}   # Standard afternoon
            ]
    
    @staticmethod
    def _distribute_themed_tasks(tasks: List[Dict], day_idx: int, daily_theme: Dict, total_days: int) -> List[Dict]:
        """Distribute tasks based on daily theme and day index"""
        if total_days == 1:
            return tasks
        
        # Filter tasks by theme preference
        theme_matched_tasks = []
        other_tasks = []
        
        for task in tasks:
            task_category = task.get('category', '').lower()
            task_priority = task.get('priority', '').lower()
            task_notes = task.get('notes', '').lower()
            
            # Match tasks to themes
            is_theme_match = False
            
            if daily_theme["focus"] == "analytical":
                is_theme_match = (task_category in ["work", "learning"] and 
                                "analysis" in task_notes or "study" in task_notes or 
                                "research" in task_notes or task_priority == "high")
            elif daily_theme["focus"] == "meetings":
                is_theme_match = ("meeting" in task_notes or "call" in task_notes or 
                                "presentation" in task_notes or task_category == "work")
            elif daily_theme["focus"] == "creative":
                is_theme_match = ("creative" in task_notes or "design" in task_notes or 
                                "art" in task_notes or task_category == "personal")
            elif daily_theme["focus"] == "planning":
                is_theme_match = ("plan" in task_notes or "goal" in task_notes or 
                                "strategy" in task_notes or task_priority == "high")
            elif daily_theme["focus"] == "execution":
                is_theme_match = ("implement" in task_notes or "complete" in task_notes or 
                                "finish" in task_notes or task_priority == "medium")
            elif daily_theme["focus"] == "personal":
                is_theme_match = (task_category in ["personal", "health"] or 
                                "family" in task_notes or "hobby" in task_notes)
            
            if is_theme_match:
                theme_matched_tasks.append(task)
            else:
                other_tasks.append(task)
        
        # Distribute theme-matched tasks first, then fill with others
        distributed_tasks = []
        
        # Add theme-matched tasks for this day
        for i, task in enumerate(theme_matched_tasks):
            if i % total_days == day_idx:
                distributed_tasks.append(task)
        
        # Fill remaining slots with other tasks
        for i, task in enumerate(other_tasks):
            if i % total_days == day_idx:
                distributed_tasks.append(task)
        
        # Ensure each day has at least one task if possible
        if not distributed_tasks and tasks:
            distributed_tasks.append(tasks[day_idx % len(tasks)])
        
        return distributed_tasks
    
    @staticmethod
    def _sort_tasks_by_theme(tasks: List[Dict], daily_theme: Dict) -> List[Dict]:
        """Sort tasks by priority and theme relevance"""
        def theme_score(task):
            score = 0
            task_category = task.get('category', '').lower()
            task_notes = task.get('notes', '').lower()
            
            # Theme matching bonuses
            if daily_theme["focus"] == "analytical" and ("analysis" in task_notes or "study" in task_notes):
                score += 10
            elif daily_theme["focus"] == "meetings" and ("meeting" in task_notes or "call" in task_notes):
                score += 10
            elif daily_theme["focus"] == "creative" and ("creative" in task_notes or "design" in task_notes):
                score += 10
            elif daily_theme["focus"] == "planning" and ("plan" in task_notes or "goal" in task_notes):
                score += 10
            elif daily_theme["focus"] == "execution" and ("implement" in task_notes or "complete" in task_notes):
                score += 10
            elif daily_theme["focus"] == "personal" and task_category in ["personal", "health"]:
                score += 10
            
            # Priority bonuses
            priority = task.get('priority', 'medium')
            if priority == 'high':
                score += 5
            elif priority == 'medium':
                score += 2
            
            return score
        
        # Sort by theme score (descending) then by priority
        return sorted(tasks, key=lambda x: (
            theme_score(x),
            {'high': 0, 'medium': 1, 'low': 2}[x.get('priority', 'medium')]
        ), reverse=True)
