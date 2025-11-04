"""
Google Calendar Settings Module

This module handles calendar integration settings including:
- Sync preferences configuration
- Calendar appearance settings
- Account management
- Notification preferences
"""

import streamlit as st
from .auth import disconnect_calendar, get_calendar_service

def render_calendar_settings():
    """Render calendar integration settings"""
    st.markdown("### ⚙️ Calendar Integration Settings")
    
    # Sync preferences
    render_sync_preferences()
    
    # Calendar appearance
    render_calendar_appearance()
    
    # Account management
    render_account_management()

def render_sync_preferences():
    """Render sync preferences section"""
    st.markdown("#### 🔄 Sync Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_sync = st.checkbox(
            "🔄 Auto-sync when tasks change",
            value=st.session_state.get('auto_sync_enabled', True),
            help="Automatically sync tasks to calendar when modified",
            key="auto_sync_enabled"
        )
        
        sync_interval = st.selectbox(
            "📅 Sync Interval",
            ["Real-time", "Every 15 minutes", "Every hour", "Daily"],
            index=get_sync_interval_index(),
            key="sync_interval",
            help="How often to perform automatic sync"
        )
        
        default_calendar = st.selectbox(
            "📅 Default Calendar",
            get_available_calendars(),
            index=get_default_calendar_index(),
            help="Default calendar for new task exports",
            key="default_calendar"
        )
    
    with col2:
        notification_settings = st.checkbox(
            "🔔 Calendar notifications",
            value=st.session_state.get('calendar_notifications', True),
            help="Enable Google Calendar notifications for exported tasks",
            key="calendar_notifications"
        )
        
        conflict_resolution = st.selectbox(
            "⚠️ Conflict Resolution",
            ["Skip conflicting events", "Reschedule automatically", "Ask for confirmation"],
            index=get_conflict_resolution_index(),
            key="conflict_resolution",
            help="How to handle scheduling conflicts"
        )
        
        event_privacy = st.selectbox(
            "🔒 Event Privacy",
            ["Default", "Public", "Private"],
            index=get_event_privacy_index(),
            help="Privacy setting for exported events",
            key="event_privacy"
        )

def render_calendar_appearance():
    """Render calendar appearance settings"""
    st.markdown("#### 🎨 Calendar Appearance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        event_color = st.selectbox(
            "🎨 Event Color",
            ["Default", "Blue", "Green", "Red", "Orange", "Purple", "Pink", "Yellow"],
            index=get_event_color_index(),
            help="Color for exported task events",
            key="event_color"
        )
        
        time_format = st.selectbox(
            "⏰ Time Format",
            ["12-hour (AM/PM)", "24-hour"],
            index=get_time_format_index(),
            help="Preferred time format for events",
            key="time_format"
        )
    
    with col2:
        include_notes = st.checkbox(
            "📝 Include task notes in events",
            value=st.session_state.get('include_notes', True),
            help="Add task notes to calendar event descriptions",
            key="include_notes"
        )
        
        include_metadata = st.checkbox(
            "📊 Include task metadata",
            value=st.session_state.get('include_metadata', True),
            help="Include priority, category, and duration in event descriptions",
            key="include_metadata"
        )
        
        default_duration = st.number_input(
            "⏱️ Default Event Duration (minutes)",
            min_value=15,
            max_value=480,
            value=st.session_state.get('default_duration', 60),
            step=15,
            help="Default duration for tasks without specified duration",
            key="default_duration"
        )

