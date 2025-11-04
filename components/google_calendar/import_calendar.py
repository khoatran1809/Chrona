"""
Google Calendar Import Module

This module handles importing events from Google Calendar including:
- Event retrieval from calendar
- Date range selection
- Event preview and display
- Converting events to tasks
"""

import streamlit as st
import datetime
from datetime import timedelta

from .auth import get_calendar_service

def render_import_section(optimizer):
    """Render calendar import section"""
    st.markdown("### 📥 Import from Google Calendar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Select Date Range")
        
        import_start = st.date_input(
            "From Date",
            value=datetime.date.today(),
            key="import_start"
        )
        
        import_end = st.date_input(
            "To Date", 
            value=datetime.date.today() + timedelta(days=7),
            key="import_end"
        )
    
    with col2:
        st.markdown("#### 🔽 Import Options")
        
        import_calendar = st.selectbox(
            "📅 Source Calendar",
            ["Primary Calendar", "Work Calendar", "Personal Calendar"],
            help="Select which Google Calendar to import from"
        )
        
        convert_to_tasks = st.checkbox(
            "🔄 Convert events to tasks",
            value=True,
            help="Convert calendar events to optimizer tasks"
        )
    
    if st.button("📥 Import Calendar Events", type="primary"):
        import_calendar_events_range(import_start, import_end, import_calendar, convert_to_tasks)
    
    # Show preview of upcoming events
    st.markdown("#### 👀 Preview: Upcoming Events")
    
    # Get real calendar events
    preview_events = get_upcoming_events(days=7)
    
    if preview_events:
        for event in preview_events:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{event['summary']}**")
                with col2:
                    st.write(f"⏰ {event['start_time']}")
                with col3:
                    st.write(f"📅 {event['date']}")
    else:
        st.info("📅 No upcoming events found or not connected to Google Calendar")

def import_calendar_events(optimizer):
    """Import events from Google Calendar"""
    service = get_calendar_service()
    if not service:
        st.error("❌ Not connected to Google Calendar!")
        return
    
    with st.spinner("Importing events from Google Calendar..."):
        try:
            # Get events for the next 7 days
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            end_time = (datetime.datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            st.success(f"✅ Successfully imported {len(events)} calendar events!")
            
            # Display imported events
            if events:
                st.markdown("#### 📅 Imported Events:")
                for event in events[:5]:  # Show first 5 events
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    st.write(f"- **{event['summary']}** ({start})")
                    
        except Exception as e:
            st.error(f"❌ Import failed: {str(e)}")

def import_calendar_events_range(start_date, end_date, calendar_name, convert_to_tasks):
    """Import calendar events from specified date range"""
    service = get_calendar_service()
    if not service:
        st.error("❌ Not connected to Google Calendar!")
        return
    
    with st.spinner(f"Importing events from {calendar_name}..."):
        try:
            # Convert dates to ISO format
            start_iso = datetime.datetime.combine(start_date, datetime.time.min).isoformat() + 'Z'
            end_iso = datetime.datetime.combine(end_date, datetime.time.max).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_iso,
                timeMax=end_iso,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            st.success(f"✅ Successfully imported {len(events)} events from {calendar_name}!")
            
            # Display imported events
            if events:
                st.markdown("#### 📅 Imported Events:")
                
                # Create a more detailed view of imported events
                for event in events:
                    with st.expander(f"📅 {event.get('summary', 'Untitled Event')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            start_time = event['start'].get('dateTime', event['start'].get('date'))
                            end_time = event['end'].get('dateTime', event['end'].get('date'))
                            
                            st.write(f"**Start:** {start_time}")
                            st.write(f"**End:** {end_time}")
                            
                            if event.get('location'):
                                st.write(f"**Location:** {event['location']}")
                        
                        with col2:
                            if event.get('description'):
                                st.write(f"**Description:** {event['description']}")
                            
                            if event.get('creator'):
                                st.write(f"**Creator:** {event['creator'].get('email', 'Unknown')}")
                
                if convert_to_tasks:
                    # Convert events to tasks (this would need to be implemented in the optimizer)
                    converted_tasks = convert_events_to_tasks(events)
                    st.info(f"🔄 Converted {len(converted_tasks)} events to optimizer tasks!")
                    
                    # Show converted tasks
                    if converted_tasks:
                        st.markdown("#### 🔄 Converted Tasks:")
                        for task in converted_tasks:
                            st.write(f"- **{task['name']}** ({task['duration']} min)")
                
        except Exception as e:
            st.error(f"❌ Import failed: {str(e)}")

def get_upcoming_events(days=7):
    """Get upcoming events from Google Calendar"""
    service = get_calendar_service()
    if not service:
        return []
    
    try:
        # Get events for the next specified days
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end_time = (datetime.datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_time,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Format events for display
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            # Parse datetime
            if 'T' in start:
                # DateTime format
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                time_str = dt.strftime('%I:%M %p')
                date_str = dt.strftime('%m/%d')
                if dt.date() == datetime.date.today():
                    date_str = "Today"
                elif dt.date() == datetime.date.today() + timedelta(days=1):
                    date_str = "Tomorrow"
            else:
                # Date only format
                time_str = "All Day"
                dt = datetime.datetime.fromisoformat(start)
                date_str = dt.strftime('%m/%d')
            
            formatted_events.append({
                'summary': event.get('summary', 'Untitled Event'),
                'start_time': time_str,
                'date': date_str,
                'description': event.get('description', ''),
                'location': event.get('location', '')
            })
        
        return formatted_events
        
    except Exception as e:
        st.error(f"❌ Failed to get upcoming events: {str(e)}")
        return []

def convert_events_to_tasks(events):
    """Convert calendar events to optimizer tasks"""
    converted_tasks = []
    
    for event in events:
        # Calculate duration
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))
        
        duration = 60  # Default duration
        if 'T' in start_time and 'T' in end_time:
            # Both are datetime objects
            start_dt = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            duration = int((end_dt - start_dt).total_seconds() / 60)
        
        # Create task
        task = {
            'name': event.get('summary', 'Imported Event'),
            'duration': duration,
            'priority': 'medium',
            'category': 'Calendar Import',
            'notes': event.get('description', ''),
            'location': event.get('location', '')
        }
        
        converted_tasks.append(task)
    
    return converted_tasks

def get_calendar_events_by_date(target_date):
    """Get calendar events for a specific date"""
    service = get_calendar_service()
    if not service:
        return []
    
    try:
        # Set up date range for the target date
        start_time = datetime.datetime.combine(target_date, datetime.time.min).isoformat() + 'Z'
        end_time = datetime.datetime.combine(target_date, datetime.time.max).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
        
    except Exception as e:
        st.error(f"❌ Failed to get events for {target_date}: {str(e)}")
        return [] 