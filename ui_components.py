# Main UI components module - now uses modular imports
from components.header import render_header, render_footer
from components.preferences import render_preferences_sidebar
from components.task_form import render_task_form
from components.task_list import render_task_list
from components.schedule_display import render_schedule_results
from components.schedule_feedback import render_schedule_feedback, get_feedback_status, clear_feedback
from components.styles import load_custom_styles

# Load styles when module is imported
load_custom_styles()

# Re-export all components for backward compatibility
__all__ = [
    'render_header',
    'render_footer',
    'render_preferences_sidebar',
    'render_task_form',
    'render_task_list',
    'render_schedule_results',
    'render_schedule_feedback',
    'get_feedback_status',
    'clear_feedback'
]