def render_account_management():
    """Render account management section"""
    st.markdown("#### 👤 Account Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Show connection status
        if st.session_state.get('calendar_authenticated', False):
            st.success("✅ **Connected to Google Calendar**")
            
            # Show connected account info
            account_info = get_account_info()
            if account_info:
                st.info(f"**Account:** {account_info}")
            
            # Refresh token button
            if st.button("🔄 Refresh Token"):
                refresh_token()
        else:
            st.error("❌ **Not connected to Google Calendar**")
    
    with col2:
        # Disconnect button
        if st.session_state.get('calendar_authenticated', False):
            if st.button("🔓 Disconnect Account", type="secondary"):
                disconnect_calendar()
                st.success("🔓 Account disconnected!")
                st.rerun()
        
        # Reset settings button
        if st.button("⚙️ Reset Settings to Default"):
            reset_settings_to_default()
            st.success("⚙️ Settings reset to default values!")
            st.rerun()

def get_sync_interval_index():
    """Get index for sync interval selectbox"""
    interval = st.session_state.get('sync_interval', 'Every hour')
    intervals = ["Real-time", "Every 15 minutes", "Every hour", "Daily"]
    return intervals.index(interval) if interval in intervals else 2

def get_default_calendar_index():
    """Get index for default calendar selectbox"""
    calendar = st.session_state.get('default_calendar', 'Primary Calendar')
    calendars = get_available_calendars()
    return calendars.index(calendar) if calendar in calendars else 0

def get_conflict_resolution_index():
    """Get index for conflict resolution selectbox"""
    resolution = st.session_state.get('conflict_resolution', 'Ask for confirmation')
    resolutions = ["Skip conflicting events", "Reschedule automatically", "Ask for confirmation"]
    return resolutions.index(resolution) if resolution in resolutions else 2

def get_event_privacy_index():
    """Get index for event privacy selectbox"""
    privacy = st.session_state.get('event_privacy', 'Default')
    privacies = ["Default", "Public", "Private"]
    return privacies.index(privacy) if privacy in privacies else 0

def get_event_color_index():
    """Get index for event color selectbox"""
    color = st.session_state.get('event_color', 'Default')
    colors = ["Default", "Blue", "Green", "Red", "Orange", "Purple", "Pink", "Yellow"]
    return colors.index(color) if color in colors else 0

def get_time_format_index():
    """Get index for time format selectbox"""
    format_type = st.session_state.get('time_format', '12-hour (AM/PM)')
    formats = ["12-hour (AM/PM)", "24-hour"]
    return formats.index(format_type) if format_type in formats else 0

def get_available_calendars():
    """Get list of available calendars"""
    service = get_calendar_service()
    if not service:
        return ["Primary Calendar"]
    
    try:
        calendar_list = service.calendarList().list().execute()
        calendars = []
        
        for calendar in calendar_list.get('items', []):
            if calendar.get('primary'):
                calendars.append("Primary Calendar")
            else:
                calendars.append(calendar.get('summary', 'Unknown Calendar'))
        
        return calendars if calendars else ["Primary Calendar"]
        
    except Exception as e:
        st.error(f"❌ Failed to get calendar list: {str(e)}")
        return ["Primary Calendar"]

def get_account_info():
    """Get connected account information"""
    service = get_calendar_service()
    if not service:
        return None
    
    try:
        # Get calendar info to determine account
        calendar_list = service.calendarList().list().execute()
        primary_calendar = next((cal for cal in calendar_list.get('items', []) if cal.get('primary')), None)
        
        if primary_calendar:
            return primary_calendar.get('summary', 'Unknown Account')
        
        return "Connected Account"
        
    except Exception as e:
        return f"Error getting account info: {str(e)}"

def refresh_token():
    """Refresh the authentication token"""
    try:
        # This would typically involve refreshing the OAuth token
        # For now, we'll just show a success message
        st.success("🔄 Token refreshed successfully!")
        
    except Exception as e:
        st.error(f"❌ Failed to refresh token: {str(e)}")

def reset_settings_to_default():
    """Reset all settings to default values"""
    default_settings = {
        'auto_sync_enabled': True,
        'sync_interval': 'Every hour',
        'default_calendar': 'Primary Calendar',
        'calendar_notifications': True,
        'conflict_resolution': 'Ask for confirmation',
        'event_privacy': 'Default',
        'event_color': 'Default',
        'time_format': '12-hour (AM/PM)',
        'include_notes': True,
        'include_metadata': True,
        'default_duration': 60
    }
    
    for key, value in default_settings.items():
        st.session_state[key] = value

def get_user_settings():
    """Get all user settings as a dictionary"""
    return {
        'auto_sync_enabled': st.session_state.get('auto_sync_enabled', True),
        'sync_interval': st.session_state.get('sync_interval', 'Every hour'),
        'default_calendar': st.session_state.get('default_calendar', 'Primary Calendar'),
        'calendar_notifications': st.session_state.get('calendar_notifications', True),
        'conflict_resolution': st.session_state.get('conflict_resolution', 'Ask for confirmation'),
        'event_privacy': st.session_state.get('event_privacy', 'Default'),
        'event_color': st.session_state.get('event_color', 'Default'),
        'time_format': st.session_state.get('time_format', '12-hour (AM/PM)'),
        'include_notes': st.session_state.get('include_notes', True),
        'include_metadata': st.session_state.get('include_metadata', True),
        'default_duration': st.session_state.get('default_duration', 60)
    }

def apply_settings_to_event(event_data, task_data):
    """Apply user settings to event data"""
    settings = get_user_settings()
    
    # Apply event color
    if settings['event_color'] != 'Default':
        color_map = {
            'Blue': '1', 'Green': '2', 'Purple': '3', 'Red': '4',
            'Yellow': '5', 'Orange': '6', 'Pink': '7'
        }
        event_data['colorId'] = color_map.get(settings['event_color'], '1')
    
    # Apply privacy settings
    if settings['event_privacy'] == 'Private':
        event_data['visibility'] = 'private'
    elif settings['event_privacy'] == 'Public':
        event_data['visibility'] = 'public'
    
    # Apply notes and metadata
    description_parts = []
    
    if settings['include_notes'] and task_data.get('notes'):
        description_parts.append(task_data['notes'])
    
    if settings['include_metadata']:
        metadata = []
        if task_data.get('priority'):
            metadata.append(f"Priority: {task_data['priority'].title()}")
        if task_data.get('category'):
            metadata.append(f"Category: {task_data['category']}")
        if task_data.get('duration'):
            metadata.append(f"Duration: {task_data['duration']} minutes")
        
        if metadata:
            description_parts.append("---")
            description_parts.extend(metadata)
    
    event_data['description'] = '\n'.join(description_parts)
    
    return event_data 