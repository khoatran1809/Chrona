import google.genai as genai
import json
import re
import streamlit as st
from typing import List, Dict, Any

from services.prompt_generator import PromptGenerator
from services.fallback_scheduler import FallbackScheduler
from services.schedule_validator import ScheduleValidator


class ScheduleOptimizer:
    """Main schedule optimization coordinator"""

    def __init__(self):
        self.tasks = []
        self.optimized_schedule = None
        self.client = None

    def initialize_genai(self, api_key: str) -> bool:
        """Initialize Google GenAI"""
        try:
            self.client = genai.Client(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Optimization error: {str(e)}")
            return False

    def add_task(self, task_data: Dict[str, Any]):
        """Add new task"""
        self.tasks.append(task_data)

    def optimize_schedule(self, preferences: Dict) -> Dict:
        """Optimize schedule using Google GenAI with enhanced error handling"""
        if not self.tasks:
            return {"error": "No tasks to optimize. Please add some tasks first."}

        # Check if client is initialized
        if not self.client:
            return {"error": "API client not initialized. Please check your API key."}

        # Validate tasks before optimization
        validation_errors = ScheduleValidator.validate_tasks(self.tasks)
        if validation_errors:
            return {"error": f"Task validation failed: {'; '.join(validation_errors)}"}

        try:
            prompt = PromptGenerator.generate_schedule_prompt(self.tasks, preferences)

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp', contents=prompt)

            response_text = response.text

            if response_text:
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            else:
                json_match = None

            if json_match:
                json_str = json_match.group()
                try:
                    result = json.loads(json_str)
                    self.optimized_schedule = result
                    return result
                except json.JSONDecodeError:
                    return FallbackScheduler.create_fallback_schedule(self.tasks, preferences)
            else:
                return FallbackScheduler.create_fallback_schedule(self.tasks, preferences)

        except Exception as e:
            st.error(f"Optimization error: {str(e)}")
            return FallbackScheduler.create_fallback_schedule(self.tasks, preferences)

    def validate_tasks(self) -> List[str]:
        """Validate tasks using the validator service"""
        return ScheduleValidator.validate_tasks(self.tasks)

    def detect_schedule_conflicts(self, schedule: List[Dict]) -> List[str]:
        """Detect schedule conflicts using the validator service"""
        return ScheduleValidator.detect_schedule_conflicts(schedule)

    def create_fallback_schedule(self) -> Dict:
        """Create fallback schedule using the fallback service"""
        return FallbackScheduler.create_fallback_schedule(self.tasks, {})