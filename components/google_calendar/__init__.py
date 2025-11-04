"""
Google Calendar Integration Module for Chrona Schedule Optimizer

This module provides comprehensive Google Calendar integration functionality,
broken down into specialized components for better organization and maintainability.

Components:
- auth: Handles Google Calendar API authentication and authorization
- export: Manages exporting tasks to Google Calendar
- import_calendar: Handles importing events from Google Calendar
- sync: Manages sync status, history, and operations
- settings: Provides settings and configuration management
- ui: Handles main UI rendering and dashboard components

Main Entry Point:
- render_google_calendar_integration: Main function to render the calendar integration tab
"""

# Import the main rendering function from UI module
from .ui import render_google_calendar_integration

# Import key functions that might be used externally
from .auth import (
    authenticate_google_calendar,
    check_google_calendar_api,
    get_calendar_service,
    is_authenticated,
    disconnect_calendar
)

from .export import (
    export_tasks_to_calendar,
    sync_tasks_to_calendar,
    get_calendar_list
)

from .import_calendar import (
    import_calendar_events,
    import_calendar_events_range,
    get_upcoming_events,
    convert_events_to_tasks
)

from .sync import (
    add_sync_record,
    get_sync_statistics,
    perform_full_sync,
    clear_sync_history
)

from .settings import (
    get_user_settings,
    apply_settings_to_event,
    reset_settings_to_default
)

# Export the main render function for backward compatibility
__all__ = [
    'render_google_calendar_integration',
    'authenticate_google_calendar',
    'check_google_calendar_api',
    'get_calendar_service',
    'is_authenticated',
    'disconnect_calendar',
    'export_tasks_to_calendar',
    'sync_tasks_to_calendar',
    'get_calendar_list',
    'import_calendar_events',
    'import_calendar_events_range',
    'get_upcoming_events',
    'convert_events_to_tasks',
    'add_sync_record',
    'get_sync_statistics',
    'perform_full_sync',
    'clear_sync_history',
    'get_user_settings',
    'apply_settings_to_event',
    'reset_settings_to_default'
] 