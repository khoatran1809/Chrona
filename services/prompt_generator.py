
import json
from typing import List, Dict

class PromptGenerator:
    """Service for generating AI optimization prompts"""
    
    @staticmethod
    def _parse_schedule_duration(duration_str: str) -> int:
        """Parse schedule duration string to extract number of days"""
        # Extract number from strings like "1 day (Single day)", "7 days (Full week)", etc.
        try:
            return int(duration_str.split()[0])
        except (ValueError, IndexError):
            return 1  # Default to 1 day if parsing fails
    
    @staticmethod
    def _get_daily_themes(num_days: int) -> List[Dict]:
        """Get unique daily themes for multi-day schedules"""
        if num_days <= 2:
            return [{"theme": "Balanced", "focus": "Mixed tasks", "energy": "Steady"}] * num_days
        
        # Define theme patterns for different schedule lengths
        theme_patterns = {
            3: [
                {"theme": "Deep Focus", "focus": "Complex/analytical tasks", "energy": "Peak morning", "style": "Intensive"},
                {"theme": "Communication", "focus": "Meetings/social tasks", "energy": "Afternoon peak", "style": "Interactive"},
                {"theme": "Creative & Personal", "focus": "Creative work/personal time", "energy": "Flexible", "style": "Relaxed"}
            ],
            4: [
                {"theme": "Strategic Planning", "focus": "Planning/analysis", "energy": "Morning peak", "style": "Thoughtful"},
                {"theme": "Execution", "focus": "Implementation/action", "energy": "Steady", "style": "Productive"},
                {"theme": "Communication", "focus": "Meetings/collaboration", "energy": "Afternoon peak", "style": "Interactive"},
                {"theme": "Creative & Recovery", "focus": "Creative/personal", "energy": "Flexible", "style": "Balanced"}
            ],
            5: [
                {"theme": "Strategic Monday", "focus": "Planning/priority tasks", "energy": "Fresh start", "style": "Organized"},
                {"theme": "Deep Work Tuesday", "focus": "Complex/analytical tasks", "energy": "Peak focus", "style": "Intensive"},
                {"theme": "Communication Wednesday", "focus": "Meetings/collaboration", "energy": "Mid-week energy", "style": "Interactive"},
                {"theme": "Implementation Thursday", "focus": "Execution/action items", "energy": "Steady momentum", "style": "Productive"},
                {"theme": "Creative Friday", "focus": "Creative/flexible tasks", "energy": "End-week creativity", "style": "Innovative"}
            ],
            7: [
                {"theme": "Strategic Monday", "focus": "Weekly planning/priorities", "energy": "Fresh start", "style": "Organized"},
                {"theme": "Deep Work Tuesday", "focus": "Complex/analytical tasks", "energy": "Peak focus", "style": "Intensive"},
                {"theme": "Communication Wednesday", "focus": "Meetings/collaboration", "energy": "Mid-week energy", "style": "Interactive"},
                {"theme": "Implementation Thursday", "focus": "Execution/action items", "energy": "Steady momentum", "style": "Productive"},
                {"theme": "Creative Friday", "focus": "Creative/flexible tasks", "energy": "End-week creativity", "style": "Innovative"},
                {"theme": "Personal Saturday", "focus": "Personal/family time", "energy": "Relaxed", "style": "Leisurely"},
                {"theme": "Reflection Sunday", "focus": "Review/preparation", "energy": "Contemplative", "style": "Peaceful"}
            ],
            14: [
                {"theme": "Strategic Monday", "focus": "Weekly planning/priorities", "energy": "Fresh start", "style": "Organized"},
                {"theme": "Deep Work Tuesday", "focus": "Complex/analytical tasks", "energy": "Peak focus", "style": "Intensive"},
                {"theme": "Communication Wednesday", "focus": "Meetings/collaboration", "energy": "Mid-week energy", "style": "Interactive"},
                {"theme": "Implementation Thursday", "focus": "Execution/action items", "energy": "Steady momentum", "style": "Productive"},
                {"theme": "Creative Friday", "focus": "Creative/flexible tasks", "energy": "End-week creativity", "style": "Innovative"},
                {"theme": "Personal Saturday", "focus": "Personal/family time", "energy": "Relaxed", "style": "Leisurely"},
                {"theme": "Reflection Sunday", "focus": "Review/preparation", "energy": "Contemplative", "style": "Peaceful"},
                # Week 2 with variations
                {"theme": "Innovation Monday", "focus": "New ideas/experimentation", "energy": "Renewed focus", "style": "Exploratory"},
                {"theme": "Analysis Tuesday", "focus": "Review/optimization", "energy": "Analytical peak", "style": "Thorough"},
                {"theme": "Collaboration Wednesday", "focus": "Team/partnership work", "energy": "Cooperative", "style": "Synergistic"},
                {"theme": "Results Thursday", "focus": "Completing/delivering", "energy": "Achievement mode", "style": "Decisive"},
                {"theme": "Learning Friday", "focus": "Skills/knowledge building", "energy": "Growth mindset", "style": "Developmental"},
                {"theme": "Adventure Saturday", "focus": "Exploration/activities", "energy": "Adventurous", "style": "Dynamic"},
                {"theme": "Integration Sunday", "focus": "Integration/planning ahead", "energy": "Synthesizing", "style": "Visionary"}
            ]
        }
        
        # Get closest pattern or create custom pattern
        if num_days in theme_patterns:
            return theme_patterns[num_days]
        else:
            # Create custom pattern for other lengths
            base_themes = theme_patterns[7]  # Use weekly pattern as base
            custom_themes = []
            for i in range(num_days):
                theme_idx = i % len(base_themes)
                custom_themes.append(base_themes[theme_idx])
            return custom_themes
    
    @staticmethod
    def generate_schedule_prompt(tasks: List[Dict], preferences: Dict) -> str:
        """Generate prompt for Google GenAI to optimize schedule"""

        # Parse schedule duration
        schedule_duration_str = preferences.get('schedule_duration', '1 day (Single day)')
        num_days = PromptGenerator._parse_schedule_duration(schedule_duration_str)
        
        # Get daily themes for unique scheduling
        daily_themes = PromptGenerator._get_daily_themes(num_days)
        
        # Extract task details more clearly
        task_details = []
        for task in tasks:
            task_info = {
                "name": task.get('name', 'Unnamed Task'),
                "duration_minutes": task.get('duration', 0),
                "priority": task.get('priority', 'medium'),
                "category": task.get('category', 'other'),
                "preferred_time": task.get('preferred_time', 'No preference'),
                "notes": task.get('notes', ''),
                "deadline": task.get('deadline', None)
            }
            task_details.append(task_info)

        # Generate day names for the schedule
        if num_days == 1:
            day_description = "single day"
        elif num_days == 2:
            day_description = "weekend (Saturday & Sunday)"
        elif num_days == 3:
            day_description = "long weekend (Friday, Saturday & Sunday)"
        elif num_days == 5:
            day_description = "workweek (Monday to Friday)"
        elif num_days == 7:
            day_description = "full week (Monday to Sunday)"
        elif num_days == 14:
            day_description = "two weeks (14 days)"
        else:
            day_description = f"{num_days} days"

        # Create daily theme descriptions
        theme_descriptions = []
        for i, theme in enumerate(daily_themes):
            theme_descriptions.append(f"Day {i+1}: {theme['theme']} - Focus on {theme['focus']} with {theme['energy']} energy in a {theme['style']} style")
        
        theme_section = "\n".join(theme_descriptions)

        prompt = f"""
        You are Chrona AI, an expert schedule optimization system. Your mission is to create a scientifically-optimized {num_days}-day schedule that maximizes productivity while maintaining work-life balance.

        === CRITICAL TECHNICAL REQUIREMENTS ===
        1. TIME FORMAT: ONLY use HH:MM format (00:00 to 23:59). NEVER use 24:00 - use 00:00 for midnight
        2. PRECISION: Every minute counts - no overlapping times or gaps within each day
        3. VALIDATION: All times must be chronologically logical within each day
        4. CONSISTENCY: Maintain exact duration as specified by user
        5. MULTI-DAY STRUCTURE: Create {num_days} separate daily schedules for the {day_description}

        === USER TASKS TO OPTIMIZE ===
        {json.dumps(task_details, ensure_ascii=False, indent=2)}

        === SCHEDULE DURATION REQUIREMENTS ===
        Number of Days: {num_days}
        Schedule Type: {day_description}
        
        === UNIQUE DAILY THEMES FOR {str(num_days).upper()}-DAY SCHEDULE ===
        CRITICAL: Each day must have a UNIQUE theme and focus. Create distinctly different daily patterns:
        
        {theme_section}
        
        THEME IMPLEMENTATION RULES:
        - DEEP FOCUS days: Schedule complex analytical tasks in morning, minimize interruptions, longer work blocks
        - COMMUNICATION days: Schedule meetings, calls, collaborative work, social tasks
        - CREATIVE days: Schedule brainstorming, design work, artistic tasks, flexible timing
        - STRATEGIC days: Schedule planning, goal-setting, analysis, review tasks
        - IMPLEMENTATION days: Schedule action items, execution tasks, practical work
        - PERSONAL days: Schedule family time, hobbies, personal development, relaxed pace
        - REFLECTION days: Schedule review, meditation, planning, lighter workload
        
        TASK DISTRIBUTION STRATEGY:
        - Distribute similar tasks across different days to avoid repetition
        - Match task types to daily themes (analytical tasks on Deep Focus days, etc.)
        - Create variety in daily schedules - no two days should look the same
        - Balance high-energy and low-energy activities across the week
        - Use different time slots for similar activities on different days

        === USER PRODUCTIVITY PROFILE ===
        Peak Performance Hours: {preferences.get('peak_hours', 'Morning')}
        Optimal Break Duration: {preferences.get('break_time', '15 minutes')}
        Work Priority Focus: {preferences.get('work_type', 'Important work')}
        Schedule Flexibility: {preferences.get('flexibility', 3)}/5 (1=rigid, 5=very flexible)

        {f"""=== USER CHAT REQUEST & SCHEDULE MODIFICATIONS ===
        CRITICAL: The user has provided specific instructions about what they want changed in their EXISTING schedule.
        You MUST take their current schedule and modify it based on their natural language request:

        USER REQUEST: {preferences.get('user_schedule_request')}

        MODIFICATION APPROACH:
        - START with the existing schedule structure
        - MODIFY only what the user specifically requested
        - MAINTAIN all other tasks and timing that work well
        - ADJUST surrounding tasks only if necessary to accommodate changes
        - PRESERVE user preferences and task requirements
        - APPLY changes consistently across all {num_days} days where applicable
        - MAINTAIN daily themes while incorporating user requests

        NATURAL LANGUAGE PROCESSING RULES:
        - "move [task] to [time]" → Reschedule specific task to requested time
        - "add [duration] for [activity]" → Insert new time block for specified activity
        - "make [task] longer/shorter" → Adjust duration of specific task
        - "more study time" → Increase study/learning activity duration
        - "math in morning" → Move math-related tasks to morning hours (06:00-12:00)
        - "english in evening" → Move English-related tasks to evening hours (18:00-22:00)
        - "1 hour each" → Ensure specified activities get exactly 1 hour duration
        - "earlier" or "move earlier" → Push start times earlier (subtract 1-2 hours)
        - "later" or "move later" → Push start times later (add 1-2 hours)
        - "longer breaks" or "more break time" → Increase buffer periods between activities
        - "morning person" or "productive in morning" → Schedule important tasks 06:00-12:00
        - "evening person" or "productive in evening" → Schedule important tasks 18:00-22:00
        - "group similar tasks" → Batch similar activities together
        - "no meetings before [time]" → Avoid scheduling meetings/calls before specified time
        - "I need time for" → Add requested activity to schedule
        
        CONTEXTUAL UNDERSTANDING:
        - Parse specific times mentioned (e.g., "6 AM", "2 PM", "evening", "morning")
        - Understand duration requests (e.g., "30 minutes", "an hour", "1 hour each")
        - Recognize task preferences (e.g., "morning workouts", "afternoon meetings")
        - Identify constraints (e.g., "not before 9 AM", "after 5 PM only")
        - Understand subject-specific requests (e.g., "math", "english", "study")
        
        Apply these modifications while maintaining schedule validity, user task requirements, and daily themes.
        """ if preferences.get('user_schedule_request') else ''}

        === INTELLIGENT SCHEDULING ALGORITHM ===

        PRIORITY MATRIX:
        1. CRITICAL: Sleep (7.5-8h), Safety, Health emergencies
        2. ESSENTIAL: Meals, Hygiene, Deadlines within 24h
        3. HIGH: User high-priority tasks, Exercise, Family time
        4. MEDIUM: User medium-priority tasks, Social activities
        5. LOW: User low-priority tasks, Optional activities

        TIME SLOT OPTIMIZATION:
        • Morning (06:00-12:00): Cognitive peak - complex/creative tasks
        • Afternoon (12:00-18:00): Steady energy - routine/administrative tasks
        • Evening (18:00-22:00): Social/family time, light activities
        • Night (22:00-06:00): Sleep, recovery, preparation

        PREFERENCE PARSING RULES:
        - "Morning (6-12)" → Schedule between 06:00-11:59
        - "Afternoon (12-18)" → Schedule between 12:00-17:59  
        - "Evening (18-22)" → Schedule between 18:00-21:59
        - Notes with specific times (e.g., "6h to 8h30 p.m") → ABSOLUTE PRIORITY
        - "theatre", "cinema", "movie" → Consider venue operating hours
        - Travel/location changes → Add 15-30min buffer time

        CIRCADIAN RHYTHM OPTIMIZATION:
        - Deep work: 09:00-11:00, 14:00-16:00
        - Creative tasks: 10:00-12:00
        - Physical exercise: 07:00-09:00 or 17:00-19:00
        - Social activities: 19:00-21:00
        - Wind-down: 21:00-22:00

        === MANDATORY DAILY STRUCTURE ===
        SLEEP: 6.5-8 hours (recommended: 23:00-07:00 or 22:30-06:30)
        MEALS: 
        - Breakfast: 07:00-09:00 (30 min)
        - Lunch: 12:00-14:00 (45 min)
        - Dinner: 18:00-20:00 (45 min)
        HYGIENE:
        - Morning routine: 15-30 min after waking
        - Evening routine: 15-30 min before sleep
        EXERCISE: 30-60 min (adapt to user preference/schedule)
        FAMILY/PERSONAL: Minimum 1-2 hours quality time
        BUFFER: 10-15 min between different locations/activities

        === ENHANCED MULTI-DAY SCHEDULING RULES ===
        1. THEME-BASED DISTRIBUTION: Match tasks to daily themes (analytical → Deep Focus, meetings → Communication)
        2. ENERGY CYCLES: Account for different energy levels throughout the multi-day period
        3. VARIETY MANDATE: Each day must be distinctly different - no repetitive patterns
        4. WEEKEND DIFFERENTIATION: Weekend days have relaxed schedules with personal focus
        5. PROGRESSION BUILDING: Create momentum across days (preparation → execution → reflection)
        6. RECOVERY INTEGRATION: Include lighter days after intensive work days
        7. CONSISTENCY MAINTENANCE: Keep sleep and meal schedules consistent across all days
        8. TASK ROTATION: Rotate similar tasks across different days and time slots
        9. FOCUS SPECIALIZATION: Each day specializes in specific types of work
        10. TEMPORAL VARIETY: Use different time slots for similar activities on different days

        === ADVANCED OPTIMIZATION RULES ===
        1. Deadline Urgency: Tasks with today's deadline get premium time slots
        2. Energy Matching: Match task complexity to natural energy levels and daily themes
        3. Context Switching: Minimize transitions between different task types within each day
        4. Realistic Timing: Include preparation, travel, and cleanup time
        5. Stress Prevention: Avoid back-to-back high-intensity activities
        6. Flow State: Group similar tasks for sustained focus, especially on themed days
        7. Recovery Periods: Schedule micro-breaks every 90-120 minutes
        8. Theme Coherence: Maintain thematic consistency within each day
        9. Cross-Day Balance: Ensure overall balance across the entire multi-day period
        10. Adaptive Scheduling: Adjust daily patterns based on theme requirements

        === OUTPUT REQUIREMENTS ===
        Return ONLY valid JSON with exact structure below. NO additional text or explanations.

        {{
            "optimized_schedule": [
                {{
                    "day": 1,
                    "day_name": "Monday",
                    "theme": "Strategic Monday",
                    "focus": "Weekly planning/priorities",
                    "energy_pattern": "Fresh start",
                    "tasks": [
                        {{
                            "task_name": "Sleep",
                            "start_time": "23:00",
                            "end_time": "07:00",
                            "priority": "essential",
                            "category": "Personal",
                            "notes": "8 hours for optimal recovery and cognitive function"
                        }},
                        {{
                            "task_name": "Morning Routine",
                            "start_time": "07:00",
                            "end_time": "07:30",
                            "priority": "essential",
                            "category": "Personal",
                            "notes": "Hygiene, preparation for the day"
                        }},
                        {{
                            "task_name": "[User Task Name]",
                            "start_time": "HH:MM",
                            "end_time": "HH:MM",
                            "priority": "[exact user priority]",
                            "category": "[exact user category]",
                            "notes": "Optimally scheduled during [daily theme] as requested"
                        }}
                    ]
                }},
                {{
                    "day": 2,
                    "day_name": "Tuesday",
                    "theme": "Deep Work Tuesday",
                    "focus": "Complex/analytical tasks",
                    "energy_pattern": "Peak focus",
                    "tasks": [
                        {{
                            "task_name": "Sleep",
                            "start_time": "23:00",
                            "end_time": "07:00",
                            "priority": "essential",
                            "category": "Personal",
                            "notes": "8 hours for optimal recovery and cognitive function"
                        }},
                        {{
                            "task_name": "Morning Routine",
                            "start_time": "07:00",
                            "end_time": "07:30",
                            "priority": "essential",
                            "category": "Personal",
                            "notes": "Hygiene, preparation for the day"
                        }}
                    ]
                }}
            ],
            "daily_summary": {{
                "total_work_time": "X hours Y minutes",
                "personal_time": "X hours Y minutes", 
                "sleep_time": "8 hours",
                "meal_time": "2 hours",
                "exercise_time": "X minutes",
                "free_time": "X hours Y minutes",
                "productivity_score": 85,
                "daily_themes": [
                    "Day 1: Strategic Monday - Focus on weekly planning",
                    "Day 2: Deep Work Tuesday - Complex analytical tasks"
                ],
                "recommendations": [
                    "Each day follows a unique theme for optimal variety",
                    "Tasks are distributed to match daily energy patterns",
                    "Consistent sleep and meal schedules maintained",
                    "Daily themes create focused work environments"
                ]
            }}
        }}

        CRITICAL NOTES:
        - Create exactly {num_days} day objects in the optimized_schedule array
        - Each day MUST have a unique theme, focus, and energy pattern
        - Use appropriate day names based on the schedule type
        - Distribute user tasks strategically across days matching daily themes
        - Ensure each day is a complete 24-hour schedule with distinct characteristics
        - Make each day genuinely unique and optimized for its specific theme

        === QUALITY ASSURANCE CHECKLIST ===
        ✓ All user tasks scheduled across the {num_days} days
        ✓ Each day has a unique theme and focus
        ✓ Tasks are matched to appropriate daily themes
        ✓ Specific time requests in notes honored
        ✓ No time overlaps or impossible sequences within each day
        ✓ Realistic duration for each activity
        ✓ Proper energy-task matching with themes
        ✓ Adequate buffer times included
        ✓ Work-life balance maintained across all days
        ✓ JSON format is valid and complete
        ✓ Each day has genuinely different scheduling patterns
        ✓ Tasks are distributed strategically across themed days
        ✓ Daily themes are properly implemented in task selection
        """
        return prompt
